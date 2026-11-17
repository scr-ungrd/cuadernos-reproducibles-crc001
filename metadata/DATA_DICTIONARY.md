# Diccionario de variables

Describe cada columna o banda de los archivos de `data/`. Los vacíos son valores faltantes y se dejan en blanco; no se usa `0` como marcador. Las fechas tienen el formato `AAAA-MM-DD` y las coordenadas están en grados decimales (WGS 84). Fuente de cada archivo: `metadata/sources.csv`. Procesamiento: `scripts/`.

## `ideam_diario_los_garzones.csv` e `ideam_diario_incoder.csv`

Una fila por día de una estación del IDEAM. Los valores salen de lecturas horarias de datos.gov.co.

| Columna | Descripción | Tipo | Unidad | Notas |
|---|---|---|---|---|
| `fecha` | Día de las lecturas, según `fechaobservacion` de la fuente | fecha | | |
| `tx` | Máximo diario de la serie «Temperatura máxima del aire» | decimal | °C | Vacío si `n_tx` es menor que 20 |
| `n_tx` | Número de lecturas con dato en el día para `tx` | entero | lecturas | En `ideam_diario_los_garzones.csv` se guarda como decimal por la presencia de vacíos |
| `tn` | Mínimo diario de la serie «Temperatura mínima del aire» | decimal | °C | Vacío si `n_tn` es menor que 20 |
| `n_tn` | Número de lecturas con dato en el día para `tn` | entero | lecturas | |

Vacíos: en Los Garzones, `tx` 20,5 % y `tn` 16,3 %; en INCODER-AUT, `tx` 25,6 % y `tn` 28,5 %. Cobertura: Los Garzones del 2015-05-30 al 2026-11-13; INCODER-AUT del 2005-01-21 al 2017-05-02.

## `ideam_humidex_diario_los_garzones.csv`

Una fila por día de la estación Los Garzones (0013035501). El Humidex horario se calcula con la temperatura (`sbwg-7ju4`) y la humedad relativa (`uext-mhny`) y el punto de rocío con la aproximación de Magnus. El IDEAM cambió de sensor el 2023-09-11 (temperatura: 0068 a 0071; humedad: 0027 a 0028) y las series se unen en esa fecha.

| Columna | Descripción | Tipo | Unidad | Notas |
|---|---|---|---|---|
| `fecha` | Día | fecha | | |
| `hx_max` | Máximo diario del Humidex horario | decimal | índice Humidex | Vacío si `n_horas` es menor que 18 |
| `hx_mean` | Media diaria del Humidex horario | decimal | índice Humidex | Vacío si `n_horas` es menor que 18 |
| `n_horas` | Horas con dato válido en el día | entero | horas | Una hora es válida con humedad entre 5 % y 100 % y temperatura entre 10 y 50 °C |
| `t_hxmax` | Temperatura del aire a la hora del Humidex máximo | decimal | °C | Vacío con `hx_max` |
| `rh_hxmax` | Humedad relativa a la hora del Humidex máximo | decimal | % | Vacío con `hx_max` |

Vacíos: 29,5 % de los días en las cuatro columnas calculadas.

## `era5land_diario_monteria.csv`

Una fila por día del 1985-01-01 al 2024-12-31 en el punto 8,826 N y 75,825 O, desde ERA5-Land por la API de archivo de Open-Meteo. Solo contraste; no tiene vacíos.

| Columna | Descripción | Tipo | Unidad |
|---|---|---|---|
| `fecha` | Día (zona horaria America/Bogota) | fecha | |
| `tx` | Máximo diario de la temperatura a 2 m | decimal | °C |
| `tn` | Mínimo diario de la temperatura a 2 m | decimal | °C |
| `hx_max` | Máximo diario del Humidex horario | decimal | índice Humidex |
| `hx_mean` | Media diaria del Humidex horario | decimal | índice Humidex |
| `t_hxmax` | Temperatura a la hora del Humidex máximo | decimal | °C |
| `td_hxmax` | Punto de rocío a la hora del Humidex máximo | decimal | °C |

## `nex_gddp_celdas_3x3_anual.csv`

