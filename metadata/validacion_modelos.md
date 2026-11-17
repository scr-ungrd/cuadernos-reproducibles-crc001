# Validación de la amenaza climática del CRC001

Generado por `scripts/validar_modelos.py` con los archivos de `data/`. Los cinco modelos de NEX-GDDP-CMIP6 se evalúan en la celda de 25 km de la estación; todos los valores son de Tmáx o Tmín diarias en °C.

## A. Sesgo de los modelos contra las estaciones

### Los Garzones: estación con la que se ancla el método absoluto (2016–2025, escenario SSP2-4.5 de cada modelo)

**Tmáx.** Sesgo = modelo − estación.

| Modelo | Días | Sesgo medio | Sesgo mediana | Sesgo P90 | KS | RMSE cuantiles |
|---|---|---|---|---|---|---|
| ACCESS-CM2 | 2929 | -0.98 | -1.37 | -1.61 | 0.33 | 1.28 |
| MPI-ESM1-2-HR | 2929 | -1.22 | -1.57 | -1.68 | 0.35 | 1.41 |
| MRI-ESM2-0 | 2929 | -1.37 | -1.75 | -2.09 | 0.40 | 1.60 |
| NorESM2-MM | 2929 | -1.08 | -1.41 | -1.64 | 0.32 | 1.31 |
| CMCC-ESM2 | 2929 | -1.34 | -1.73 | -2.01 | 0.38 | 1.57 |
| **Mediana de los modelos** | | **-1.22** | **-1.57** | **-1.68** | **0.35** | **1.41** |

**Tmín.** Sesgo = modelo − estación.

| Modelo | Días | Sesgo medio | Sesgo mediana | Sesgo P90 | KS | RMSE cuantiles |
|---|---|---|---|---|---|---|
| ACCESS-CM2 | 2929 | +0.51 | +0.19 | -0.36 | 0.18 | 1.00 |
| MPI-ESM1-2-HR | 2929 | +0.24 | +0.07 | -0.24 | 0.09 | 0.49 |
| MRI-ESM2-0 | 2929 | +0.13 | -0.13 | -0.70 | 0.16 | 0.73 |
| NorESM2-MM | 2929 | +0.25 | +0.03 | -0.44 | 0.11 | 0.59 |
| CMCC-ESM2 | 2929 | -0.16 | -0.32 | -0.89 | 0.19 | 0.59 |
| **Mediana de los modelos** | | **+0.24** | **+0.03** | **-0.44** | **0.16** | **0.59** |

Sesgo medio de la Tmáx por mes (modelo − estación):

| Mes | ACCESS-CM2 | MPI-ESM1-2-HR | MRI-ESM2-0 | NorESM2-MM | CMCC-ESM2 | Mediana |
|---|---|---|---|---|---|---|
| 1 | -1.2 | -1.6 | -1.6 | -1.5 | -2.0 | -1.6 |
| 2 | -2.0 | -2.4 | -2.4 | -2.2 | -2.4 | -2.4 |
| 3 | -1.1 | -1.4 | -2.0 | -1.6 | -1.8 | -1.6 |
| 4 | -0.9 | -1.1 | -1.0 | -0.8 | -1.0 | -1.0 |
| 5 | -0.5 | -0.7 | -1.0 | -0.4 | -1.0 | -0.7 |
| 6 | -0.2 | -0.5 | -0.8 | -0.5 | -0.6 | -0.5 |
| 7 | -0.3 | -0.5 | -0.5 | -0.4 | -0.6 | -0.5 |
| 8 | -0.7 | -0.9 | -1.4 | -0.6 | -1.1 | -0.9 |
| 9 | -0.7 | -1.1 | -1.2 | -0.7 | -1.0 | -1.0 |
| 10 | -1.1 | -1.4 | -1.4 | -1.2 | -1.4 | -1.4 |
| 11 | -1.4 | -1.4 | -1.4 | -1.6 | -1.6 | -1.4 |
| 12 | -1.9 | -1.8 | -1.9 | -1.6 | -1.8 | -1.8 |

### INCODER-AUT: estación independiente: no se usa para anclar nada (2005–2014, periodo histórico de los modelos)

**Tmáx.** Sesgo = modelo − estación.

| Modelo | Días | Sesgo medio | Sesgo mediana | Sesgo P90 | KS | RMSE cuantiles |
|---|---|---|---|---|---|---|
| ACCESS-CM2 | 2317 | -1.91 | -2.25 | -1.94 | 0.54 | 2.01 |
| MPI-ESM1-2-HR | 2317 | -1.59 | -2.07 | -1.07 | 0.45 | 1.76 |
| MRI-ESM2-0 | 2317 | -1.77 | -2.22 | -1.55 | 0.50 | 1.90 |
| NorESM2-MM | 2317 | -2.47 | -2.77 | -2.79 | 0.66 | 2.56 |
| CMCC-ESM2 | 2317 | -1.94 | -2.35 | -1.79 | 0.53 | 2.06 |
| **Mediana de los modelos** | | **-1.91** | **-2.25** | **-1.79** | **0.53** | **2.01** |

**Tmín.** Sesgo = modelo − estación.

