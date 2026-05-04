# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A reproducible research publication on La Palma 2021 seismicity, built with [MyST Markdown](https://mystmd.org/) and submitted to AGU's Notebooks Now! initiative. The output is a multi-format scientific article (HTML site, PDF via AGU LaTeX template, JATS, MECA).

## Environment Setup

```bash
conda env create -f environment.yml
conda activate lapalma-earthquakes
```

The conda environment (`lapalma-earthquakes`) includes JupyterLab ≥4 with the `jupyterlab-myst` extension.

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

2. **`notebooks/data-screening.ipynb`** — Loads raw IGN earthquake catalog from `data/lapalma_ign.csv`, filters to La Palma events (5,465 events), and outputs cleaned data used downstream.

3. **`notebooks/visualization-figure-creation-seaborn.ipynb`** — Generates static figures from the screened data using Seaborn/Matplotlib; figures are embedded into `article.ipynb`.

4. **`notebooks/seismic-monitoring.md`** — Static markdown chapter describing the 12-station monitoring network (no execution required).

The notebooks must be run in order (data-screening before visualization). `myst build` handles execution via Jupyter when building.

## Key Configuration

- **`myst.yml`** — Project metadata, export targets (AGU 2019 LaTeX template), site navigation, and resource declarations. Authors, affiliations, and DOI/ORCID metadata live here.
- **`_toc.yml`** — Chapter order for the built site.
- **`references.bib`** — BibTeX bibliography; inline DOI citations in notebooks use MyST's `{cite}` role.

## Data

`data/lapalma_ign.csv` is the primary dataset (IGN catalog, 11 Sep – 9 Nov 2021). Columns: `Event`, `Date`, `Time`, `Latitude`, `Longitude`, `Depth`, `Magnitude`, `Location`, `DateTime`, `Swarm`, `Phase`.
