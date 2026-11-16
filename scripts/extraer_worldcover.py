"""Fracciones de cobertura ESA WorldCover 2021 (10 m) agregadas a la rejilla de 30 m del compuesto LST.

Fuente: Planetary Computer (colección esa-worldcover, asset 'map', firma anónima). Clases: 10 árboles, 20 arbustos,
30 pastizal, 40 cultivos, 50 construido, 60 suelo desnudo, 80 agua, 90 humedal herbáceo, 95 manglar, 100 musgo.
Salida: data/worldcover_monteria_2021.tif con 5 bandas (fracción 0-1 por celda de 30 m):
  construido, arboles, agua, manglar, otros_vegetacion (arbustos + pastizal + cultivos + humedal herbáceo)
"""
from pathlib import Path
import numpy as np
import rasterio
from rasterio.transform import Affine
from rasterio.vrt import WarpedVRT
from rasterio.warp import Resampling
import pystac_client
import planetary_computer as pc

RAIZ = Path(__file__).resolve().parent.parent
LST = RAIZ / "data" / "lst_monteria_2018_2024.tif"


def main():
    with rasterio.open(LST) as ref:
        crs, tr, ancho, alto, bounds = ref.crs, ref.transform, ref.width, ref.height, ref.bounds
        wgs = rasterio.warp.transform_bounds(crs, "EPSG:4326", *bounds)
    cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=pc.sign_inplace)
    items = list(cat.search(collections=["esa-worldcover"], bbox=wgs, datetime="2021-01-01/2021-12-31").items())
    print(len(items), "teselas")
    tr10 = Affine(10.0, 0, tr.c, 0, -10.0, tr.f)
    clases = np.zeros((alto * 3, ancho * 3), dtype="uint8")
    for it in items:
        with rasterio.open(it.assets["map"].href) as ds:
            with WarpedVRT(ds, crs=crs, transform=tr10, width=ancho * 3, height=alto * 3,
                           resampling=Resampling.nearest, nodata=0) as vrt:
                a = vrt.read(1)
                clases = np.where(clases == 0, a, clases)

    def frac(mask):
        return mask.reshape(alto, 3, ancho, 3).mean(axis=(1, 3)).astype("float32")
    bandas = [frac(clases == 50), frac(clases == 10), frac(clases == 80), frac(clases == 95),
              frac(np.isin(clases, [20, 30, 40, 90]))]
    out = RAIZ / "data" / "worldcover_monteria_2021.tif"
    with rasterio.open(out, "w", driver="GTiff", height=alto, width=ancho, count=5, dtype="float32",
                       crs=crs, transform=tr, compress="deflate") as dst:
        for k, b in enumerate(bandas, 1):
            dst.write(b, k)
        dst.descriptions = ("construido", "arboles", "agua", "manglar", "otra_vegetacion")
    print("escrito", out)


if __name__ == "__main__":
    main()
