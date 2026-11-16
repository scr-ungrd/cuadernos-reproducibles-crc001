"""Ensambla las series de NEX-GDDP-CMIP6 bajadas por extraer_nex_gddp.py.

Salidas (en data/):
  nex_gddp_celda_estacion.nc     tx, tn diarios (°C) de la celda que contiene a la estación Los Garzones (8,875 N; 75,875 O),
                                 dims (modelo, escenario, time), 1985-2080 (histórico 1985-2014 + SSP 2015-2080)
  nex_gddp_celdas_3x3_anual.csv  por modelo, escenario, año y celda de la ventana 3x3: tx medio, tn medio y
                                 fracción de días con TX > TX90 de la referencia 1985-2014 (propia de cada celda y modelo)
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import xarray as xr

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / "data" / "raw" / "nex"
MODELOS = ["ACCESS-CM2", "MPI-ESM1-2-HR", "MRI-ESM2-0", "NorESM2-MM", "CMCC-ESM2"]
ESC = ["ssp245", "ssp370", "ssp585"]
FECHAS = pd.date_range("1985-01-01", "2080-12-31", freq="D")


def serie(modelo, esc, var):
    """DataArray (time, lat, lon) en °C, histórico + escenario, sobre el calendario gregoriano completo."""
    trozos = []
    for nombre, anios in (("historical", range(1985, 2015)), (esc, range(2015, 2081))):
        for a in anios:
            f = CACHE / f"{modelo}_{nombre}_{var}_{a}.nc"
            if not f.exists():
                return None
            da = xr.open_dataset(f)[var]
            # El calendario se reconstruye desde el año del archivo: algunos archivos llegan con el tiempo sin
            # decodificar y varios modelos usan calendario de 365 días (sin 29 de febrero)
            dias = pd.date_range(f"{a}-01-01", f"{a}-12-31")
            if da.sizes["time"] != len(dias):
                dias = dias[~((dias.month == 2) & (dias.day == 29))]
            da["time"] = dias
            trozos.append(da)
    da = xr.concat(trozos, dim="time") - 273.15
    da = da.reindex(time=FECHAS)
    return da.ffill("time", limit=1)      # 29 de febrero ausente en calendarios de 365 días


def tx90_doy(da, ini="1985", fin="2014", ventana=5, q=0.9):
    ref = da.sel(time=slice(ini, fin))
    doy = ref.time.dt.dayofyear.clip(max=365)
    out = np.empty((366,) + da.shape[1:], dtype="float32")
    for d in range(1, 367):
        vecinos = [(d - 1 + k) % 365 + 1 for k in range(-(ventana // 2), ventana // 2 + 1)]
        out[d - 1] = np.nanquantile(ref.values[np.isin(doy.values, vecinos)], q, axis=0)
    return out


def main(modelos=None):
    modelos = modelos or MODELOS
    centrales, filas = {}, []
    for m in modelos:
        for esc in ESC:
            tx, tn = serie(m, esc, "tasmax"), serie(m, esc, "tasmin")
            if tx is None or tn is None:
                print("faltan datos de", m, esc)
                continue
            centrales[(m, esc)] = (tx.isel(lat=1, lon=1).values, tn.isel(lat=1, lon=1).values)
            umbral = tx90_doy(tx)
            doy = np.minimum(tx.time.dt.dayofyear.values, 366) - 1
            exced = np.where(np.isnan(tx.values), np.nan, (tx.values > umbral[doy])).astype("float32")  # celdas de mar: NaN
            anio = tx.time.dt.year.values
            for a in np.unique(anio):
                s = anio == a
                for i, lat in enumerate(tx.lat.values):
                    for j, lon in enumerate(tx.lon.values):
                        filas.append((m, esc, int(a), float(lat), float(lon - 360),
                                      float(tx.values[s, i, j].mean()), float(tn.values[s, i, j].mean()),
                                      float(exced[s, i, j].mean())))
            print("ok", m, esc, flush=True)
    mods = sorted({k[0] for k in centrales}, key=MODELOS.index)
    tx = np.full((len(mods), len(ESC), len(FECHAS)), np.nan, "float32")
    tn = tx.copy()
    for (m, esc), (a, b) in centrales.items():
        tx[mods.index(m), ESC.index(esc)], tn[mods.index(m), ESC.index(esc)] = a, b
    ds = xr.Dataset({"tx": (("modelo", "escenario", "time"), tx), "tn": (("modelo", "escenario", "time"), tn)},
                    coords={"modelo": mods, "escenario": ESC, "time": FECHAS})
    ds.attrs = {"fuente": "NEX-GDDP-CMIP6 (NASA), celda de 0,25 grados que contiene a 8,826 N, 75,825 O (Aeropuerto Los Garzones)",
                "unidades": "grados Celsius"}
    ds.to_netcdf(RAIZ / "data" / "nex_gddp_celda_estacion.nc",
                 encoding={v: {"zlib": True, "complevel": 5, "dtype": "float32"} for v in ("tx", "tn")})
    pd.DataFrame(filas, columns=["modelo", "escenario", "anio", "lat", "lon", "tx_medio", "tn_medio", "p_tx90"]
                 ).round(4).to_csv(RAIZ / "data" / "nex_gddp_celdas_3x3_anual.csv", index=False)
    print("listo:", mods)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
