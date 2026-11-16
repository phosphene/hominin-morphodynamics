# Hominin Morphodynamics

Quantitative paleobiology, geometric morphometrics, evolutionary geography, and taphonomically conditioned diversification inference for the hominin clade.

## Architecture

The package follows Robert Foley's evolutionary ecology and quantitative paleobiology constructs:

- **`hominin_morphodynamics.schema`** (Annotated Specimen and Paleodeme Layer): Formalizes osteological and paleoanthropological metadata—museum catalog IDs (KNM-ER, OH, AL, StW, SK, Dmanisi), 3D anatomical landmark coordinate spaces, taphonomic flags, stratigraphic horizons (`Strat_Max_MA`, `Strat_Min_MA`), and Foley's paleodeme and ecological grade labels (`Homo 1`, `Homo 2`, `Homo 3`).
- **`hominin_morphodynamics.morphometrics`** (Shape, Allometry, and Modularity): Generalized Procrustes Analysis (GPA) coordinates, allometric regressions against body mass and endocranial volume, and modularity indices testing cranial-postcranial covariance.
- **`hominin_morphodynamics.evogeog`** (Evolutionary Geography and Macroecology): Parameterizes Afrotropical habitat fragmentation, basin isolation, dispersal corridors, and phylogenetic comparative models (BM, OU, rate shifts).
- **`hominin_morphodynamics.inference`** (Scoped Hypothesis Testing): Bounds statistical conclusions to explicit falsification criteria, such as verifying whether shape variance within a fossil sample exceeds extant primate intraspecific baselines, and conditioning birth-death diversification against preservation gradients.

## Quickstart

```bash
uv run pytest
```
