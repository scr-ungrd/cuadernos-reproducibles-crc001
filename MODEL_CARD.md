# Ficha del modelo: olas de calor urbano en Montería

Conforme al «Estándar de modelos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-modelos>). Describe los modelos de `article.ipynb`: no hay un modelo de aprendizaje automático; son proyecciones climáticas de terceros, indicadores estadísticos propios y un índice de riesgo relativo.

## 1. Propósito y uso previsto

- **Modelos.** (1) Proyecciones de Tmáx y Tmín de cinco modelos globales de NEX-GDDP-CMIP6 (ACCESS-CM2, MPI-ESM1-2-HR, MRI-ESM2-0, NorESM2-MM y CMCC-ESM2), con índices de olas de calor (TX90p, HWF, HWD, HWML) y días con Tmáx ≥ 37 °C anclados a la estación. (2) Un compuesto de LST de Landsat 8 y 9 (2018–2024). (3) El Humidex observado. (4) Un riesgo relativo: media geométrica de los rangos percentiles de la LST P90, la población y una vulnerabilidad parcial.
- **Versión:** 2.0.0 (2026-11-16; DOI 10.5281/zenodo.24309440). **Autoría:** Subdirección para el Conocimiento del Riesgo, UNGRD, y Mauricio Romero Torres. **Licencia:** código MIT; texto y figuras CC BY-SA 4.0.
- **Uso previsto:** caracterizar el calor extremo de Montería, su cambio proyectado por escenario y dónde se concentra el riesgo relativo dentro de la ciudad, con fines educativos y de método. Un modelo físico propio no es viable; se usan proyecciones globales ya reducidas de escala y estadísticos sencillos.
- **Usos no previstos:** estimar pérdidas o daños (no hay función de impacto de calor validada para Montería), definir alertas o refugios sin validación con la Subdirección de Manejo de Desastres, comparar barrios con los rectángulos del cuaderno (no son límites oficiales) y leer la LST como temperatura del aire.
- **Límites de validez:** Montería (recuadro 8,68° a 8,85° N y 75,95° a 75,80° O); proyecciones de 2021 a 2080 en SSP2-4.5, SSP3-7.0 y SSP5-8.5, siempre por separado; población de 2020; LST de las 10:30 de la mañana.
- **Revisión previa a una decisión:** una persona experta en riesgo climático y salud pública. La revisión la coordina Mauricio Romero Torres (SCR-UNGRD).

## 2. Datos del modelo

- **Observaciones:** estaciones del IDEAM Aeropuerto Los Garzones (2015–2026) e INCODER-AUT (2005–2017), con control de calidad documentado (descarta Tmín < 17 °C, rango diurno > 16 °C y Tmín > Tmáx); 22 % de los días de Los Garzones sin dato válido.
- **Forzamiento:** NEX-GDDP-CMIP6 (DOI 10.7917/OFSG3345), celda de 25 km; ERA5-Land solo como contraste; Landsat, ESA WorldCover 2021, WorldPop 2020 y OpenStreetMap. Todos abiertos, con licencia y metadatos en `metadata/` (`DATA_STATEMENT.md`).
- **Hoja de datos:** `metadata/sources.csv`, `metadata/data_catalog.csv` y `metadata/DATA_DICTIONARY.md`. Sin datos personales ni de comunidades.
- **Verdad de terreno:** la estación Los Garzones es la referencia de Tmáx y Tmín. Registra 1,7 °C más de Tmáx que INCODER-AUT, de modo que los niveles absolutos dependen del sitio de medición.
- **Sin partición entrenamiento/prueba:** no se entrena nada. La validación usa las estaciones como referencia (sección 4).
- **Eventos raros:** los días ≥ 37 °C varían entre 5 y 45 por año en la estación; la muestra es de una década.

## 3. Descripción del método

- **Olas de calor:** racha de al menos 3 días con Tmáx y Tmín sobre su percentil 90 del día del año (ventana de 5 días, referencia 1985–2014, por modelo). El sesgo sistemático de cada modelo se elimina de la comparación.
- **Días ≥ 37 °C anclados:** a cada día observado (2016–2025) se suma el cambio por cuantil que proyecta el modelo entre 2016–2025 y el periodo futuro; hereda la muestra y la variabilidad de la estación.
- **Parámetros:** percentil 90, ventana de 5 días, 3 días, referencia 1985–2014 y umbral de 37 °C/26 °C, tomados de la literatura (ETCCDI, Cantillo et al.) y del P90 de la estación; ninguno se ajusta con datos de prueba.
- **Modelos de terceros:** los cinco modelos de NEX-GDDP-CMIP6 (Thrasher et al., 2022), con las licencias de `sources.csv`; `xclim` (< 1) solo verifica el conteo de olas.
- **Riesgo relativo:** sigue el enfoque de la matriz de riesgo del Manual de CLIMAAX (nivel relativo al área), pero **no usa su código**: es una implementación propia.
- **Formato:** no hay pesos; los resultados son tablas y figuras.

## 4. Validación y desempeño

Los resultados completos están en [`metadata/validacion_modelos.md`](metadata/validacion_modelos.md), generados por `scripts/validar_modelos.py`.

