# Historial de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [2.0.0] - 2026-11-16

### Agregado
- Carpeta `metadata/`: `sources.csv`, `data_catalog.csv`, `DATA_DICTIONARY.md`, `descargas.csv` (sumas SHA-256) y 8 archivos RDLS 1.0.0 en `metadata/rdls/`.
- `DATA_STATEMENT.md`, `CITATION.cff`, `AI_USE.md` y este historial.
- `scripts/registrar_descargas.py`.
- Columna `control_calidad` (`ok`/`falla`) en `ideam_diario_los_garzones.csv` e `ideam_diario_incoder.csv`: marca los días con `tn` < 17 °C, rango diurno > 16 °C o `tn` > `tx`. Los valores no cambian.

### Cambiado
- El cuaderno se reescribió con datos reales de seis fases (commit `d3993d5`, 2026-11-15): estaciones del IDEAM, NEX-GDDP-CMIP6, Landsat, WorldCover, WorldPop y OpenStreetMap.

### Corregido
- Respuestas CARE (sin territorios étnicos) y compromiso de conservación de cinco años en `DATA_STATEMENT.md`; persona revisora en `AI_USE.md`.
- ORCID de Mauricio Romero Torres en `CITATION.cff`.
- Licencia de ERA5-Land: Copernicus pasó a CC BY 4.0 el 2025-07-02; se aclaró que la restricción de uso no comercial es de la API de Open-Meteo, no de los datos.

### Pendiente
- Actualizar `DATA_STATEMENT.md`, el README y el `id` de los archivos RDLS con el DOI de la versión 2.0.0 una vez archivada en Zenodo.
- Confirmar los marcadores de `AI_USE.md` (interfaz usada, fecha de ejecución en entorno limpio, datos enviados).

## [1.0.1] - 2026-05-06

- Versión archivada en Zenodo (`10.5281/zenodo.20061610`). Es anterior a la reescritura de noviembre de 2026.

## [1.0.0] - 2026-05-06

- Primera versión etiquetada.
