# Epistemic Taxonomy & Boundary Separation Architecture: Forensics, Canonical Baselines, Curated Data Benches, and Forward Inference

**Coordinate:** `docs/EPISTEMIC_TAXONOMY_AND_BOUNDARY_SEPARATION.md`  
**Namespace:** `morphodynamics.architecture`  
**Authors:** Ed Phil, Jan (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Living Architectural Standard & Methodological Contract  
**Date:** 2026-11-17  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. The Architectural Mandate

In quantitative paleobiology and computational macroevolution, research environments frequently suffer from code rot and epistemic contamination caused by conflating distinct scientific activities:
1. **Auditing someone else's flawed replication code** is confused with building an inference engine.
2. **Reproducing a canonical mathematical baseline** is confused with raw empirical data ingestion.
3. **Ingesting empirical fossils** is confused with fitting an unverified macroevolutionary model.

When these activities are mixed in the same directory, foreign modeling defects (such as machine-epsilon branch singularities, ad-hoc exception drops, and circular taphonomic proxies) leak into forward research.

To enforce strict adherence to **Phosphene Axiomatic Standards** (Open-World Assumption, Logic/IO Separation, Positive Predication, ID-Path Parity), this document formalizes a sovereign, four-tier taxonomy and separation boundary.

---

## 2. The Four Sovereign Epistemic Tiers

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE FOUR EPISTEMIC TIERS                                        │
├───────────────────────┬────────────────────────────────────────────────────────────────────────┤
│ Tier 1: Forensics     │ Epistemic stress-testing & failure reproduction of published papers    │
│ Tier 2: Canonics      │ Pure, unit-separated physical implementations of classical baselines   │
│ Tier 3: Data Benches  │ High-integrity, layer-separated empirical records with provenance      │
│ Tier 4: Inference     │ Native, forward research engines and hypothesis testing                │
└───────────────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

### Tier 1: Forensic Auditing (`forensics/`)

- **Primary Objective:** Rigorous stress-testing, verification, and forensic deconstruction of published literature, external data packages, and third-party replication scripts.
- **Governing Practice:**
  1. **Line-by-line code audit:** Systematic inspection for mathematical singularities (e.g. inverted sub-picosecond consensus edges $l \approx 10^{-12}\text{ Myr}$ causing division by 38 microseconds).
  2. **Ad-hoc intervention detection:** Identifying silent data surgery, including manual taxon deletion (`drop.tip("Ardipithecus_ramidus")`), ad-hoc failed run slicing (`temporary <- addedbranches[-c(188, 761, 869, 943)]`), and LLM-assisted superficial smoothing.
  3. **Data hygiene verification:** Checking for stratigraphically inverted horizons, boundary leakage, and circular proxy definitions.
- **Architectural Isolation:**
  - Forensic audit code and external replication scripts **never** import from or export to native Tier 4 modeling packages.
  - Sourced external consensus trees, scripts, and logs reside strictly in isolated test fixtures or external data directories (`data/raw/`).
- **Required Deliverables:**
  - Structured Close Read dossiers (`CR-001` through `CR-00n`) adhering to the Phosphene Seme triadic format (`:seme/firstness`, `:pheme/secondness`, `:delome/thirdness`).
  - Forensic Finding briefs (e.g. `FINDING_001_VAN_HOLSTEIN_2024_FORENSIC_AUDIT.md`).
  - Failure-reproducing regression tests proving the exact mechanism of reported artifacts.

---

### Tier 2: Canonical Model Baselines (`canonical/`)

- **Primary Objective:** Pure, unit-separated reference implementations of foundational, classical scientific and mechanical models.
- **Governing Practice:**
  1. **Strict dimensional consistency:** Every single variable and constant has an explicit, physically meaningful unit ($\text{mass} \cdot \text{area}^{-1} \cdot \text{time}^{-1}$, $\text{individuals} \cdot \text{volume}^{-1}$, $\text{distance} \cdot \text{time}^{-1}$). Zero black-box dimensionless indices.
  2. **Primary ledger execution:** Executed directly from primary historical and experimental datasets (e.g. Darwin 1881 quadrat casting weights $\to$ bulk displacement $\to$ compaction factor $\to$ decadal accretion; Boudreau 1996 diagenetic porewater reaction-diffusion; MacArthur & Wilson 1967 island equilibrium).
  3. **Analytical transparency:** Closed-form solutions or fully transparent numerical solvers. Zero opaque MCMC loops whose convergence hides underlying parameter degeneracies.
- **Architectural Isolation:**
  - Serves as the ground truth calibration benchmark against which all downstream models are dimensionally and physically verified.
- **Required Deliverables:**
  - Immutable historical data structures (`DarwinWormExperiment`, `AncientBioturbationTier`).
  - Unit tests verifying exact reproduction of published physical ledgers within measurement rounding.

---

### Tier 3: Curated Data Benches (`data/curated/` & `data-bench/`)

- **Primary Objective:** High-integrity, model-agnostic empirical datasets that preserve raw observations and distinct geological uncertainty envelopes without imposing forward modeling assumptions.
- **Governing Practice (Three-Layer Architecture):**
  - **Layer 1 (Raw Ingest):** Immutable preservation of original source files with cryptographic SHA256 receipts. Zero in-place edits.
  - **Layer 2 (Non-Destructive Rectification):** Explicit, auditable transformation pipelines resolving physical defects (such as stratigraphically inverted horizons) without clobbering raw source tables. Every change is logged with an epistemic rationale and warrant citation.
  - **Layer 3 (Uncertainty Preservation):** Preserving spatial and temporal uncertainty envelopes (e.g. separating high-resolution basin tie-points from 40 Myr regional umbrella intervals; decoupling continuous literature osteometrics from Linnaean binning).
- **Architectural Isolation:**
  - Independent of any specific diversification, phylogenetic, or macroevolutionary hypothesis. Reusable across disparate research programs.

---

### Tier 4: Native Forward Inference (`inference/` & `morphodynamics/`)

- **Primary Objective:** Original, forward scientific modeling, continuous morphological disparity evaluation, and hypothesis testing designed from first principles.
- **Governing Practice:**
  1. **Continuous morphological variance:** Disparity tracked as continuous pairwise and centroid variance vectors ($MD_W(t)$) computed on allometric residuals of published osteometric/dental traits, weighted inversely by measurement error and taphonomic fragility.
  2. **Sympatric vertebrate extinctability baselines:** Benchmarking hominin lineage persistence and turnover against contemporary vertebrate clades sharing identical depositional basins (e.g. *Theropithecus*, *Alcelaphini*, carnivore guild collapse) using transparent survival and hazard functions.
  3. **Explicit spatial & environmental kernels:** Bounded spatial mechanics reflecting localized depositional basins (Turkana, Awash, Sterkfontein) rather than assuming panmictic continental carrying capacities.
  4. **Epistemic austerity:** Zero foreign code dependencies, zero inlined Newick literals, and zero imported proxy metrics from flawed literature.

---

## 3. Operational Invariants & Code Review Checklist

Before any PR or module is approved in the repository, it must be verified against this boundary matrix:

```text
[ ] INVARIANT 1: TIER SEPARATION
    Does the module strictly belong to exactly ONE tier?
    (Forensic scripts must not reside inside inference packages; inference must not import forensic scripts.)

[ ] INVARIANT 2: ZERO INLINED EXTERNAL ARTIFACTS
    Are external trees, raw tables, or third-party outputs loaded from external data fixtures 
    via dynamic parsers rather than inlined as source literals?

[ ] INVARIANT 3: DIMENSIONAL TRANSPARENCY
    Are all units explicit and physically verifiable? 
    (No unregularized denominators, no division by near-zero branch lengths, no arbitrary index scores.)

[ ] INVARIANT 4: LOGIC / IO SEPARATION
    Are numerical mathematical kernels pure functions with zero disk IO or console side effects?

[ ] INVARIANT 5: NON-DESTRUCTIVE PROVENANCE
    Are raw data files treated as immutable, with transformations explicitly recorded in Layer 2 receipts?
```

---

## 4. Repository Mapping

```text
work/flow/hominin-morphodynamics/
├── data/
│   ├── raw/                  <-- Tier 3 (Layer 1: Immutable raw data & benchmark fixtures)
│   └── curated/              <-- Tier 3 (Layer 2 & 3: Rectified schemas, uncertainty benches)
├── docs/
│   ├── close-reads/          <-- Tier 1 (Forensic Close Reads & Finding Dossiers)
│   └── architecture/         <-- Standards & Epistemic Contracts
├── src/hominin_morphodynamics/
│   ├── evogeog/              <-- Tier 1 / Tier 4 (Phylogenetic auditing & spatial metrics)
│   ├── canonical/            <-- Tier 2 (Darwin, Boudreau, MacArthur & Wilson baselines)
│   ├── morphometrics/        <-- Tier 4 (Continuous variance & allometric disparity)
│   ├── inference/            <-- Tier 4 (Native forward likelihood & survival models)
│   └── schema/               <-- Tier 3 (Typed schemas, rectification, coupled resampling)
└── tests/
    ├── forensics/            <-- Tier 1 failure reproduction & numerical tests
    ├── canonical/            <-- Tier 2 physical reproduction tests
    └── inference/            <-- Tier 4 native model unit tests
```
