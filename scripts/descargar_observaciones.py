"""Descarga observaciones y reanálisis para Montería (sin credenciales).

1. IDEAM, estación Aeropuerto Los Garzones (0013035501): temperatura máxima y mínima del aire del conjunto abierto
   de datos.gov.co (ccvq-rp9s y afdg-3zpb), agregadas a diario. Serie 2015-2026.
2. IDEAM, misma estación: Humidex horario (temperatura sbwg-7ju4 y humedad relativa uext-mhny), máximo diario.
   El IDEAM cambió de sensor el 2023-09-11: temperatura 0068 -> 0071 y humedad 0027 -> 0028; se unen en la fecha del cambio.
3. IDEAM, estación INCODER-AUT (0013055040, 8,747 N; 75,914 O): temperatura máxima y mínima 2005-2017. Es una serie
   más larga y más cercana al casco urbano, solo como contraste.
4. ERA5-Land vía Open-Meteo (archive-api): tmax, tmin diarias y Humidex horario máximo, 1985-2024, solo como contraste.

Cada descarga verifica que el número de filas coincide con el conteo de la fuente. Después de regenerar los datos,
ejecute scripts/registrar_descargas.py para guardar las sumas de verificación en metadata/descargas.csv.

Salidas (data/): ideam_diario_los_garzones.csv, ideam_humidex_diario_los_garzones.csv, ideam_diario_incoder.csv,
era5land_diario_monteria.csv
"""
from pathlib import Path
import time
import numpy as np
import pandas as pd
import requests
from config import ESTACION, ESTACION_ANTIGUA, LAT, LON, USER_AGENT

RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "data"
OUT.mkdir(parents=True, exist_ok=True)
UMBRAL_TN_MIN = 17           # °C; una Tmín menor es implausible en Montería (incluye lecturas de 0 °C)
RANGO_DIURNO_MAX = 16        # °C; un rango diurno mayor indica un sensor defectuoso
MIN_OBS_DIA = 20             # lecturas con dato para aceptar el día (temperatura máxima y mínima)
CAMBIO_SENSOR = pd.Timestamp("2023-09-11")
URL = "https://www.datos.gov.co/resource/{}.json"


