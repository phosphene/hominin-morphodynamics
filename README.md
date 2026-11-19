# Hominin Morphodynamics

**A Sovereign Scientific Platform for Macroevolutionary Inference, Continuous Morphological Disparity, and Diversification Mechanics in the Hominin Clade.**

---

## 1. Dual Mandate & Epistemic Posture

This repository operates under an explicit scientific dual mandate:

1. **Supporting Explanatory Scale:** We respect and support the foundational human desire for large-scale explanatory storytelling in human origins and evolutionary biology. Large synthetic narratives inspire scientific inquiry and drive public engagement.
2. **Grounded Empirical Inference:** We maintain an unyielding, caliper-and-dirt commitment to what physical fossil specimens and stratigraphy can genuinely bear. We make epistemic boundaries visible: distinguishing where mathematical machinery has empirical traction from where it overreaches on sparse, fragmentary horizons.

### The Grounding Precedent: The Open Science Harness
Deep-time sediment mechanics, bioturbation physics, and historical paleontological baselines are established in our companion platform, `phosphene/public-science-harness` (`studies/cambrian-substrate`, `studies/darwin_cirripedia`):
- **Darwin's Earthworms (1881):** Topsoil accretion and preservation blanket deposition ($+Z$).
- **Cambrian Agronomic Revolution:** Downward sediment biodiffusion ($-Z$, BI 1 to 5).
- **Darwin's Cirripedia (1851):** 35 species across 10 Cretaceous stages, isolated plate taphonomy, and the Fitch cabinet empirical decoupling of taxonomic richness from standing biomass.

Building upon those physical substrate precedents, **this repository focuses strictly on macroevolutionary inference, diversification dynamics, and morphological disparity in the hominin clade.**

---

## 2. The Methodological Triad: Galápagos Baseline vs. Hominin Sparsity

To evaluate macroevolutionary models with inferential rigor, we avoid evaluating sparse hominin data in a theoretical vacuum. Instead, we follow a rigorous comparative calibration:

```
[Dense Insular Baseline]                 [Mathematical Precursor]               [Sparse Deep-Time Evaluation]
 Etienne et al. (2012)                     Master Equation Solver                  Van Holstein & Foley (2024)
 Galápagos Avifauna (DAISIE)      --->     Continuous-Time State   --->           17 Fragmentary Hominin Horizons
 N = 11 clades, complete sampling          Transitions P(n, m, t)                 Profile Likelihood: Flat (p >= 0.25)
 Carrying Capacity K Identifiable          Carrying Capacity K                    Diversity-Dependence Not Rejectable
```

### A. The Data-Rich Baseline: Etienne et al. (2012) Galápagos Avifauna
- **Implementation:** `src/hominin_morphodynamics/canonical/master_equation.py`
- **Tests:** `tests/inference/test_galapagos_etienne.py`
- **Method:** Continuous-time diversification master equation tracking colonization, anagenesis, cladogenesis, and extinction under carrying capacity $K$.
- **Why It Works Here:** The Galápagos avifauna represents an insular, completely sampled radiation with verified lineage branch lengths and zero taphonomic horizon distortion. Carrying capacity $K$ is numerically identifiable, and maximum likelihood estimates converge to stable finite optima ($K \approx 20$).

### B. The Sparse Deep-Time Evaluation: Van Holstein & Foley (2024) Audit
- **Implementation:** `src/hominin_morphodynamics/inference/diversity_surface.py`
- **Documentation:** `docs/CANONICAL_ETIENNE_APPLICATION_TO_HOMININS.md`, `docs/VAN_HOLSTEIN_FOLEY_2024_CLOSE_READ.md`
- **Finding:** Applying diversity-dependent diversification machinery to 17 fragmentary hominin fossil horizons across 6.0 Myr reveals a flat profile likelihood surface ($\Delta \ln L \le 0.35$). The likelihood ratio test fails to reject diversity-independence ($p \ge 0.25$). Running Bayesian MCMC on this surface merely samples the hyperpriors, mistaking posterior distributions for ecological carrying capacity.

