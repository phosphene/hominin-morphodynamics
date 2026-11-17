# Hominin Morphodynamics

Quantitative paleobiology, continuous morphological disparity, comparative vertebrate extinctability, and legible diversification mechanics for the hominin clade.

---

## 1. Epistemic Architecture & Separation Boundaries

The repository enforces strict separation between four sovereign scientific tiers (`docs/EPISTEMIC_TAXONOMY_AND_BOUNDARY_SEPARATION.md`):

1. **Tier 1: Forensic Auditing (`forensics/`, `docs/close-reads/`):** Epistemic stress-testing of third-party replication packages, identifying numerical singularities (e.g. division by 38-microsecond consensus polytomies) and ad-hoc taxon surgery without allowing defective foreign code patterns into the platform.
2. **Tier 2: Canonical Model Baselines (`src/hominin_morphodynamics/canonical/`):** Pure, unit-separated implementations of foundational physical models (Darwin 1881 topsoil accretion, Boudreau 1996 diagenetic biodiffusion, Etienne 2012 island master equation) run directly against primary historical ledgers.
3. **Tier 3: Curated Data Benches (`data/raw/`, `data/curated/`):** Three-layer non-destructive empirical data benches preserving immutable raw files (Layer 1), auditable stratigraphic rectification receipts (Layer 2), and spatial/temporal uncertainty envelopes (Layer 3).
4. **Tier 4: Native Forward Inference (`src/hominin_morphodynamics/morphometrics/`, `inference/`):** Continuous morphological variance on allometric residuals ($MD_W(t)$), sympatric mammalian extinctability baselines (*Theropithecus*, *Alcelaphini*, carnivore guild collapse), and bounded depositional basin kernels designed from first principles.

---

## 2. Core Methodological Standards

- **Mathematical Legibility (`docs/MATHEMATICAL_LEGIBILITY_AND_SELF_SUFFICIENT_UNITS_OF_REASON.md`):** Rejects computational "oracle patterns" where millions of MCMC steps obscure parameter degeneracies. Requires closed-form objective functions, strict dimensional accounting, deterministic profile likelihood evaluation, and the J.O. Wisdom "Caliper and Dirt" test.
- **Application of Proven Models (`docs/CANONICAL_ETIENNE_APPLICATION_TO_HOMININS.md`):** Rather than inheriting opaque birth-death tools, applies proven continuous-time master equations (Etienne 2012) directly to hominin branching times, demonstrating that carrying capacity $K$ is non-viable and unidentifiable ($\Delta \ln L \le 0.35$, $p = 0.61$).

---

## 3. Package Structure

- **`hominin_morphodynamics.schema`**: Specimen metadata, stratigraphic rectification, coupled horizon resampling, and Galápagos avifaunal schemas.
- **`hominin_morphodynamics.inference.master_equation`**: Canonical continuous-time master equation solver for diversity-dependent diversification under carrying capacity $K$.
- **`hominin_morphodynamics.inference.worm_models`**: Physical baseline engines reproducing Darwin (1881) earthworm topsoil accretion and Cambrian trace bioturbation indices.
- **`hominin_morphodynamics.inference.primitives`**: Dimensionally consistent primitives for spatial decay, temporal weighting, and tip diversification rates.
- **`hominin_morphodynamics.inference.diversity_surface`**: Deterministic profile likelihood optimizer for Poisson hazard processes.
- **`hominin_morphodynamics.evogeog`**: Dynamic Newick tree parsing, tip path extraction, and singularity diagnostics.

---

## 4. Verification

Run the complete test suite (all 44 unit tests):

```bash
uv run pytest
```
