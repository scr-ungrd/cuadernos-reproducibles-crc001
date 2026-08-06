# Proyección de Temperatura en Montería, Córdoba bajo Escenarios de Cambio Climático

[![Made with MyST](https://img.shields.io/badge/made%20with-MyST-orange)](https://mystmd.org)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc001/main?filepath=article.ipynb)
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/scr-ungrd/cuadernos-reproducibles-crc001/blob/main/article.ipynb)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20061610.svg)](https://doi.org/10.5281/zenodo.20061610)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

> **Publicación Científica Reproducible**  
> **Subdirección para el Conocimiento del Riesgo (SCR)** — Unidad Nacional para la Gestión del Riesgo de Desastres (**UNGRD**), Colombia.  
> *Sometido a la iniciativa Notebooks Now! de la AGU (American Geophysical Union).*

---

## 📌 Resumen del Proyecto

Este repositorio contiene la publicación científica reproducible sobre la **proyección probabilística de temperatura media anual en Montería, Córdoba (Caribe colombiano)** para el periodo **2024–2074** bajo cuatro trayectorias representativas de concentración (**RCP 2.6, 4.5, 6.0 y 8.5**).

La metodología implementa la técnica de escalamiento por patrón de calentamiento (*pattern scaling*) sobre la plataforma de riesgo probabilístico **CLIMADA** (ETH Zurich), utilizando el ensamble de temperatura media global (GMST) consistente con CMIP5 (Jewson, 2021) y aplicando un factor de amplificación regional ($FAR = 1.05 \pm 0.10$) específico para el dominio Caribe (IPCC AR6).

---

## 🔑 Puntos Clave (*Key Points*)

1. **Calentamiento robusto bajo todos los escenarios:** Incluso bajo mitigación agresiva (RCP 2.6), la temperatura mediana asciende a 28.2 °C en 2074 (+0.7 °C sobre la línea base 1991–2020). Bajo RCP 8.5, supera los 30.2 °C (+2.7 °C).
2. **Altas temperaturas en RCP 8.5:** Bajo el escenario de altas emisiones, la temperatura mediana sobrepasa los 30 °C hacia el año 2074 en Montería.
3. **Aumento drástico de años cálidos extremos:** La frecuencia esperada de años que superan el percentil 95 climatológico (~28.8 °C) pasa del 5 % histórico a más del 90 % hacia 2070 en RCP 8.5.
4. **Divergencia post-2050:** Las trayectorias climáticas se separan marcadamente después de 2045, definiendo las próximas dos décadas como la ventana estratégica decisiva para la mitigación.
5. **Impactos multisectoriales en la GRD:** El calentamiento proyectado genera presiones críticas sobre la seguridad hídrica del río Sinú, la salud pública por estrés térmico sostenido y la productividad agropecuaria y ganadera de Córdoba.

---

## 🏷️ Palabras Clave (*Keywords*)

`Cambio climático` • `Proyección de temperatura` • `Montería` • `Córdoba` • `Caribe colombiano` • `Estrés térmico` • `CLIMADA` • `Gestión del riesgo de desastres`

---

## 📂 Estructura del Repositorio

```text
cuadernos-reproducibles-crc001/
├── article.ipynb                   # Cuaderno principal y manuscrito científico MyST
├── myst.yml                        # Configuración de metadatos, autores y exportaciones MyST
├── _toc.yml                        # Tabla de contenido para el sitio web
├── environment.yml                 # Especificación del entorno Conda
├── references.bib                  # Citas bibliográficas en formato BibTeX
├── notebooks/
│   └── data-screening-visualization.ipynb  # Análisis complementarios (GMST, FAR, ToE)
├── data/                           # Conjuntos de datos y catálogos de soporte
├── images/                         # Recursos gráficos y banners
├── _templates/                     # Plantillas Typst / LaTeX para generación de PDF
└── fig1_trayectorias.png ...       # Gráficos generados por los cuadernos
```

---

## 🚀 Ejecución e Instalación

### Opción 1: Ejecución en la Nube (Recomendado)
- **Google Colab:** Abrir [`article.ipynb` en Colab](https://colab.research.google.com/github/scr-ungrd/cuadernos-reproducibles-crc001/blob/main/article.ipynb) (Runtime CPU). La instalación inicial de CLIMADA requiere ~5–8 min.
- **MyBinder:** Ejecutar el entorno completo interactivo a través de [Binder](https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc001/main?filepath=article.ipynb).

### Opción 2: Entorno Local (Conda + MyST CLI)

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/scr-ungrd/cuadernos-reproducibles-crc001.git
   cd cuadernos-reproducibles-crc001
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   conda env create -f environment.yml
   conda activate lapalma-earthquakes
   ```

3. **Instalar MyST CLI (Node.js requerida):**
   ```bash
   npm install -g mystmd
   ```

---

## 🛠️ Comandos de Compilación (MyST Markdown)

- **Previsualizar sitio web localmente con live-reload:**
  ```bash
  myst start
  ```

- **Compilar únicamente el sitio HTML:**
  ```bash
  myst build --html
  ```

- **Compilar todas las exportaciones (PDF vía AGU LaTeX/Typst, JATS, MECA, HTML):**
  ```bash
  myst build --all
  ```

---

## 📄 Cita y Licencia

- **Soporte financiero:** Financiado por la *Alfred P. Sloan Foundation* a través de la iniciativa **Notebooks Now!** de la AGU.
- **Licencia del Contenido:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
- **Licencia del Código:** [MIT License](LICENSE)
- **DOI:** [10.5281/zenodo.20061610](https://doi.org/10.5281/zenodo.20061610)