### C. Precursor Deconstruction & Singularity Forensics
- **Precursor Models (`src/hominin_morphodynamics/inference/precursor_models.py`):** Deconstructing the theoretical lineage from MacArthur-Wilson (1963, 1967) island biogeography $\to$ Walker-Valentine (1984) marine invertebrate saturation $\to$ Etienne (2012) master equations $\to$ Silvestro (2014) PyRate, exposing four physical category errors when transferred to hominins:
  1. *Insular Spatial Coupling:* Hominins roamed an unmodeled, continuous continental African landmass, not an isolated oceanic archipelago.
  2. *Clade Monophyly:* Hominini is an arbitrary Linnaean sub-tribe embedded in a continuous mammalian herbivore-carnivore guild.
  3. *Taphonomic Stationarity:* Rift Valley preservation is highly episodic and facies-dependent, violating uniform fossilization assumptions.
  4. *Competitive Equivalence:* Tool-using, scavenging hominins occupied completely different ecological niches across time rather than competing symmetrically for a static carrying capacity.
- **Phylogenetic Singularity Forensics (`src/hominin_morphodynamics/evogeog/phylogenetic_dr.py`):** Uncovering internal branch lengths on consensus trees as short as $4.82 \times 10^{-12}\text{ Myr}$ (38 microseconds), which trigger $10^{11}$ Tip DR rate explosions in unregularized pipelines.

---

## 3. Repository Architecture & Sovereign Tiers

The codebase maintains clear separation across four sovereign scientific tiers (`docs/EPISTEMIC_TAXONOMY_AND_BOUNDARY_SEPARATION.md`):

```
hominin-morphodynamics/
├── src/hominin_morphodynamics/
│   ├── canonical/                     # Tier 2: Pure mathematical baselines
│   │   └── master_equation.py         # Etienne (2012) continuous-time master equation
│   ├── inference/                     # Tier 4: Native likelihood & disparity engines
│   │   ├── precursor_models.py        # MacArthur-Wilson -> Etienne -> PyRate decomposition
│   │   ├── diversity_surface.py       # Profile likelihood grids & LRT tests
│   │   ├── primitives.py              # Dimensionally consistent spatial/temporal primitives
│   │   └── joint_likelihood.py        # Conditioned likelihood estimators
│   ├── evogeog/                       # Phylogenetic parsing & singularity forensics
│   │   └── phylogenetic_dr.py         # Tree parsing, branch regularization, Tip DR
│   └── schema/                        # Tier 3: Rectified hominin specimen schemas
│       ├── specimens.py               # Immutable Linnaean and anatomical records
│       ├── paleodemes.py              # Spatiotemporal horizon clustering
│       └── rectification.py           # Invariant preservation and validation
├── data/
│   └── raw/                           # Curated, checksummed primary datasets
│       ├── galapagos_etienne_2012/    # Calibrating island avifauna matrices
│       └── van_holstein_2024/         # Ingested hominin time series & consensus trees
├── docs/                              # Literate specifications, audits, and close reads
│   ├── HYPOTHESIS_PATTERNS_AND_CALIBRATION.md
│   ├── CANONICAL_ETIENNE_APPLICATION_TO_HOMININS.md
│   ├── COMPARATIVE_PAPER_ETIENNE_VS_FOLEY.md
│   ├── PRECURSOR_MODELS_AND_THEORETICAL_DERIVATION.md
│   └── VAN_HOLSTEIN_FOLEY_2024_CLOSE_READ.md
└── tests/                             # 40/40 passing unit and property-based test suites
```

---

## 4. Verification & Testing

Every mathematical solver, likelihood surface, and data cleaning pipeline is continuously verified with deterministic unit and property-based tests (`pytest`, `hypothesis`):

```bash
# Run the complete test suite (40 tests)
uv run pytest

# Run the Galápagos Etienne baseline tests
uv run pytest tests/inference/test_galapagos_etienne.py

# Run the hominin profile likelihood evaluation
uv run pytest tests/inference/test_hominin_etienne_evaluation.py

# Run precursor model theoretical deconstruction tests
uv run pytest tests/inference/test_precursor_models.py
```

---

## 5. Methodological Lineage & References

- **Etienne, R. S., et al. (2012).** *A dynamic model of island biogeography with speciation and diversity-dependent diversification.* Evolution, 66(10), 3241–3253.
- **MacArthur, R. H., & Wilson, E. O. (1963, 1967).** *The Theory of Island Biogeography.* Princeton University Press.
- **Van Holstein, L. A., & Foley, R. A. (2024).** *Diversity-dependent speciation and extinction in hominins.* Nature Ecology & Evolution, 8, 990–999.
- **Walker, T. D., & Valentine, J. W. (1984).** *Equilibrium models of evolutionary species diversity and the number of living marine bivalve species.* The American Naturalist, 124(6), 887–899.
- **Silvestro, D., et al. (2014).** *PyRate: a new program to estimate speciation and extinction rates from incomplete fossil data.* Methods in Ecology and Evolution, 5(10), 1126–1131.
