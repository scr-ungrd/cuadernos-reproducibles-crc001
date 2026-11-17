# Declaración de disponibilidad de datos y de código

Cuaderno CRC001: riesgo por olas de calor urbano en Montería, Córdoba, bajo escenarios de cambio climático. Conforme al «Estándar de datos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-de-datos>).

## Datos de entrada

Las 10 fuentes, con su dirección exacta, versión o consulta, licencia y restricciones, están en [`metadata/sources.csv`](metadata/sources.csv). Todas se obtienen sin credenciales y sin pago con los scripts de `scripts/`.

- **IDEAM** (datos.gov.co): `ccvq-rp9s`, `afdg-3zpb`, `sbwg-7ju4` y `uext-mhny`, filtrados por las estaciones 0013035501 y 0013055040. CC BY-SA 4.0. El portal actualiza estos conjuntos en el origen: los archivos de `data/` corresponden a la descarga del 2026-11-15, con datos hasta el 2026-11-13. Las sumas de verificación están en [`metadata/descargas.csv`](metadata/descargas.csv).
- **NEX-GDDP-CMIP6** (NASA, `10.7917/OFSG3345`): CC BY-SA 4.0.
- **ERA5-Land** por la API de archivo de Open-Meteo: CC BY 4.0. Copernicus cambió la licencia de ERA5-Land a CC BY 4.0 el 2025-07-02 ([aviso de ECMWF](https://forum.ecmwf.int/t/cc-by-licence-to-replace-licence-to-use-copernicus-products-on-02-july-2025/13464)). El uso gratuito de la API de Open-Meteo es solo no comercial ([términos](https://open-meteo.com/en/terms)); es una condición del servicio y no de la licencia de los datos. La UNGRD la usa sin fines comerciales.
- **Landsat Collection 2 Level-2** (USGS, vía Planetary Computer): dominio público.
- **ESA WorldCover 2021** (`10.5281/zenodo.7254221`): CC BY 4.0.
- **WorldPop 2020 Colombia, restringido a edificaciones** (`10.5258/SOTON/WP00684`): CC BY 4.0.
- **OpenStreetMap** (Overpass): ODbL 1.0.

## Datos derivados publicados

Los 10 archivos de `data/` están descritos en [`metadata/data_catalog.csv`](metadata/data_catalog.csv), sus variables en [`metadata/DATA_DICTIONARY.md`](metadata/DATA_DICTIONARY.md) y sus metadatos RDLS 1.0.0 en [`metadata/rdls/`](metadata/rdls/).

| Datos | Licencia |
|---|---|
| Derivados del IDEAM y de NEX-GDDP-CMIP6 | CC BY-SA 4.0 |
| Derivados de ERA5-Land, Landsat, WorldCover y WorldPop | CC BY 4.0 |
| Derivados de OpenStreetMap | ODbL 1.0 |

**DOI.** El DOI de todas las versiones es [`10.5281/zenodo.20061609`](https://doi.org/10.5281/zenodo.20061609). La versión actual es la v2.0.0 ([`10.5281/zenodo.24309440`](https://doi.org/10.5281/zenodo.24309440), 2026-11-16); la v1.0.1 ([`10.5281/zenodo.20061610`](https://doi.org/10.5281/zenodo.20061610), 2026-05-06) es anterior a la reescritura de noviembre de 2026. Los identificadores `id` de los archivos RDLS usan el DOI de la v2.0.0.

## Datos con acceso restringido

Ninguno.

## Revisión CARE

- Los datos son observaciones meteorológicas, proyecciones climáticas, rásteres de cobertura, temperatura y población, y puntos de infraestructura. No contienen datos personales: los nombres de `osm_infraestructura_monteria.csv` son de instituciones.
- No contienen conocimiento local ni tradicional sobre amenazas.
- ¿El área de estudio incluye territorios, resguardos o consejos comunitarios de pueblos étnicos? No. Autorización: «No aplica».

## Disponibilidad de código

- Repositorio: <https://github.com/scr-ungrd/cuadernos-reproducibles-crc001>. Licencia MIT.
- Versión archivada con DOI: v1.0.1. Falta un *release* del estado actual.
- Software: [`environment.yml`](environment.yml).
- El código no tiene componentes aleatorios.

## Validación técnica y limitaciones

- Comprobaciones: depuración de las series del IDEAM con tres criterios físicos (sección 6.1 del cuaderno); las series publicadas traen la columna `control_calidad` que marca los días que fallan y verificación del conteo de olas de calor contra `xclim.heat_wave_frequency` (secciones 4.3 y 6.2).
- Limitaciones introducidas por el análisis y heredadas de las fuentes: sección 12.1 del cuaderno.
- Este cuaderno es un ejercicio sin validar por una persona experta; no debe usarse para tomar decisiones (aviso al inicio del cuaderno).

## Compromiso de preservación

- Responsable: Subdirección para el Conocimiento del Riesgo, UNGRD (conocimiento@gestiondelriesgo.gov.co).
- Los datos se conservarán al menos cinco años después de la publicación.