- **Sesgo de los modelos contra la estación** (mediana de los cinco modelos): contra Los Garzones (2016–2025) la Tmáx queda 1,2 °C por debajo en promedio, 1,6 °C en la mediana y 1,7 °C en el P90; la Tmín tiene un sesgo de +0,2 °C en promedio. Contra INCODER-AUT (2005–2014, estación **independiente**, que no se usa para anclar nada) la Tmáx queda 1,9 °C por debajo en promedio y 1,8 °C en el P90, y la Tmín 0,6 °C por debajo. Por mes, el sesgo de la Tmáx en Los Garzones es mayor de noviembre a marzo (hasta −2,4 °C en febrero) y menor de mayo a septiembre (−0,5 a −1,0 °C); en INCODER-AUT va de −1,3 a −2,6 °C a lo largo del año.
- **Hindcast del método anclado** (días por año con Tmáx ≥ 37 °C): en la prueba mitad-contra-mitad de Los Garzones (anclaje 2016–2020, objetivo 2021–2025) se observaron 14 días por año, la climatología de los años de anclaje daba 34 y el modelo anclado 37 (19 a 46 según el modelo); en INCODER-AUT (2005–2009 → 2010–2014) se observaron 34 frente a 17 de la climatología y 19 del anclado. Con un año fuera, el error medio absoluto fue de 13,2 días por año con la climatología y 14,7 con el anclado en Los Garzones (8 años), y de 8,8 y 10,8 en INCODER-AUT (4 años); el modelo sin anclar tuvo 24,5 y 13,7. **El anclaje no mejora a la climatología simple, pero corrige el sesgo del modelo crudo.** Con cinco o diez años no se puede evaluar el cambio climático.
- **No hay validación independiente de las proyecciones futuras:** no existen observaciones del futuro. Tampoco de la LST contra la temperatura del aire, del Humidex en el trópico ni del riesgo relativo (no hay función de impacto validada).
- **Línea base:** climatología de los años de anclaje y modelo sin anclar (sección B de la validación). Con el método vigente de la colección no se comparó. *Back-testing* de olas de calor documentadas: no se hizo.
- **Casos de fallo conocidos:** el modelo subestima la Tmáx todo el año (más de noviembre a marzo en Los Garzones); un año seco o húmedo aislado no se reproduce (con un miembro por modelo); la celda de 25 km no resuelve diferencias dentro de la ciudad.
- **Revisión por una persona experta del dominio:** no se ha hecho.

## 5. Incertidumbre y sensibilidad

- **Fuentes de incertidumbre:** estructural (cinco modelos de un miembro cada uno; el rango entre modelos no es un intervalo de confianza), escenario (tres SSP, nunca promediados), observacional (estación de una década con vacíos, sesgo entre estaciones) y de método (definición de ola de calor, umbral).
- **Sensibilidad:** cinco variantes de la fórmula del riesgo (coincidencia del 20 % superior), la humedad constante del Humidex y la variante de solo Tmáx de la ola de calor. El rango entre modelos se reporta junto a la mediana en todas las tablas.
- No se entregan intervalos de confianza ni probabilidades.

## 6. Reproducibilidad

- **Entorno:** `environment.yml`, con Python 3.11 y versiones exactas. Verificado el 2026-11-17 en un clon limpio del repositorio con un entorno nuevo: `article.ipynb` corrió completo y sin errores en 79 s en un Apple M1 (CPU, sin GPU), y las 43 salidas de texto coinciden con las publicadas (solo cambia la ruta del directorio de trabajo). No se probó en Colab ni en Binder.
- **Aleatoriedad:** el análisis es determinista; no usa semillas.
- **Datos:** el cuaderno corre completo con `data/`; los scripts de `scripts/` los regeneran desde las fuentes (hasta una hora para NEX-GDDP-CMIP6). `metadata/descargas.csv` guarda las sumas SHA-256.
- **Pruebas:** el conteo de olas se verifica contra `xclim` en una serie de prueba; no hay pruebas automáticas más allá de esa.
- No hay registro de experimentos ni artefactos intermedios archivados.

## 7. Riesgos, sesgos y uso responsable

- **No hacer daño:** el cuaderno avisa que es un ejercicio sin validar. Un uso indebido sería leer el riesgo relativo como pérdida o como prioridad de inversión, o la LST como temperatura del aire. El riesgo relativo ordena zonas; no estima cuánto vale el riesgo.
- **Sesgos:** una sola estación y una sola celda para todo el municipio; la vulnerabilidad no incluye edad, salud ni vivienda; las categorías del Humidex se diseñaron para otro clima.
- **Comunidades:** no se usan datos de comunidades; los datos son climáticos y de población agregada por celda de 100 m.
- **Explicabilidad:** los índices y el riesgo relativo son fórmulas explícitas en el cuaderno.

## 8. Documentación y ciclo de vida

- `README.md`, `CHANGELOG.md` (versionado semántico), `CITATION.cff`, `DATA_STATEMENT.md` y `AI_USE.md`.
- **Obsolescencia:** se rehace cuando haya más estaciones y años, datos sociales por manzana o una función de impacto de calor, o cuando cambie NEX-GDDP-CMIP6. Decide Mauricio Romero Torres (SCR-UNGRD).
- **Uso de IA:** declarado en `AI_USE.md`.
- No se publica en un repositorio de modelos (no hay pesos).
