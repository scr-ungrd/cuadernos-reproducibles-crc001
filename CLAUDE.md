# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A reproducible research publication on temperature projections for Montería, Córdoba (Caribbean coast of Colombia) under climate change scenarios (RCP 2.6/4.5/6.0/8.5), built with [MyST Markdown](https://mystmd.org/) and submitted to AGU's Notebooks Now! initiative. The output is a multi-format scientific article (HTML site, PDF via AGU LaTeX template, JATS, MECA). Uses the CLIMADA probabilistic risk platform (ETH Zurich) with pattern-scaling methodology, horizon 2024–2074.

## Environment Setup

```bash
conda env create -f environment.yml
conda activate lapalma-earthquakes
```

The conda environment (`lapalma-earthquakes`) includes JupyterLab ≥4 with the `jupyterlab-myst` extension. The main analysis point is Montería (8.7479° N, 75.8814° W, 15 m a.s.l.), with T_base = 27.5 °C and regional amplification factor FAR = 1.05 (IPCC AR6 CAR domain).

## Build Commands

```bash
# Install MyST CLI (one-time)
npm install -g mystmd

# Build HTML site for local preview
myst build --html

# Build all export formats (PDF, JATS, MECA, TeX, HTML)
myst build --all

# Start local dev server with live reload
myst start
```

CI builds via GitHub Actions (`.github/workflows/deploy.yml`) on push to `main` and deploys HTML to GitHub Pages.

## Architecture

The publication follows a linear execution pipeline:

1. **`article.ipynb`** — Main scientific text (MyST markdown with frontmatter, as a Jupyter notebook). References figures produced by the notebooks using MyST cross-reference syntax (`{numref}`, `{cite}`).

2. **`notebooks/data-screening-visualization.ipynb`** — Three complementary analyses: (A) historical GMST context 1880–2100 with warming-rate trend, (B) FAR sensitivity analysis showing how regional amplification uncertainty propagates to projected temperatures, (C) Time of Emergence analysis determining when the warming signal robustly exceeds natural variability for each RCP.

`myst build` handles notebook execution via Jupyter when building.

## Key Configuration

- **`myst.yml`** — Project metadata, export targets (AGU 2019 LaTeX template), site navigation, and resource declarations. Authors, affiliations, and DOI/ORCID metadata live here.
- **`_toc.yml`** — Chapter order for the built site.
- **`references.bib`** — BibTeX bibliography; inline DOI citations in notebooks use MyST's `{cite}` role.

## Data

`data/lapalma_ign.csv` is a legacy dataset from the original La Palma template (not used by `article.ipynb`). The main article generates all data synthetically via CLIMADA's GMST ensemble (`get_gmst_info()`). The analysis point is Montería, Córdoba (Colombia).
