# CRC001: riesgo por olas de calor urbano en Montería, Córdoba, bajo escenarios de cambio climático

[![Made with MyST](https://img.shields.io/badge/made%20with-MyST-orange)](https://mystmd.org)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc001/main?filepath=article.ipynb)
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/scr-ungrd/cuadernos-reproducibles-crc001/blob/main/article.ipynb)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24309440.svg)](https://doi.org/10.5281/zenodo.24309440)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

> **Cuaderno reproducible de conocimiento del riesgo.**
> Subdirección para el Conocimiento del Riesgo (SCR), Unidad Nacional para la Gestión del Riesgo de Desastres (UNGRD), Colombia.

- **Sitio:** <https://scr-ungrd.github.io/cuadernos-reproducibles-crc001/>
- **Cuaderno:** [`article.ipynb`](article.ipynb), con las salidas guardadas.

## Qué hace

Evalúa cómo cambia el riesgo por calor urbano en **Montería** con datos abiertos reales y tres escenarios del CMIP6 (SSP2-4.5, SSP3-7.0 y SSP5-8.5). Este cuaderno reúne, en un solo análisis, la proyección del cambio climático, las olas de calor y el riesgo. Recorre seis fases:

1. **Amenaza climática:** estaciones del IDEAM (Aeropuerto Los Garzones e INCODER-AUT) y proyecciones NEX-GDDP-CMIP6 de cinco modelos; olas de calor por percentil local.
2. **Isla de calor urbana:** temperatura de superficie Landsat 8 y 9 a 30 m y cobertura ESA WorldCover.
3. **Estrés térmico:** Humidex observado con temperatura y humedad relativa de la estación.
4. **Exposición:** población WorldPop (100 m) e infraestructura de salud de OpenStreetMap.
5. **Vulnerabilidad (parcial):** arbolado y distancia a hospitales y clínicas; faltan edad y condiciones sociales.
6. **Riesgo relativo:** combina las fases 2, 4 y 5; ordena zonas y no estima pérdidas.

El alcance y las limitaciones de cada fase están en las secciones 1 y 12 del cuaderno.

## Estructura

| Ruta | Contenido |
|---|---|
| `article.ipynb` | Cuaderno principal (corre completo sin credenciales con los datos de `data/`) |
| `data/` | Series y rásteres recortados al área de estudio (unos 25 MB); `data/final/` guarda figuras y tablas |
| `scripts/` | Descarga y procesamiento desde las fuentes originales; `scripts/config.py` fija la ciudad |
| `metadata/` | Fuentes (`sources.csv`), catálogo y diccionario de datos, sumas SHA-256 (`descargas.csv`) y metadatos RDLS (`rdls/`) |
| `DATA_STATEMENT.md`, `CITATION.cff`, `CHANGELOG.md`, `AI_USE.md` | Disponibilidad de datos y de código, cita, historial de cambios y uso de IA |
| `SECURITY.md`, `metadata/escaneo_seguridad.md` | Política de seguridad y registro del escaneo previo al release |
| `references.bib` | Bibliografía |
| `_templates/plain-typst-article/` | Plantilla Typst del PDF |
| `myst.yml`, `.github/workflows/deploy.yml` | Sitio MyST y publicación en GitHub Pages |

## Ejecutar

```bash
conda env create -f environment.yml
conda activate crc001-calor-monteria
jupyter lab article.ipynb
```

El cuaderno corre completo y sin credenciales con los archivos de `data/`. Para regenerarlos desde las fuentes abiertas (la caché de descargas, `data/raw/`, no se versiona):

```bash
python scripts/descargar_observaciones.py      # IDEAM, Humidex y ERA5-Land
python scripts/extraer_nex_gddp.py             # NEX-GDDP-CMIP6 por OPeNDAP (tarda alrededor de una hora)
python scripts/procesar_nex.py                 # celda de la estación e índices de la ventana 3 por 3
python scripts/extraer_lst_landsat.py          # compuesto de LST de Landsat 8 y 9
python scripts/extraer_worldcover.py           # cobertura del suelo
python scripts/extraer_poblacion_worldpop.py   # población
python scripts/extraer_osm.py                  # hospitales, clínicas, hogares de mayores y colegios
```

`scripts/extraer_nex_gddp.py` y `scripts/descargar_observaciones.py` hacen reintentos, y el primero fuerza IPv4 porque el servidor THREDDS de la NASA no responde por IPv6.

## Cómo construir el sitio y el PDF

```bash
npm install -g mystmd
myst build --html      # sitio
myst build --typst     # PDF con la plantilla Typst (requiere Typst y la fuente Liberation Sans)
```

## Licencia

Texto y figuras bajo CC BY-SA 4.0 ([`LICENSE-CC-BY-SA-4.0`](LICENSE-CC-BY-SA-4.0)); código bajo licencia MIT ([`LICENSE`](LICENSE)). Los datos de `data/` conservan la licencia de su fuente, indicada por archivo en [`metadata/data_catalog.csv`](metadata/data_catalog.csv):

| Datos | Licencia |
|---|---|
| Derivados del IDEAM y de NEX-GDDP-CMIP6 | CC BY-SA 4.0 |
| Derivados de ERA5-Land, Landsat, WorldCover y WorldPop | CC BY 4.0 |
| Derivados de OpenStreetMap | ODbL 1.0 |

Las condiciones de cada fuente están en [`metadata/sources.csv`](metadata/sources.csv) y la declaración completa en [`DATA_STATEMENT.md`](DATA_STATEMENT.md).

## Cita y DOI

El DOI de todas las versiones es [10.5281/zenodo.20061609](https://doi.org/10.5281/zenodo.20061609). La versión actual es la v2.0.0 ([10.5281/zenodo.24309440](https://doi.org/10.5281/zenodo.24309440)); la v1.0.1 ([10.5281/zenodo.20061610](https://doi.org/10.5281/zenodo.20061610)) es anterior a la reescritura de noviembre de 2026. Los metadatos de cita están en [`CITATION.cff`](CITATION.cff).

## Uso de inteligencia artificial

El desarrollo de este repositorio contó con la asistencia de modelos de IA de la familia Claude (Sonnet 4.6, 5 y 5.5), según el historial de commits. El registro y la declaración están en [`AI_USE.md`](AI_USE.md).
