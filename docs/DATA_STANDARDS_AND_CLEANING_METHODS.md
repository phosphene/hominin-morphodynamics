# Data Standards, Cleaning Methods & Ingestion Hygiene

**Document Coordinate:** `docs/DATA_STANDARDS_AND_CLEANING_METHODS.md`  
**Repository:** `phosphene/hominin-morphodynamics`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Platform Standard & Methodological Rehearsal  
**Date:** 2026-11-16  

---

## 1. Foundational Epistemic Philosophy

This repository practices **hermetic self-sufficiency**: every standard, methodological defense, and data hygiene rule required to ensure scientific reproducibility must be defined, rehearsed, and tested within this repository's own boundaries.

Our data cleaning and integrity framework synthesizes principles from David Mertz's *Cleaning Data for Effective Data Science* (Packt, 2021), adapted to the specific evidentiary demands of quantitative paleoanthropology and hominin evolutionary ecology:

* **Universal Dirtiness (Imbesi's Law):** All empirical datasets contain defects within some margin of error. In paleoanthropology, this includes disputed bed dates, stratigraphically conflated cave deposits, disparate taxonomic synonymies, and uncalibrated radiocarbon or argon dates. Cleaning does not manufacture certainty; it isolates, bounds, and documents defects so models test empirical reality rather than software or transcription artifacts.
* **Data Quality vs. Data Utility:** Quality (internal structural and numerical consistency) and utility (fitness for resolving a specific evolutionary question) are orthogonal. A spreadsheet can be structurally intact but scientifically vacuous due to severe taphonomic or collection bias (e.g., 60% of all occurrences coming from three late Pleistocene taxa). Conversely, a table with missing subsite coordinates remains useful if its bed boundaries and museum catalog numbers are securely anchored.
* **Structural Grime vs. Content Grime:**
  * *Structural Grime:* Values in the wrong place (ragged CSV rows, inconsistent delimiters, per-cell typing in spreadsheets, character encoding glitches). Must be resolved at the ingestion boundary with zero data loss.
  * *Content Grime:* Incorrect values in the right place (sentinel ages like `-999`, inverted date intervals where $t_{\min} > t_{\max}$, spelling typos in genus names). Resolved via domain-bound validation and explicit anomaly ledgers.
* **Scripted Provenance & Idempotence ($f(f(x)) = f(x)$):** Never overwrite raw source files. Never rely on interactive notebook cell states as the source of truth. Every transform must be an idempotent function in version-controlled code, fully testable under automated CI.

---

## 2. Ingestion Hygiene & Format Traps

### 2.1 The Raw Boundary: Spreadsheets as an Attractive Nuisance
Spreadsheets (Excel `.xlsx`) are the primary exchange format in paleobiology (e.g., the Van Holstein & Foley 2024 occurrence table). Following Mertz (Ch. 1), spreadsheets present severe systemic hazards:
1. **Per-Cell Rather Than Per-Column Typing:** A single column can contain floats, strings, and blank cells without warning.
2. **Silent Coercion:** Text identifiers like specimen codes (`AL 288-1`) or dates can be silently reformatted or corrupted.
3. **Hidden Layout Grime:** Embedded notes, color codes, and non-contiguous tables.

**Our Defense:**
- Raw spreadsheets are preserved byte-for-byte in `data/raw/` and cryptographically hashed (SHA-256).
- Ingestion bypasses heavy, mutating spreadsheet engines; we use zero-dependency, streaming XML/Zip parsers (`xml.etree.ElementTree`) reading `xl/worksheets/sheet1.xml` and `xl/sharedStrings.xml` directly to extract raw strings and numeric attributes without automatic type mutation.
- All extracted records are immediately mapped to strongly-typed, immutable dataclasses (`HomininSpecimenOccurrence`).

### 2.2 Delimited Text (CSV/TSV) and Type Safety
Delimited files carry no schema metadata. Standard dataframe readers (`pandas.read_csv`) infer types from leading row batches, leading to catastrophic type casting if trailing rows contain alphanumeric catalog IDs or missing value sentinels.
- Ingestion scripts must enforce explicit schema definitions with strict type conversions and defensive null-handling.
- Floating-point date values must be checked for sentinel encoding (`NA`, `None`, `-1`, `0`).

---

## 3. Paleobiological Data Cleaning Protocols

When ingesting fossil hominin records, five domain-specific integrity checks are mandatory:

```
PALEONTOLOGICAL INTEGRITY GATES
┌─────────────────────────────────┐
│ Gate 1: Stratigraphic Invariant │  Verify: Site_Max_MA ≥ Site_Min_MA and
│                                 │          Strat_Max_MA ≥ Strat_Min_MA
└────────────────┬────────────────┘  Isolate inverted geological age intervals (Content Grime)
                 │
                 ▼
┌─────────────────────────────────┐
│ Gate 2: Temporal Granularity    │  Distinguish site-level bounding intervals
│                                 │  from bed-level stratigraphic member dates
└────────────────┬────────────────┘  Flag occurrences lacking bed-level constraints
                 │
                 ▼
┌─────────────────────────────────┐
│ Gate 3: Specimen Disambiguation │  Extract canonical museum catalog IDs
│                                 │  (KNM-ER, OH, AL, StW, SK, Dmanisi) from comments
└────────────────┬────────────────┘  Prevent conflating find-spots with individuals
                 │
                 ▼
┌─────────────────────────────────┐
│ Gate 4: Taxonomic Decoupling    │  Separate empirical specimen records from
│                                 │  lumper/splitter taxonomic opinions
└────────────────┬────────────────┘  Map to Foley's Paleodemes and Ecological Grades
                 │
                 ▼
┌─────────────────────────────────┐
│ Gate 5: Taphonomic Compensation │  Profile spatial and temporal sampling skew
│                                 │  Condition models against preservation gradients
└─────────────────────────────────┘
```

### 3.1 Stratigraphic Age Invariants & Inversion Defects (Content Grime)
Geological ages in deep time are measured in millions of years before present ($\text{Ma}$). Therefore:
$$\text{Max\_Age} \ge \text{Min\_Age} \ge 0$$
Any row where $\text{Max\_Age} < \text{Min\_Age}$ is an **inverted interval defect** (where min and max were transposed during data entry). In our audit of Van Holstein & Foley's raw database, our automated gate discovered **5 inverted age records**:
1. **Row 31 (A. anamensis, Korsi Dora):** Site Max 3.58 Ma < Site Min 3.6 Ma, Strat Max 3.58 Ma < Strat Min 3.6 Ma.
2. **Row 35 (A. anamensis, Korsi Dora):** Strat Max 3.58 Ma < Strat Min 3.6 Ma.
3. **Row 264 (H. neanderthalensis, Madonna dell'Arma):** Site Max 0.191 Ma < Site Min 0.71 Ma.
4. **Row 269 (H. neanderthalensis, La Chapelle-aux-Saints):** Site Max 0.04 Ma < Site Min 0.071 Ma.
5. **Row 322 (H. sapiens, Tabon):** Site Max 0.039 Ma < Site Min 0.22 Ma.

**Protocol:** We preserve the raw values in Layer 0 and Layer 1 exactly as published, but flag them in an anomaly registry and provide rectified bounds in Layer 2 transforms so downstream models do not execute on inverted time spans.

### 3.2 Granularity Separation: Bed vs. Site Dates
In Van Holstein & Foley (2024), only 169 of 385 rows possess bed-level bounds (`Strat_Max_MA`, `Strat_Min_MA`), while 373 possess site bounds (`Site_Max_MA`, `Site_Min_Ma`). A fatal flaw of uncritical data ingestion is treating broad cave-complex site dates (e.g., $3.83 - 2.32\text{ Ma}$) as if they were tightly resolved stratigraphic horizons ($3.66 - 3.63\text{ Ma}$). Our schema explicitly tracks `has_strat_bounds` to prevent artificial temporal smearing.

### 3.3 Specimen Disambiguation & Provenance Extraction
Many public occurrence databases record a "site occurrence" where the comments field contains multiple distinct cataloged specimens (e.g., `L.H. 1, 20` or `Includes A.L. 288 (Lucy), 438, 444`).
- Ingestion scripts must run deterministic regex extractors to capture all museum catalog identifiers into structured collections.
- This maintains auditability back to physical museum collections (National Museums of Kenya, Dmanisi, Ditsong National Museum).

### 3.4 Decoupling Specimen Reality from Taxonomic Analogies
Species names in paleoanthropology are analytical hypotheses summarizing clusters of morphological difference vectors across cranial, dental, and postcranial traits. Following Robert Foley:
- The fundamental unit of evidence is the **specimen occurrence** at a dated geological horizon.
- Biological populations are modeled as **paleodemes** (localized fossil populations sampled from a specific basin and time slice).
- Functional comparisons are organized by **ecological grades** (`Homo 1`, `Homo 2`, `Homo 3`, `Paranthropus`, `Australopithecine`).
- Models must test parameter sensitivity across alternative taxonomic views (e.g., Wood & Boyle vs. Foley & Lahr) rather than locking in a single subjective lumping or splitting scheme.

---

## 4. Anomaly Detection and Taphonomic Forensics

Mertz (Part II: Chapters 4–6) outlines statistical cleaning methods that directly apply to evaluating paleobiological datasets:

1. **Benford's Law and Digit Preference:** Tabulated morphological measurements and stratigraphic dates should be tested for digit preference or rounding artifacts (e.g., clustering at `.0` or `.5` Ma).
2. **Truncation and Clipping Detection:** Stratigraphic intervals ending abruptly at geological epoch boundaries (e.g., exactly at $2.58\text{ Ma}$ for the Plio-Pleistocene boundary) indicate artificial convention rather than radiometric measurement.
3. **Outlier Profiles vs. Sampling Asymmetry:** In the Van Holstein & Foley dataset, 233 of 385 occurrences (60.5%) belong to just three late taxa (*H. erectus*, *H. neanderthalensis*, *H. sapiens*). Standard outlier rejection would discard vital data; instead, taphonomic compensation models must explicitly incorporate this preservation and collection surge into the likelihood function rather than mistaking it for a biological speciation burst.

---

## 5. Summary Checklist for New Ingress

Before any external dataset enters this repository:
- [ ] Raw file placed in `data/raw/<source_year>/` with original name and extension.
- [ ] SHA-256 hash and byte count logged in `data/DATA_INVENTORY_AND_PROVENANCE.md`.
- [ ] Zero-dependency streaming reader implemented in `src/hominin_morphodynamics/schema/`.
- [ ] Domain invariants verified (stratigraphic ordering, age bounds, coordinate validity).
- [ ] Automated pytest suite validates structural integrity and documents known anomalies.
