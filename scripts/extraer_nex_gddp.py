"""Extrae series diarias de tasmax y tasmin de NEX-GDDP-CMIP6 (NASA) para una ventana 3x3 de celdas
(0,25 grados) alrededor de Montería, por el NetCDF Subset Service de THREDDS (corte en el servidor, sin credenciales).

Uso:  python scripts/extraer_nex_gddp.py            # descarga lo que falte (reanuda)
Salida: data/raw/nex_gddp_monteria.nc  (modelo, escenario, tiempo, lat, lon)
Cache por archivo anual: data/raw/nex/<modelo>_<escenario>_<var>_<anio>.nc
"""
from pathlib import Path
import json, re, socket, sys, time
import requests

# El servidor THREDDS de la NASA no responde por IPv6 y Python espera ~70 s antes de caer a IPv4: se fuerza IPv4.
_getaddrinfo = socket.getaddrinfo
socket.getaddrinfo = lambda *a, **k: [r for r in _getaddrinfo(*a, **k) if r[0] == socket.AF_INET]
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import xarray as xr

MODELOS = ["ACCESS-CM2", "MPI-ESM1-2-HR", "MRI-ESM2-0", "NorESM2-MM", "CMCC-ESM2"]
ESCENARIOS = {"historical": range(1985, 2015), "ssp245": range(2015, 2081), "ssp370": range(2015, 2081),
              "ssp585": range(2015, 2081)}
VARS = ["tasmax", "tasmin"]
# Ventana 3x3 de celdas (ver config.py)
from config import NEX_LATS as LATS, NEX_LONS as LONS
BASE = "https://ds.nccs.nasa.gov/thredds"
RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / "data" / "raw" / "nex"
CACHE.mkdir(parents=True, exist_ok=True)


def catalogo(modelo, esc, var):
    """Archivos anuales de un modelo, escenario y variable en el catálogo THREDDS (se guarda en caché local)."""
    cache = CACHE / "catalogos" / f"{modelo}_{esc}_{var}.json"
    if cache.exists():
        return {int(a): u for a, u in json.loads(cache.read_text()).items()}
    url = f"{BASE}/catalog/AMES/NEX/GDDP-CMIP6/{modelo}/{esc}/r1i1p1f1/{var}/catalog.xml"
    for intento in range(4):
        try:
            # 'Connection: close': con urllib el servidor mantenía la conexión abierta 60 s por catálogo
            txt = requests.get(url, timeout=60, headers={"Connection": "close"}).text
            out = dict((int(m.group(2)), m.group(1)) for m in
                       re.finditer(r'urlPath="([^"]*_(\d{4})(?:_v[\d.]+)?\.nc)"', txt))
            if out:
                cache.parent.mkdir(exist_ok=True)
                cache.write_text(json.dumps(out))
                return out
        except Exception:
            pass
        time.sleep(3 * (intento + 1))
    raise RuntimeError(f"sin catálogo {modelo} {esc} {var}")


def extraer(tarea):
    """Baja un año de un modelo/escenario/variable: subconjunto 3x3 por NetCDF Subset Service (HTTP simple)."""
    modelo, esc, var, anio, path = tarea
    out = CACHE / f"{modelo}_{esc}_{var}_{anio}.nc"
    if out.exists():
        return out
    params = {"var": var, "north": max(LATS) + 0.075, "south": min(LATS) - 0.075,
              "west": min(LONS) - 0.075, "east": max(LONS) + 0.075, "horizStride": 1,
              "time_start": f"{anio}-01-01T00:00:00Z", "time_end": f"{anio}-12-31T23:59:59Z", "accept": "netcdf"}
    tmp = out.with_suffix(".tmp")
    for intento in range(6):
        try:
            r = requests.get(f"{BASE}/ncss/grid/{path}", params=params, timeout=180, headers={"Connection": "close"})
            r.raise_for_status()
            tmp.write_bytes(r.content)
            ds = xr.open_dataset(tmp)
            if ds[var].shape[1:] != (len(LATS), len(LONS)) or ds[var].shape[0] < 360:
                raise ValueError(f"forma inesperada {ds[var].shape}")
            ds.close()
            tmp.rename(out)
            return out
        except Exception as e:
            time.sleep(5 * (intento + 1))
    print("FALLÓ", modelo, esc, var, anio, file=sys.stderr)
    return None


def main(hilos=6):
    tareas = []
    for m in MODELOS:
        for esc, anios in ESCENARIOS.items():
            for v in VARS:
                cat = catalogo(m, esc, v)
                for a in anios:
                    if a in cat:
                        tareas.append((m, esc, v, a, cat[a]))
                    else:
                        print("no está en el catálogo:", m, esc, v, a, file=sys.stderr)
    pend = [t for t in tareas if not (CACHE / f"{t[0]}_{t[1]}_{t[2]}_{t[3]}.nc").exists()]
    print(f"{len(tareas)} archivos, {len(pend)} pendientes", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(hilos) as ex:
        for i, r in enumerate(ex.map(extraer, pend, chunksize=2), 1):
            if i % 25 == 0:
                print(f"{i}/{len(pend)}  {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    import os
    main(int(os.environ.get("NEX_PROCESOS", "6")))
