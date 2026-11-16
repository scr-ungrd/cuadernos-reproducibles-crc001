# CLAUDE.md

Guía para Claude Code (claude.ai/code) en este repositorio.

## Proyecto

Cuaderno reproducible CRC001: riesgo por olas de calor urbano en Montería (Córdoba) bajo escenarios de cambio climático, con datos abiertos reales. Se escribe en MyST (`article.ipynb`) y se publica como sitio HTML y como PDF (plantilla Typst propia). Reúne la proyección climática, las olas de calor y el riesgo en un solo análisis, en seis fases (amenaza climática, isla de calor urbana, estrés térmico, exposición, vulnerabilidad parcial y riesgo relativo).

## Entorno

```bash
conda env create -f environment.yml && conda activate crc001-calor-monteria
```

Usar `xclim<1`: la versión 1.0 retiró `xclim.indices`.

## Construcción

```bash
myst build --html      # sitio
myst build --typst     # PDF (article.pdf)
```

Requiere mystmd >= 1.13 y Node >= 22. El sitio fija la plantilla `article-theme` en la v1.4.1 (la v2 rompe el build con `BASE_URL`).

## Arquitectura

- `article.ipynb`: texto y código. Corre completo con los archivos de `data/`; `jupyter: false` en `myst.yml`, así que el sitio usa las salidas guardadas (hay que ejecutar el cuaderno y guardarlas antes del commit).
- `scripts/`: descarga y procesamiento de datos; `scripts/config.py` fija la ciudad, la estación, el recuadro y las celdas de NEX-GDDP. La caché `data/raw/` no se versiona (en esta máquina es un enlace a `~/.cache/crc001/raw`).
- `_templates/plain-typst-article/`: plantilla del PDF (`style.typ`, `template.typ`, `subpar-wrap.typ`). El identificador de la portada (CRC001) sale del nombre del repositorio en `myst.yml`.

## Convenciones del cuaderno

- Cada bloque de código lleva antes un párrafo que lo presenta y termina con «(ver código en la versión web)»; las celdas de código llevan la etiqueta `hide-input` (se pliegan en la web y se ocultan en el PDF).
- Toda tabla y figura se cita en el texto (`{numref}`) y tiene leyenda; las tablas de DataFrame se incrustan con una celda auxiliar `remove-cell` + `remove-input` dentro de `{table}`.
- Los escenarios SSP nunca se promedian; SSP2-4.5 es el principal, SSP3-7.0 el intermedio y SSP5-8.5 la prueba de estrés.
- Los datos crudos del IDEAM no se modifican: el control de calidad se hace en el cuaderno y se documenta.

## Datos

Estaciones IDEAM (Aeropuerto Los Garzones 0013035501 y INCODER-AUT 0013055040), NEX-GDDP-CMIP6 (5 modelos, 3 escenarios), ERA5-Land (solo contraste), Landsat 8 y 9, ESA WorldCover, WorldPop y OpenStreetMap. Todo es abierto y no requiere credenciales.