def _conteo(id_, estacion, sensor=None):
    """Número de filas que declara datos.gov.co para el mismo filtro (count(*))."""
    params = {"codigoestacion": estacion, "$select": "count(*)"}
    if sensor:
        params["codigosensor"] = sensor
    r = requests.get(URL.format(id_), params=params, timeout=300, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    return int(r.json()[0]["count"])


def _paginado(id_, estacion, sensor=None, pagina=25000):
    esperado = _conteo(id_, estacion, sensor)
    filas, desde = [], 0
    while True:
        params = {"codigoestacion": estacion, "$select": "fechaobservacion,valorobservado",
                  "$order": "fechaobservacion", "$limit": pagina, "$offset": desde}
        if sensor:
            params["codigosensor"] = sensor
        for intento in range(6):          # el servidor de datos.gov.co corta lecturas largas: se reintenta
            try:
                r = requests.get(URL.format(id_), params=params, timeout=300, headers={"User-Agent": USER_AGENT})
                r.raise_for_status()
                lote = r.json()
                break
            except (requests.exceptions.RequestException, ValueError):
                if intento == 5:
                    raise
                time.sleep(15 * (intento + 1))
        filas += lote
        if len(lote) < pagina:
            break
        desde += pagina
    if len(filas) != esperado:        # la fuente cambió durante la descarga o la paginación falló: se repite la ejecución
        raise RuntimeError(f"{id_}: se descargaron {len(filas)} filas y la fuente declara {esperado}")
    df = pd.DataFrame(filas)
    df["t"] = pd.to_datetime(df.fechaobservacion)
    df["v"] = df.valorobservado.astype(float)
    return df.set_index("t").v


def marcar_calidad(d):
    """Columna control_calidad: «ok» o «falla» en los días con Tmáx y Tmín. Falla si Tmín < 17 °C, el rango diurno supera
    16 °C o Tmín > Tmáx (los mismos criterios físicos de la sección 6.1 del cuaderno). Los valores no se modifican."""
    completo = d.tx.notna() & d.tn.notna()
    bueno = (d.tn >= UMBRAL_TN_MIN) & ((d.tx - d.tn) <= RANGO_DIURNO_MAX) & (d.tn <= d.tx)
    d["control_calidad"] = np.where(completo, np.where(bueno, "ok", "falla"), "")
    return d


def ideam(estacion, archivo):
    mx, mn = _paginado("ccvq-rp9s", estacion), _paginado("afdg-3zpb", estacion)
    d = pd.DataFrame({"tx": mx.resample("D").max(), "n_tx": mx.resample("D").count(),
                      "tn": mn.resample("D").min(), "n_tn": mn.resample("D").count()})
    d.loc[d.n_tx < MIN_OBS_DIA, "tx"] = np.nan
    d.loc[d.n_tn < MIN_OBS_DIA, "tn"] = np.nan
    d.index.name = "fecha"
    marcar_calidad(d)
    d.to_csv(OUT / archivo)
    return d


def ideam_humidex():
    """Humidex horario con temperatura (sbwg-7ju4) y humedad relativa (uext-mhny) de IDEAM, uniendo los sensores
    anterior y posterior al cambio del 2023-09-11 (el sensor 0027 pasa a reportar humedad del suelo)."""
    t = pd.concat([_paginado("sbwg-7ju4", ESTACION, "0068").loc[:CAMBIO_SENSOR],
                   _paginado("sbwg-7ju4", ESTACION, "0071").loc[CAMBIO_SENSOR:]])
    rh = pd.concat([_paginado("uext-mhny", ESTACION, "0027").loc[:CAMBIO_SENSOR],
                    _paginado("uext-mhny", ESTACION, "0028").loc[CAMBIO_SENSOR:]])
    t = t[~t.index.duplicated()].resample("h").mean()
    rh = rh[~rh.index.duplicated()].resample("h").mean()
    h = pd.DataFrame({"t": t, "rh": rh}).dropna()
    h = h[(h.rh > 5) & (h.rh <= 100) & (h.t > 10) & (h.t < 50)]
    a, b = 17.62, 243.12                                     # Magnus
    g = np.log(h.rh / 100) + a * h.t / (b + h.t)
    h["td"] = b * g / (a - g)
    h["hx"] = humidex(h.t, h.td)
    idx = h.groupby(h.index.date)["hx"].idxmax()
    d = h.resample("D").agg(hx_max=("hx", "max"), hx_mean=("hx", "mean"), n_horas=("hx", "count"))
    mx = pd.DataFrame({"t_hxmax": h.loc[idx.values, "t"].values, "rh_hxmax": h.loc[idx.values, "rh"].values},
                      index=pd.to_datetime(list(idx.index)))
    d = d.join(mx)
    d.loc[d.n_horas < 18, ["hx_max", "hx_mean", "t_hxmax", "rh_hxmax"]] = np.nan
    d.index.name = "fecha"
    d.to_csv(OUT / "ideam_humidex_diario_los_garzones.csv")
    return d


def humidex(t, td):
    e = 6.11 * np.exp(5417.7530 * (1 / 273.16 - 1 / (td + 273.15)))
    return t + 0.5555 * (e - 10.0)


def era5land():
    filas = []
    for anio in range(1985, 2025):
        for intento in range(5):
            r = requests.get("https://archive-api.open-meteo.com/v1/archive",
                             params={"latitude": LAT, "longitude": LON, "models": "era5_land",
                                     "start_date": f"{anio}-01-01", "end_date": f"{anio}-12-31",
                                     "hourly": "temperature_2m,dew_point_2m", "timezone": "America/Bogota"},
                             timeout=120)
            if r.status_code == 200:
                break
            time.sleep(20 * (intento + 1))
        r.raise_for_status()
        h = pd.DataFrame(r.json()["hourly"])
        h["time"] = pd.to_datetime(h["time"])
        h["hx"] = humidex(h.temperature_2m, h.dew_point_2m)
        h = h.set_index("time")
        g = h.resample("D").agg(tx=("temperature_2m", "max"), tn=("temperature_2m", "min"),
                                hx_max=("hx", "max"), hx_mean=("hx", "mean"))
        # Temperatura y punto de rocío a la hora del Humidex máximo (para el análisis de sensibilidad)
        idx = h.groupby(h.index.date)["hx"].idxmax()
        g["t_hxmax"] = h.loc[idx.values, "temperature_2m"].values
        g["td_hxmax"] = h.loc[idx.values, "dew_point_2m"].values
        filas.append(g)
        time.sleep(2)
    d = pd.concat(filas)
    d.index.name = "fecha"
    d.to_csv(OUT / "era5land_diario_monteria.csv")
    return d


if __name__ == "__main__":
    if not (OUT / "ideam_diario_los_garzones.csv").exists():
        print(ideam(ESTACION, "ideam_diario_los_garzones.csv").describe().round(1))
    if not (OUT / "ideam_diario_incoder.csv").exists():
        print(ideam(ESTACION_ANTIGUA, "ideam_diario_incoder.csv").describe().round(1))
    if not (OUT / "ideam_humidex_diario_los_garzones.csv").exists():
        print(ideam_humidex().describe().round(1))
    if not (OUT / "era5land_diario_monteria.csv").exists():
        print(era5land().describe().round(1))