Una fila por modelo, escenario, año y celda de la ventana de 3 por 3 celdas de NEX-GDDP-CMIP6 (0,25 grados) alrededor de Montería. Cada año de 1985 a 2014 pertenece al periodo histórico y se repite en cada escenario.

| Columna | Descripción | Tipo | Unidad | Valores |
|---|---|---|---|---|
| `modelo` | Modelo climático | texto | | ACCESS-CM2, MPI-ESM1-2-HR, MRI-ESM2-0, NorESM2-MM, CMCC-ESM2 |
| `escenario` | Escenario de emisiones | texto | | ssp245, ssp370, ssp585 |
| `anio` | Año | entero | | 1985 a 2080 |
| `lat` | Latitud del centro de la celda | decimal | grados | 8,625; 8,875; 9,125 |
| `lon` | Longitud del centro de la celda | decimal | grados | de -76,125 a -75,625 |
| `tx_medio` | Media anual de la temperatura máxima diaria | decimal | °C | |
| `tn_medio` | Media anual de la temperatura mínima diaria | decimal | °C | |
| `p_tx90` | Fracción de días del año con la temperatura máxima por encima de su percentil 90 de 1985–2014, propio de cada celda y modelo | decimal | fracción de 0 a 1 | |

## `nex_gddp_celda_estacion.nc`

Series diarias de la celda de NEX-GDDP-CMIP6 que contiene a la estación Los Garzones (8,875 N; 75,875 O), de 1985-01-01 a 2080-12-31.

| Elemento | Descripción | Unidad |
|---|---|---|
| Dimensión `modelo` | 5 modelos (los mismos del CSV) | |
| Dimensión `escenario` | ssp245, ssp370 y ssp585 | |
| Dimensión `time` | 35 064 días del calendario gregoriano | |
| Variable `tx` | Temperatura máxima diaria | °C |
| Variable `tn` | Temperatura mínima diaria | °C |

## `lst_monteria_2018_2024.tif`

Compuesto de temperatura de superficie (LST) de Landsat 8 y 9 en WGS 84 / UTM zona 18N, 30 m. Las imágenes se toman hacia las 10:30 hora local; es LST diurna de la mañana. Se usa la banda térmica `lwir11` con máscara de nubes, sombras y cirros, y nubosidad de escena inferior a 40 %.

| Banda | Descripción | Unidad |
|---|---|---|
| 1 | Media de todas las fechas | K |
| 2 | Percentil 90 de todas las fechas | K |
| 3 | Número de fechas válidas | fechas |
| 4 | Media de la época seca (diciembre a marzo) | K |
| 5 | Percentil 90 de la época seca | K |
| 6 | Número de fechas válidas de la época seca | fechas |

## `worldcover_monteria_2021.tif`

Fracción de cada clase de ESA WorldCover 2021 (10 m) dentro de cada celda de 30 m, en WGS 84 / UTM zona 18N, en la misma rejilla que el compuesto de LST.

| Banda | Descripción | Unidad |
|---|---|---|
| 1 | Construido (clase 50) | fracción de 0 a 1 |
| 2 | Árboles (clase 10) | fracción de 0 a 1 |
| 3 | Agua (clase 80) | fracción de 0 a 1 |
| 4 | Manglar (clase 95) | fracción de 0 a 1 |
| 5 | Otra vegetación: arbustos, pastizal, cultivos y humedal herbáceo (clases 20, 30, 40 y 90) | fracción de 0 a 1 |

## `worldpop_monteria_2020.tif`

Una banda con la población estimada por celda de 100 m (WorldPop 2020, restringida a edificaciones, BSGM) en WGS 84, recortada al área de estudio. Unidad: personas por celda.

## `osm_infraestructura_monteria.csv`

Una fila por elemento de OpenStreetMap dentro del área de estudio (204 filas).

| Columna | Descripción | Tipo | Valores |
|---|---|---|---|
| `tipo` | Tipo de infraestructura | texto | `school` (169), `clinic` (28), `hospital` (5), `social_facility` (2) |
| `nombre` | Nombre del elemento en OpenStreetMap | texto | Vacío en 6,4 % de las filas; son nombres de instituciones |
| `lat` | Latitud | decimal | grados |
| `lon` | Longitud | decimal | grados |
