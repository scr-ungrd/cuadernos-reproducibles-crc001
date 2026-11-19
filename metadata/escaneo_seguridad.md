# Registro del escaneo de seguridad

Constancia del escaneo previo a un *release*, según los [Requisitos de seguridad](https://scr-ungrd.github.io/cuadernos-reproducibles/requisitos-seguridad) de la colección (REL-01). Se agrega una sección por cada escaneo.

## 2026-11-19

- **Estado revisado:** commit `94566d5` y los cambios sin commit de ese día.
- **Herramientas:** `gitleaks` 8.30.1 (descargada con la suma de verificación de su publicación) y `pip-audit` 2.10.1. La auditoría se ejecutó con el estándar de seguridad en modo estático más herramientas.

| Comprobación | Resultado |
|---|---|
| Secretos en todo el historial de git (`gitleaks git`) | Sin hallazgos |
| Secretos en el árbol de trabajo (`gitleaks dir`) | 2 hallazgos, ambos falsos positivos: código del tema en `_build/`, que no se versiona (`.gitignore`) |
| Vulnerabilidades de las 16 dependencias fijadas en `environment.yml` (`pip-audit --no-deps`) | Sin vulnerabilidades conocidas |
| Rutas locales en archivos versionados | Una en la salida de la celda 7 de `article.ipynb`: corregida |
| Metadatos de imágenes (EXIF, GPS, autoría) | Sin GPS ni autoría; solo la etiqueta `Software` de matplotlib |
| Binarios, macros y código remoto | Sin ejecutables ni archivos con macros; `curl` solo en el flujo de despliegue, ahora con suma de verificación |
| Datos personales | Ninguno en los archivos; los correos de autoría del historial siguen pendientes de decisión (FUG-04) |

**Limitaciones.** `pip-audit` se ejecutó con `--no-deps`, así que no cubre las dependencias indirectas. Los escaneos de patrones no detectan secretos de formato inusual. No se revisó la configuración de la cuenta de GitHub ni de Zenodo. Un rastro del historial con una ruta local de usuario permanece en un *diff* antiguo.
