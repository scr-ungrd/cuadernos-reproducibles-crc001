# Uso de inteligencia artificial

Registro de uso de IA de este repositorio, conforme a la sección «Uso de IA» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/uso-de-ia>).

## Declaración

El desarrollo de este cuaderno contó con la asistencia de modelos de IA de la familia Claude (Anthropic): Claude Sonnet 4.6, Claude Sonnet 5 y Claude Sonnet 5.5. El historial de git lo registra con la línea `Co-Authored-By` en 48 de 53 commits (HEAD `94566d5`, 2026-11-17); los 5 restantes, del 2026-05-03 al 2026-08-06, no llevan esa línea. Las instrucciones permanentes para el asistente están en [`CLAUDE.md`](CLAUDE.md).

- **Herramienta y versión:** Claude Sonnet 4.6, Claude Sonnet 5 y Claude Sonnet 5.5. Todas las sesiones se hicieron con Claude Code (interfaz de línea de comandos de Anthropic).
- **Fechas de uso:** del 2026-05-03 al 2026-11-17.
- **Para qué se usó:** el historial muestra cambios asistidos en el texto y el código del cuaderno, los scripts de descarga y procesamiento, la plantilla Typst del PDF, los flujos de integración continua y la configuración del sitio. Mauricio Romero Torres dirigió cada cambio y aprobó los resultados.
- **Revisión humana:** Mauricio Romero Torres ([ORCID 0000-0003-3282-0372](https://orcid.org/0000-0003-3282-0372)) revisó el cuaderno. La versión 2.0.0 se revisó y se publicó el 2026-11-16.
- **Datos enviados a la herramienta:** ninguno que no sea público. Los datos del repositorio son públicos y no contienen datos personales.
- **Prompts y salidas:** no se conservan los prompts de las sesiones; las instrucciones permanentes están en `CLAUDE.md`.

El cuaderno incluye un aviso de que no ha sido validado por una persona experta y de que no debe usarse para tomar decisiones.

## Registro de usos

Los usos se reconstruyen a partir del historial de git; cada fila agrupa los commits con rastro de IA por modelo.

| Periodo | Herramienta y versión | Commits | Archivos que tocan | Riesgo | Revisión humana |
|---|---|---|---|---|---|
| 2026-05-03 a 2026-06-29 | Claude Sonnet 4.6 | 14 | `article.ipynb`, `myst.yml`, `references.bib`, `environment.yml`, flujos de CI, imágenes, `CLAUDE.md` | ámbar | <completar> |
| 2026-07-11 | Claude Sonnet 5 | 3 | plantilla Typst, flujos de CI, `article.ipynb`, `myst.yml` | verde a ámbar | <completar> |
| 2026-11-15 a 2026-11-17 | Claude Sonnet 5.5 | 31 | `article.ipynb`, `scripts/`, `data/`, plantilla Typst, `myst.yml`, `README.md`, `references.bib`, `CLAUDE.md` | ámbar | <completar> |

**Usos del 2026-11-17.** Ese día Claude Code (Sonnet 5.5) redactó `MODEL_CARD.md`, escribió `scripts/validar_modelos.py` (sesgo de los modelos contra dos estaciones e hindcast del anclaje) y `scripts/probar_datos.py`, fijó las versiones de `environment.yml` tras una ejecución limpia y completó los vacíos de `metadata/sources.csv`. Estos cambios ya están en el historial (commits `edf193b`, `2619217` y `94566d5`). Es uso ámbar (código y texto de análisis). Las cifras de `metadata/validacion_modelos.md` salen del script a partir de `data/`; una persona debe verificarlas.

**Cambios posteriores sin commit.** A fecha 2026-11-19 el árbol de trabajo tiene cambios posteriores a `94566d5` que aún no están en el historial: `article.ipynb`, `myst.yml`, `CLAUDE.md`, la plantilla Typst (`_templates/plain-typst-article/`), `TITULO_BREVE.md` y `data/final/fig0_flujo.*`. Si se hicieron con asistencia de IA, se registrarán en la tabla al hacer el commit. <completar>

La categoría de riesgo sigue la clasificación de la sección «Uso de IA»: el código y el texto generados con asistencia son ámbar y exigen verificación humana y declaración.
