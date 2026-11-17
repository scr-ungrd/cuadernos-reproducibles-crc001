"""Pruebas automáticas de los datos de `data/`: estructura, duplicados, rangos, control de calidad y sumas de verificación.

Uso:  python scripts/probar_datos.py
Falla con un mensaje claro si un archivo está mal formado, si un valor sale de su rango o si una suma SHA-256 no coincide
con `metadata/descargas.csv`. Se ejecuta en el despliegue antes de construir el sitio.
"""
import csv
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
errores = []


def comprobar(cond, mensaje):
    if not cond:
        errores.append(mensaje)


def campos_por_fila(ruta):
    """Conjunto de números de campos por fila (más de uno indica una coma sin comillas)."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return {len(fila) for fila in csv.reader(f)}


ESPERADAS = {
    "ideam_diario_los_garzones.csv": ["fecha", "tx", "n_tx", "tn", "n_tn", "control_calidad"],
    "ideam_diario_incoder.csv": ["fecha", "tx", "n_tx", "tn", "n_tn", "control_calidad"],
    "ideam_humidex_diario_los_garzones.csv": ["fecha", "hx_max", "hx_mean", "n_horas", "t_hxmax", "rh_hxmax"],
    "era5land_diario_monteria.csv": ["fecha", "tx", "tn", "hx_max", "hx_mean", "t_hxmax", "td_hxmax"],
    "nex_gddp_celdas_3x3_anual.csv": ["modelo", "escenario", "anio", "lat", "lon", "tx_medio", "tn_medio", "p_tx90"],
    "osm_infraestructura_monteria.csv": ["tipo", "nombre", "lat", "lon"],
}
for nombre, columnas in ESPERADAS.items():
    ruta = DATA / nombre
    comprobar(ruta.exists(), f"{nombre}: no existe")
    if not ruta.exists():
        continue
    comprobar(len(campos_por_fila(ruta)) == 1, f"{nombre}: las filas no tienen el mismo número de campos")
    try:
        d = pd.read_csv(ruta)
    except Exception as e:
        errores.append(f"{nombre}: no se puede leer ({str(e)[:90]})")
        continue
    comprobar(list(d.columns) == columnas, f"{nombre}: columnas distintas de las esperadas")
    comprobar(not d.duplicated().any(), f"{nombre}: hay filas duplicadas")
    if "fecha" in d:
        f = pd.to_datetime(d["fecha"], format="%Y-%m-%d", errors="coerce")
        comprobar(f.notna().all(), f"{nombre}: fechas que no están en AAAA-MM-DD")
        comprobar(f.is_monotonic_increasing and f.is_unique, f"{nombre}: fechas desordenadas o repetidas")

# IDEAM: control de calidad coherente con la regla del cuaderno y valores plausibles tras el control
for nombre, n_falla in (("ideam_diario_los_garzones.csv", 59), ("ideam_diario_incoder.csv", 83)):
    d = pd.read_csv(DATA / nombre)
    con_dato = d.tx.notna() & d.tn.notna()
    regla = (d.tn >= 17) & ((d.tx - d.tn) <= 16) & (d.tn <= d.tx)
    esperado = np.where(con_dato, np.where(regla, "ok", "falla"), "")
    real = d.control_calidad.fillna("").values
    comprobar((esperado == real).all(), f"{nombre}: `control_calidad` no coincide con la regla (Tmín ≥ 17, rango ≤ 16, Tmín ≤ Tmáx)")
    comprobar(int((real == "falla").sum()) == n_falla, f"{nombre}: se esperaban {n_falla} días con falla y hay {int((real == 'falla').sum())}")
    ok = d[d.control_calidad == "ok"]
    comprobar(ok.tx.between(20, 45).all() and ok.tn.between(17, 32).all(), f"{nombre}: Tmáx o Tmín fuera de rango en los días válidos")

# NEX-GDDP-CMIP6: modelos, escenarios y variables
nex = xr.open_dataset(DATA / "nex_gddp_celda_estacion.nc")
comprobar(sorted(str(m) for m in nex.modelo.values) == sorted(["ACCESS-CM2", "MPI-ESM1-2-HR", "MRI-ESM2-0", "NorESM2-MM", "CMCC-ESM2"]), "NEX-GDDP-CMIP6: modelos distintos de los cinco esperados")
comprobar(sorted(str(e) for e in nex.escenario.values) == ["ssp245", "ssp370", "ssp585"], "NEX-GDDP-CMIP6: escenarios distintos de los esperados")
comprobar(float(nex.tx.min()) > 15 and float(nex.tx.max()) < 50, "NEX-GDDP-CMIP6: Tmáx fuera de 15 a 50 °C")

# OSM: coordenadas dentro del área de estudio (con margen)
osm = pd.read_csv(DATA / "osm_infraestructura_monteria.csv")
comprobar(osm.lat.between(8.5, 9.0).all() and osm.lon.between(-76.2, -75.6).all(), "osm_infraestructura_monteria.csv: coordenadas fuera del área de estudio")

# Sumas de verificación contra metadata/descargas.csv
with open(RAIZ / "metadata" / "descargas.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        ruta = RAIZ / fila["archivo"]
        if not ruta.exists():
            errores.append(f"descargas.csv: {fila['archivo']} no existe")
            continue
        h = hashlib.sha256()
        with open(ruta, "rb") as g:
            for bloque in iter(lambda: g.read(1 << 20), b""):
                h.update(bloque)
        comprobar(h.hexdigest() == fila["sha256"], f"{fila['archivo']}: la suma SHA-256 no coincide con descargas.csv")

if errores:
    print("FALLAN LAS PRUEBAS DE DATOS:")
    print("\n".join(" - " + e for e in errores))
    sys.exit(1)
print("Pruebas de datos: todas correctas.")
