"""Población WorldPop 2020 (100 m, restringida a edificaciones) recortada a Montería.

Fuente: data.worldpop.org, producto Global_2000_2020_Constrained (BSGM), archivo col_ppp_2020_constrained.tif (27 MB).
El servidor no admite lecturas parciales (Range), así que se baja entero a un temporal, se recorta y se borra.
Las estructuras por edad y sexo de WorldPop pesan ~0,5 GB por grupo en Colombia y no se usan aquí: la vulnerabilidad
por edad queda pendiente del censo DANE 2018 por manzana (ver Sección de Fase 5).

Salida: data/worldpop_monteria_2020.tif (1 banda: personas por celda de 100 m)
"""
from pathlib import Path
import tempfile
import numpy as np
import rasterio
from rasterio.windows import from_bounds
import requests

RAIZ = Path(__file__).resolve().parent.parent
from config import BBOX
URL = "https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/BSGM/COL/col_ppp_2020_constrained.tif"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "x.tif"
        with requests.get(URL, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(f, "wb") as fh:
                for bloque in r.iter_content(1 << 20):
                    fh.write(bloque)
        with rasterio.open(f) as ds:
            w = from_bounds(*BBOX, transform=ds.transform).round_offsets().round_lengths()
            a = ds.read(1, window=w).astype("float32")
            a[(a < 0) | ~np.isfinite(a)] = 0
            tr, crs = ds.window_transform(w), ds.crs
    out = RAIZ / "data" / "worldpop_monteria_2020.tif"
    with rasterio.open(out, "w", driver="GTiff", height=a.shape[0], width=a.shape[1], count=1, dtype="float32",
                       crs=crs, transform=tr, compress="deflate") as dst:
        dst.write(a, 1)
        dst.descriptions = ("poblacion_2020",)
    print("escrito", out, "| población total en el AOI:", round(float(a.sum())))


if __name__ == "__main__":
    main()
