"""Compuesto de temperatura de superficie (LST) Landsat 8/9 Collection 2 Level 2 para Montería.

Fuente: Microsoft Planetary Computer (STAC landsat-c2-l2; la firma de URL es anónima y gratuita).
Banda térmica 'lwir11' (ST_B10): K = DN * 0,00341802 + 149,0. Máscara de nubes, sombras y cirros con 'qa_pixel'.
Periodo 2018-2024, nubosidad de escena < 40 %. Rejilla común UTM 18N a 30 m.

Salida: data/lst_monteria_2018_2024.tif con 6 bandas:
  1 media de todas las fechas, 2 P90 de todas las fechas, 3 número de fechas válidas,
  4 media de la época seca (dic-mar), 5 P90 de la época seca, 6 número de fechas válidas (seca)
Las imágenes se toman hacia las 10:30 hora local: es LST diurna de la mañana, no de la tarde.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.transform import from_origin
from rasterio.vrt import WarpedVRT
from rasterio.warp import transform_bounds, Resampling
import pystac_client
import planetary_computer as pc

RAIZ = Path(__file__).resolve().parent.parent
from config import BBOX as _BBOX
BBOX = list(_BBOX)   # oeste, sur, este, norte
CRS_UTM = CRS.from_epsg(32618)
RES = 30.0


def rejilla():
    w, s, e, n = transform_bounds("EPSG:4326", CRS_UTM, *BBOX)
    w, n = np.floor(w / RES) * RES, np.ceil(n / RES) * RES
    ancho, alto = int(np.ceil((e - w) / RES)), int(np.ceil((n - s) / RES))
    return from_origin(w, n, RES, RES), ancho, alto


TRANSFORM, ANCHO, ALTO = rejilla()


def leer(item):
    try:
        out = {}
        for nombre in ("lwir11", "qa_pixel"):
            with rasterio.open(item.assets[nombre].href) as ds:
                with WarpedVRT(ds, crs=CRS_UTM, transform=TRANSFORM, width=ANCHO, height=ALTO,
                               resampling=Resampling.nearest, nodata=0) as vrt:
                    out[nombre] = vrt.read(1)
        dn, qa = out["lwir11"].astype("float32"), out["qa_pixel"]
        malo = (qa & 0b111111) != 0          # relleno, nube dilatada, cirro, nube, sombra, nieve
        lst = dn * 0.00341802 + 149.0 - 273.15
        lst[(dn == 0) | malo | (lst < 15) | (lst > 65)] = np.nan
        return item.datetime, lst
    except Exception as e:
        print("fallo", item.id, str(e)[:80], flush=True)
        return None


def main():
    cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1",
                                    modifier=pc.sign_inplace)
    busq = cat.search(collections=["landsat-c2-l2"], bbox=BBOX, datetime="2018-01-01/2024-12-31",
                      query={"eo:cloud_cover": {"lt": 40}, "platform": {"in": ["landsat-8", "landsat-9"]}})
    items = list(busq.items())
    print(len(items), "escenas", flush=True)
    res = []
    with ThreadPoolExecutor(4) as ex:
        for i, r in enumerate(ex.map(leer, items), 1):
            if r is not None:
                res.append(r)
            if i % 20 == 0:
                print(i, "/", len(items), flush=True)
    fechas = np.array([r[0] for r in res])
    pila = np.stack([r[1] for r in res])
    seca = np.array([f.month in (12, 1, 2, 3) for f in fechas])
    # Solo píxeles con al menos 5 fechas válidas
    def resumen(p):
        n = np.sum(~np.isnan(p), axis=0).astype("float32")
        media = np.nanmean(p, axis=0)
        p90 = np.nanpercentile(p, 90, axis=0)
        media[n < 5] = np.nan
        p90[n < 5] = np.nan
        return media.astype("float32"), p90.astype("float32"), n
    a = resumen(pila)
    b = resumen(pila[seca])
    bandas = [a[0], a[1], a[2], b[0], b[1], b[2]]
    out = RAIZ / "data" / "lst_monteria_2018_2024.tif"
    with rasterio.open(out, "w", driver="GTiff", height=ALTO, width=ANCHO, count=6, dtype="float32",
                       crs=CRS_UTM, transform=TRANSFORM, nodata=np.nan, compress="deflate") as dst:
        for k, bnd in enumerate(bandas, 1):
            dst.write(bnd, k)
        dst.descriptions = ("lst_media", "lst_p90", "n_fechas", "lst_media_seca", "lst_p90_seca", "n_fechas_seca")
    print("escrito", out, "| escenas válidas:", len(res), "| época seca:", int(seca.sum()), flush=True)


if __name__ == "__main__":
    main()
