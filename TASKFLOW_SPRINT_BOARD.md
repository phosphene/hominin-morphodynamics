---
uri: work/flow/hominin-morphodynamics/TASKFLOW_SPRINT_BOARD.md
owner: edphos
title: TaskFlow Sprint Board — Etienne Archipelago vs. Foley Hominin PyRate
status: in-progress
track: hominin-morphodynamics.paper-sprint
created: 2026-11-17
updated: 2026-11-17
---

# TASKFLOW_SPRINT_BOARD.md

Sprint board tracking the implementation of the canonical Etienne (2012) / Valente et al. (2015) Galápagos empirical dataset and master equation solver, rigorous comparative testing against Foley & Van Holstein (2024), and synthesis into a publication-ready comparative paper.

---

## Sprint Overview

| ID | Module / Track | Type | Pri | Title | Owner | Status |
|---|---|---|---|---|---|---|
| **TF-ETI-001** | `data/raw/galapagos_valente_2015` | data | high | Ingest canonical Galápagos avifauna dataset & seal SHA-256 provenance | edphos + flow | closed |
| **TF-ETI-002** | `schema/galapagos.py` | schema | high | Typed dataclasses for Galápagos insular colonization and branching events | edphos + flow | closed |
| **TF-ETI-003** | `inference/master_equation.py` | feature | high | Continuous-time master equation solver & profile likelihood for Etienne DDD | edphos + flow | closed |
| **TF-ETI-004** | `tests/inference/test_galapagos_etienne.py` | test | high | Comprehensive unit, property, and convergence test suite for Galápagos | edphos + flow | closed |
| **TF-ETI-005** | `inference/comparative_metrics.py` | feature | high | Cross-domain metric extractor (Archipelago vs. Continental Taphonomy) | edphos + flow | closed |
| **TF-ETI-006** | `docs/COMPARATIVE_PAPER_ETIENNE_VS_FOLEY.md` | docs/paper | high | Full comparative scientific monograph & paper draft | edphos + flow | closed |

---

## Detailed Task Specifications

### TF-ETI-001: Ingest Canonical Galápagos Avifauna Dataset
- **Coordinate:** `data/raw/galapagos_valente_2015/`
- **Objective:** Ingest the canonical Valente, Phillimore, & Etienne (2015, *Ecology Letters*) Galápagos terrestrial avifauna dataset (including Darwin's finches branching times and independent colonization clades) in native format and cryptographic SHA-256 seal.
- **Invariants:** Byte-sealed in `DATA_INVENTORY_AND_PROVENANCE.md`.

### TF-ETI-002: Typed Dataclasses for Insular Colonization & Branching
- **Coordinate:** `src/hominin_morphodynamics/schema/galapagos.py`
- **Objective:** Provide immutable schemas (`GalapagosClade`, `GalapagosDataset`, `ColonistStatus`) preserving clade names, colonization status (Endemic, Non_endemic, etc.), missing species counts, and stem/crown branching times.
- **Invariants:** Zero loss of precision; complete type safety; integration with `hominin_morphodynamics.schema`.

### TF-ETI-003: Continuous-Time Master Equation Solver for Etienne DDD
- **Coordinate:** `src/hominin_morphodynamics/inference/master_equation.py`
- **Objective:** Implement the exact discrete master equation forward transition operator ($P(n, t)$) with matrix exponentiation and Runge-Kutta Cash-Karp integration, supporting linear diversity-dependent speciation ($\lambda(n) = \max(0, \lambda_0(1 - n/K))$), conditioning on crown/stem age and non-extinction, and carrying capacity profile likelihood evaluation.
- **Invariants:** Numerical log-space stability; handles $K \ge S$; strict bounds checking.

### TF-ETI-004: Comprehensive Test Suite for Galápagos Etienne Solver
- **Coordinate:** `tests/inference/test_galapagos_etienne.py`
- **Objective:** Unit tests verifying likelihood values against known analytical baselines, property sweeps verifying monotonic penalties as $K < S$, and profile likelihood optimization recovering carrying capacity $K$ on Darwin's finches.
- **Invariants:** Fast execution (<3s); 100% green with `uv run pytest`.

### TF-ETI-005: Cross-Domain Comparative Metric Extractor
- **Coordinate:** `src/hominin_morphodynamics/inference/comparative_metrics.py`
- **Objective:** Unified framework computing spatial coupling index, trophic guild overlap, profile likelihood curvature around $K$, and LRT statistic against density-independent null across both domains (Galápagos Finches vs. Hominins).
- **Invariants:** Deterministic; exports structured JSON summary.

### TF-ETI-006: Comparative Scientific Monograph & Paper Draft
- **Coordinate:** `docs/COMPARATIVE_PAPER_ETIENNE_VS_FOLEY.md`
- **Objective:** Comprehensive scientific paper analyzing Foley & Van Holstein (2024) alongside Etienne et al. (2012) / Valente et al. (2015). Demonstrates when interspecies competition models work (Galápagos) vs. why they break on continental taphonomy (Hominins), supported by empirical code, likelihood profiles, and taphonomic geometry.
