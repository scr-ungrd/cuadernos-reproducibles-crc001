"""Validación de la amenaza climática del CRC001: sesgo de los modelos contra dos estaciones e hindcast del anclaje.

Uso:  python scripts/validar_modelos.py
Salida: metadata/validacion_modelos.md (tablas) y metadata/validacion_modelos.csv (resultados por modelo).

Qué comprueba (solo con los archivos de `data/`):
  A. Sesgo de los cinco modelos de NEX-GDDP-CMIP6 contra la estación Los Garzones (2016–2025) y contra la estación
     INCODER-AUT (2005–2014, que no se usa para anclar nada), en media, cuantiles y por mes.
  B. Hindcast del método absoluto anclado (días con Tmáx ≥ 37 °C): se ancla con una mitad de los años y se predice la otra,
     y se compara con dos referencias simples: la climatología de los años de anclaje (sin modelo) y el modelo sin anclar.
No valida el cambio climático futuro: no hay observaciones del futuro.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
UMBRAL_TX = 37.0
QS = np.linspace(0.005, 0.995, 100)
MIN_DIAS_ANIO = 250   # un año de la estación entra en la comparación si tiene al menos estos días válidos


def cargar_estacion(nombre):
    d = pd.read_csv(DATA / f"ideam_diario_{nombre}.csv", parse_dates=["fecha"], index_col="fecha")
    # mismo control de calidad que el cuaderno: Tmín >= 17, rango diurno <= 16 y Tmín <= Tmáx
    qc = (d.tn >= 17) & ((d.tx - d.tn) <= 16) & (d.tn <= d.tx)
    d.loc[~qc, ["tx", "tn"]] = np.nan
    return d[["tx", "tn"]]


los_garzones, incoder = cargar_estacion("los_garzones"), cargar_estacion("incoder")
nex = xr.open_dataset(DATA / "nex_gddp_celda_estacion.nc")
MODELOS = [str(m) for m in nex.modelo.values]


def serie(modelo, var, esc="ssp245"):
    return nex.sel(modelo=modelo, escenario=esc)[var].to_series()


def sesgos(obs, periodo, var):
    """Sesgo medio, de la mediana y del P90, y estadístico KS de cada modelo contra la estación en el periodo."""
    o = obs.loc[periodo[0]:periodo[1], var].dropna()
    filas = []
    for m in MODELOS:
        s = serie(m, var).loc[periodo[0]:periodo[1]]
        s = s.reindex(o.index).dropna()
        oo = o.reindex(s.index)
        filas.append(dict(modelo=m, n_dias=len(oo), sesgo_media=s.mean() - oo.mean(), sesgo_p50=s.quantile(.5) - oo.quantile(.5),
                          sesgo_p90=s.quantile(.9) - oo.quantile(.9), ks=stats.ks_2samp(s.values, oo.values).statistic,
                          rmse_cuantiles=float(np.sqrt(np.mean((np.quantile(s, QS) - np.quantile(oo, QS)) ** 2)))))
    return pd.DataFrame(filas)


def sesgo_mensual(obs, periodo, var="tx"):
    o = obs.loc[periodo[0]:periodo[1], var].dropna()
    out = {}
    for m in MODELOS:
        s = serie(m, var).loc[periodo[0]:periodo[1]].reindex(o.index).dropna()
        d = s - o.reindex(s.index)
        out[m] = d.groupby(d.index.month).mean()
    return pd.DataFrame(out)


def frec_anclada(obs_ref, mod_ref, mod_fut, umbral=UMBRAL_TX):
    """Fracción de días con Tmáx >= umbral tras sumar a la serie observada el cambio por cuantil del modelo."""
    dq = np.quantile(mod_fut, QS) - np.quantile(mod_ref, QS)
    p = stats.rankdata(obs_ref) / (len(obs_ref) + 1)
    return float(np.mean(obs_ref + np.interp(p, QS, dq) >= umbral))


def hindcast(obs, var, anclaje, objetivo, umbral):
    """Ancla con los años `anclaje` y predice los `objetivo`; devuelve observado, climatología, modelo crudo y anclado por modelo."""
    oa = obs.loc[anclaje[0]:anclaje[1], var].dropna().values
    oo = obs.loc[objetivo[0]:objetivo[1], var].dropna().values
    fila = dict(observado=365 * np.mean(oo >= umbral), climatologia=365 * np.mean(oa >= umbral))
    for m in MODELOS:
        s = serie(m, var)
        ref, fut = s.loc[anclaje[0]:anclaje[1]].values, s.loc[objetivo[0]:objetivo[1]].values
        fila[f"crudo_{m}"] = 365 * np.mean(fut >= umbral)
        fila[f"anclado_{m}"] = 365 * frec_anclada(oa, ref, fut, umbral)
    return fila


def resumen_hindcast(f):
    cr = [f[f"crudo_{m}"] for m in MODELOS]
    an = [f[f"anclado_{m}"] for m in MODELOS]
    return f["observado"], f["climatologia"], float(np.median(cr)), float(np.median(an)), min(an), max(an)


L = []
csv_filas = []
L.append("# Validación de la amenaza climática del CRC001\n")
L.append("Generado por `scripts/validar_modelos.py` con los archivos de `data/`. Los cinco modelos de NEX-GDDP-CMIP6 se evalúan en la celda de 25 km de la estación; todos los valores son de Tmáx o Tmín diarias en °C.\n")

# ---------------- A. sesgo
L.append("## A. Sesgo de los modelos contra las estaciones\n")
for nombre, obs, per, texto in (("Los Garzones", los_garzones, ("2016", "2025"), "estación con la que se ancla el método absoluto (2016–2025, escenario SSP2-4.5 de cada modelo)"),
                                ("INCODER-AUT", incoder, ("2005", "2014"), "estación independiente: no se usa para anclar nada (2005–2014, periodo histórico de los modelos)")):
    L.append(f"### {nombre}: {texto}\n")
    for var, etq in (("tx", "Tmáx"), ("tn", "Tmín")):
        t = sesgos(obs, per, var)
        t.insert(0, "estacion", nombre); t.insert(1, "variable", var)
        csv_filas.append(t)
        L.append(f"**{etq}.** Sesgo = modelo − estación.\n")
        L.append("| Modelo | Días | Sesgo medio | Sesgo mediana | Sesgo P90 | KS | RMSE cuantiles |\n|---|---|---|---|---|---|---|")
        for _, r in t.iterrows():
            L.append(f"| {r.modelo} | {r.n_dias} | {r.sesgo_media:+.2f} | {r.sesgo_p50:+.2f} | {r.sesgo_p90:+.2f} | {r.ks:.2f} | {r.rmse_cuantiles:.2f} |")
        L.append(f"| **Mediana de los modelos** | | **{t.sesgo_media.median():+.2f}** | **{t.sesgo_p50.median():+.2f}** | **{t.sesgo_p90.median():+.2f}** | **{t.ks.median():.2f}** | **{t.rmse_cuantiles.median():.2f}** |\n")
    m = sesgo_mensual(obs, per, "tx")
    L.append("Sesgo medio de la Tmáx por mes (modelo − estación):\n")
    L.append("| Mes | " + " | ".join(MODELOS) + " | Mediana |\n|---|" + "---|" * (len(MODELOS) + 1))
    for mes in range(1, 13):
        L.append(f"| {mes} | " + " | ".join(f"{m.loc[mes, c]:+.1f}" for c in MODELOS) + f" | {m.loc[mes].median():+.1f} |")
    L.append("")
pd.concat(csv_filas).to_csv(RAIZ / "metadata" / "validacion_modelos.csv", index=False, float_format="%.3f")

# ---------------- B. hindcast
L.append("## B. Hindcast del método absoluto anclado (días por año con Tmáx ≥ 37 °C)\n")
L.append("Se ancla con unos años de la estación y se predice el resto. **Referencias simples:** *climatología* (la frecuencia de los años de anclaje, sin modelo) y *modelo crudo* (los días ≥ 37 °C del modelo, sin anclar). El modelo anclado solo aporta si se acerca más al observado que la climatología.\n")
casos = [("Los Garzones", los_garzones, ("2016", "2020"), ("2021", "2025")),
         ("INCODER-AUT", incoder, ("2005", "2009"), ("2010", "2014"))]
L.append("### B1. Mitad contra mitad\n")
L.append("| Estación | Anclaje → objetivo | Observado | Climatología | Modelo crudo (mediana) | Anclado (mediana) | Anclado [mín–máx] |\n|---|---|---|---|---|---|---|")
for nombre, obs, a, o in casos:
    f = hindcast(obs, "tx", a, o, UMBRAL_TX)
    ob, cl, cr, an, lo, hi = resumen_hindcast(f)
    L.append(f"| {nombre} | {a[0]}–{a[1]} → {o[0]}–{o[1]} | {ob:.0f} | {cl:.0f} | {cr:.0f} | {an:.0f} | {lo:.0f}–{hi:.0f} |")
    csv_filas.append(pd.DataFrame([dict(estacion=nombre, variable="hindcast_mitades", **{k: v for k, v in f.items()})]))
L.append("")

L.append("### B2. Un año fuera (Los Garzones y INCODER-AUT)\n")
L.append("Cada año con al menos 250 días válidos se predice anclando con los demás años de la estación.\n")
L.append("| Estación | Año | Observado | Climatología | Modelo crudo | Anclado (mediana) |\n|---|---|---|---|---|---|")
res = {}
for nombre, obs, per in (("Los Garzones", los_garzones, ("2016", "2025")), ("INCODER-AUT", incoder, ("2005", "2014"))):
    base = obs.loc[per[0]:per[1], "tx"].dropna()
    anios = [a for a in range(int(per[0]), int(per[1]) + 1) if (base.index.year == a).sum() >= MIN_DIAS_ANIO]
    filas = []
    for y in anios:
        oa = base[base.index.year != y].values
        oy = base[base.index.year == y].values
        cr_, an_ = [], []
        for m in MODELOS:
            s = serie(m, "tx").loc[per[0]:per[1]]
            ref, fut = s[s.index.year != y].values, s[s.index.year == y].values
            cr_.append(365 * np.mean(fut >= UMBRAL_TX)); an_.append(365 * frec_anclada(oa, ref, fut))
        fila = (y, 365 * np.mean(oy >= UMBRAL_TX), 365 * np.mean(oa >= UMBRAL_TX), float(np.median(cr_)), float(np.median(an_)))
        filas.append(fila)
        L.append(f"| {nombre} | {y} | {fila[1]:.0f} | {fila[2]:.0f} | {fila[3]:.0f} | {fila[4]:.0f} |")
    d = pd.DataFrame(filas, columns=["anio", "obs", "clim", "crudo", "anclado"])
    res[nombre] = d
L.append("")
L.append("**Error medio absoluto (días por año) y sesgo, un año fuera:**\n")
L.append("| Estación | Años | MAE climatología | MAE modelo crudo | MAE anclado | Sesgo climatología | Sesgo crudo | Sesgo anclado | Correlación anclado–observado |\n|---|---|---|---|---|---|---|---|---|")
for nombre, d in res.items():
    r = np.corrcoef(d.anclado, d.obs)[0, 1] if d.anclado.std() > 0 else float("nan")
    L.append(f"| {nombre} | {len(d)} | {np.mean(abs(d.clim - d.obs)):.1f} | {np.mean(abs(d.crudo - d.obs)):.1f} | {np.mean(abs(d.anclado - d.obs)):.1f} | "
             f"{np.mean(d.clim - d.obs):+.1f} | {np.mean(d.crudo - d.obs):+.1f} | {np.mean(d.anclado - d.obs):+.1f} | {r:+.2f} |")
    csv_filas.append(d.assign(estacion=nombre, variable="hindcast_un_anio_fuera"))
L.append("")
L.append("## Qué se puede y qué no se puede concluir\n")
L.append("- La sección A mide el **sesgo del clima de fondo** contra dos estaciones; la B mide si el **anclaje** mejora una predicción sencilla en periodos de pocos años.\n"
         "- Con un solo miembro por modelo, la variabilidad interanual de cada modelo no coincide con la observada: no se espera que un modelo acierte el año.\n"
         "- Cinco o diez años no permiten juzgar el **cambio climático** (unas décimas de grado frente a variaciones de decenas de días entre años). Estas pruebas no validan las proyecciones hacia 2040–2080: no hay observaciones del futuro.\n"
         "- Las estaciones tienen vacíos (22 % de los días de Los Garzones sin dato válido); los años con menos de 250 días válidos no entran en el un año fuera.\n"
         "- El riesgo relativo (fases 4 a 6), la LST y el Humidex no se validan aquí.\n")
(RAIZ / "metadata" / "validacion_modelos.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
