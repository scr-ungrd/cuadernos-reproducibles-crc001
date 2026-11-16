"""Infraestructura crítica del AOI desde OpenStreetMap (Overpass API): hospitales, clínicas, hogares de
adultos mayores y colegios. © colaboradores de OpenStreetMap (ODbL).

Salida: data/osm_infraestructura_monteria.csv  (tipo, nombre, lat, lon)
"""
from pathlib import Path
import time
import pandas as pd
import requests
from config import BBOX, USER_AGENT

RAIZ = Path(__file__).resolve().parent.parent
W, S, E, N = BBOX
CONSULTA = f"""[out:json][timeout:90];
(nwr["amenity"~"^(hospital|clinic|nursing_home|school)$"]({S},{W},{N},{E});
 nwr["social_facility"="nursing_home"]({S},{W},{N},{E}););
out center tags;"""


def main():
    for intento in range(4):
        # Overpass exige un User-Agent identificable; se usa un nombre genérico del cuaderno (config.py)
        r = requests.post("https://overpass-api.de/api/interpreter", data={"data": CONSULTA}, timeout=120,
                          headers={"User-Agent": USER_AGENT})
        if r.status_code == 200:
            break
        time.sleep(30 * (intento + 1))
    r.raise_for_status()
    filas = []
    for e in r.json()["elements"]:
        t = e.get("tags", {})
        lat = e.get("lat") or e.get("center", {}).get("lat")
        lon = e.get("lon") or e.get("center", {}).get("lon")
        tipo = t.get("amenity") or ("nursing_home" if t.get("social_facility") == "nursing_home" else None)
        if tipo and lat and lon:
            filas.append((tipo, t.get("name", ""), lat, lon))
    df = pd.DataFrame(filas, columns=["tipo", "nombre", "lat", "lon"]).drop_duplicates()
    df.to_csv(RAIZ / "data" / "osm_infraestructura_monteria.csv", index=False)
    print(df.tipo.value_counts().to_string())


if __name__ == "__main__":
    main()
