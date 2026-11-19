# Política de seguridad

Este repositorio es un cuaderno reproducible de la Subdirección para el Conocimiento del Riesgo (UNGRD). No tiene servidores, cuentas de usuario ni credenciales, y todos sus datos son públicos. Aun así, cuida los riesgos propios de un repositorio abierto: secretos, datos personales, rutas locales, dependencias y automatización.

## Versiones compatibles

Se mantiene la última versión publicada en el [sitio](https://scr-ungrd.github.io/cuadernos-reproducibles-crc001/) y archivada en Zenodo (DOI [10.5281/zenodo.20061609](https://doi.org/10.5281/zenodo.20061609), que agrupa todas las versiones).

## Cómo reportar una vulnerabilidad o una filtración

Escriba a conocimiento@gestiondelriesgo.gov.co e indique el archivo, la línea y qué se expone. No publique el detalle en un *issue* ni en un *pull request*. Acusamos recibo y respondemos por el mismo medio.

## Si se filtra un secreto o un dato personal

1. Revocar o rotar la credencial en el proveedor. Borrar el archivo no basta.
2. Retirar el contenido del repositorio y, si el dato ya se archivó, pedir a Zenodo la retirada o la restricción del registro.
3. Avisar a las personas afectadas.
4. Registrar el incidente en [`CHANGELOG.md`](CHANGELOG.md).

## Controles que se aplican

- Escaneo de secretos del árbol y del historial antes de cada *release*, con el resultado archivado en [`metadata/escaneo_seguridad.md`](metadata/escaneo_seguridad.md).
- Dependencias con versión exacta en [`environment.yml`](environment.yml) y auditoría de vulnerabilidades con `pip-audit`.
- Sumas de verificación SHA-256 de los datos descargados en [`metadata/descargas.csv`](metadata/descargas.csv).
- Flujo de despliegue con permisos mínimos, y herramientas de compilación con versión fijada y suma de verificación.

Los requisitos completos están en [Requisitos de seguridad](https://scr-ungrd.github.io/cuadernos-reproducibles/requisitos-seguridad) de la colección.