| Modelo | Días | Sesgo medio | Sesgo mediana | Sesgo P90 | KS | RMSE cuantiles |
|---|---|---|---|---|---|---|
| ACCESS-CM2 | 2317 | -0.55 | -0.54 | -0.66 | 0.23 | 0.56 |
| MPI-ESM1-2-HR | 2317 | -0.15 | -0.11 | +0.03 | 0.07 | 0.51 |
| MRI-ESM2-0 | 2317 | -0.68 | -0.66 | -0.78 | 0.31 | 0.73 |
| NorESM2-MM | 2317 | -0.88 | -0.82 | -0.94 | 0.34 | 0.93 |
| CMCC-ESM2 | 2317 | -0.61 | -0.54 | -0.64 | 0.25 | 0.65 |
| **Mediana de los modelos** | | **-0.61** | **-0.54** | **-0.66** | **0.25** | **0.65** |

Sesgo medio de la Tmáx por mes (modelo − estación):

| Mes | ACCESS-CM2 | MPI-ESM1-2-HR | MRI-ESM2-0 | NorESM2-MM | CMCC-ESM2 | Mediana |
|---|---|---|---|---|---|---|
| 1 | -2.7 | -1.5 | -2.0 | -3.3 | -2.6 | -2.6 |
| 2 | -2.9 | -1.9 | -2.0 | -3.1 | -2.2 | -2.2 |
| 3 | -2.0 | -1.0 | -1.2 | -3.0 | -1.3 | -1.3 |
| 4 | -1.4 | -0.8 | -0.7 | -2.1 | -1.4 | -1.4 |
| 5 | -1.3 | -1.6 | -1.3 | -2.1 | -1.6 | -1.6 |
| 6 | -1.5 | -1.6 | -2.1 | -2.2 | -1.7 | -1.7 |
| 7 | -1.6 | -1.2 | -1.5 | -2.1 | -1.8 | -1.6 |
| 8 | -1.4 | -1.0 | -1.5 | -2.0 | -1.6 | -1.5 |
| 9 | -2.1 | -2.0 | -2.4 | -2.6 | -2.5 | -2.4 |
| 10 | -2.3 | -2.0 | -2.4 | -2.5 | -2.1 | -2.3 |
| 11 | -2.1 | -2.5 | -1.7 | -2.7 | -2.2 | -2.2 |
| 12 | -2.2 | -2.0 | -2.2 | -2.4 | -2.3 | -2.2 |

## B. Hindcast del método absoluto anclado (días por año con Tmáx ≥ 37 °C)

Se ancla con unos años de la estación y se predice el resto. **Referencias simples:** *climatología* (la frecuencia de los años de anclaje, sin modelo) y *modelo crudo* (los días ≥ 37 °C del modelo, sin anclar). El modelo anclado solo aporta si se acerca más al observado que la climatología.

### B1. Mitad contra mitad

| Estación | Anclaje → objetivo | Observado | Climatología | Modelo crudo (mediana) | Anclado (mediana) | Anclado [mín–máx] |
|---|---|---|---|---|---|---|
| Los Garzones | 2016–2020 → 2021–2025 | 14 | 34 | 5 | 37 | 19–46 |
| INCODER-AUT | 2005–2009 → 2010–2014 | 34 | 17 | 6 | 19 | 0–45 |

### B2. Un año fuera (Los Garzones y INCODER-AUT)

Cada año con al menos 250 días válidos se predice anclando con los demás años de la estación.

| Estación | Año | Observado | Climatología | Modelo crudo | Anclado (mediana) |
|---|---|---|---|---|---|
| Los Garzones | 2016 | 46 | 22 | 0 | 20 |
| Los Garzones | 2017 | 40 | 23 | 11 | 37 |
| Los Garzones | 2018 | 35 | 24 | 3 | 20 |
| Los Garzones | 2020 | 37 | 23 | 3 | 9 |
| Los Garzones | 2021 | 20 | 25 | 5 | 24 |
| Los Garzones | 2023 | 6 | 27 | 8 | 29 |
| Los Garzones | 2024 | 22 | 25 | 2 | 14 |
| Los Garzones | 2025 | 17 | 26 | 1 | 8 |
| INCODER-AUT | 2006 | 21 | 23 | 3 | 16 |
| INCODER-AUT | 2007 | 21 | 24 | 4 | 30 |
| INCODER-AUT | 2008 | 5 | 26 | 10 | 19 |
| INCODER-AUT | 2009 | 16 | 24 | 1 | 1 |

**Error medio absoluto (días por año) y sesgo, un año fuera:**

| Estación | Años | MAE climatología | MAE modelo crudo | MAE anclado | Sesgo climatología | Sesgo crudo | Sesgo anclado | Correlación anclado–observado |
|---|---|---|---|---|---|---|---|---|
| Los Garzones | 8 | 13.2 | 24.5 | 14.7 | -3.6 | -23.9 | -7.8 | +0.04 |
| INCODER-AUT | 4 | 8.8 | 13.7 | 10.8 | +8.8 | -11.1 | +0.6 | +0.13 |

## Qué se puede y qué no se puede concluir

- La sección A mide el **sesgo del clima de fondo** contra dos estaciones; la B mide si el **anclaje** mejora una predicción sencilla en periodos de pocos años.
- Con un solo miembro por modelo, la variabilidad interanual de cada modelo no coincide con la observada: no se espera que un modelo acierte el año.
- Cinco o diez años no permiten juzgar el **cambio climático** (unas décimas de grado frente a variaciones de decenas de días entre años). Estas pruebas no validan las proyecciones hacia 2040–2080: no hay observaciones del futuro.
- Las estaciones tienen vacíos (22 % de los días de Los Garzones sin dato válido); los años con menos de 250 días válidos no entran en el un año fuera.
- El riesgo relativo (fases 4 a 6), la LST y el Humidex no se validan aquí.
