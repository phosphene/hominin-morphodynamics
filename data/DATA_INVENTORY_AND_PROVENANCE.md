# Data Inventory, Provenance & Preservation Ledger

**Document Coordinate:** `data/DATA_INVENTORY_AND_PROVENANCE.md`  
**Repository:** `phosphene/hominin-morphodynamics`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Forensic Standard  
**Date:** 2026-11-16  

---

## 1. Raw Data Ingress & Preservation Directive

Per the platform's raw data preservation ethic:
1. **Zero Premature Conversion:** Raw data is preserved in its authentic, unmodified native formats (`.xlsx`, `.csv`). It is never prematurely coerced into JSON or altered in whitespace or precision.
2. **Cryptographic Sealing:** Every raw file in `data/raw/` is sealed with SHA-256 hashes and byte counts prior to asking questions or conducting transforms.
3. **Immutability of `data/raw/`:** Files under `data/raw/` are strictly read-only.
4. **Codified and Versioned Transforms:** Any derived view, annotation layer (e.g., Foley paleodemes, ecological grades, specimen catalog extraction), or stratigraphic realignment is codified in deterministic Python modules under `src/hominin_morphodynamics/` with explicit input/output provenance and automated regression tests in CI.

---

## 2. Ingress Manifest & Cryptographic Hashes

```
RAW ASSET LEDGER
┌──────────────────────────────┬──────────────────┬───────────┬──────────────────────────────────────────────────────────────────┐
│ Relative Path                │ Native Format    │ Bytes     │ SHA-256 Digest                                                   │
├──────────────────────────────┼──────────────────┼───────────┼──────────────────────────────────────────────────────────────────┤
│ Occurrence_database.xlsx     │ Native Excel     │ 44,748    │ d3eb51d6a4f892d376409bb40af7511a97e9027c98a3281f39b530b78f7577f9│
│ WB_equivalent_taxonomy.csv   │ Native CSV (UTF8)│ 638       │ f51ad7d4f1c82cf71349c381e8e169ee25684966f6a501309cbc6dabe0573de1│
└──────────────────────────────┴──────────────────┴───────────┴──────────────────────────────────────────────────────────────────┘
```

### Source Attribution
- **Published Study:** Van Holstein, L., & Foley, R. A. (2024). *Diversity-dependent speciation and extinction in the hominin lineage.* Nature Ecology & Evolution.
- **Repository Package:** Figshare DOI `10.6084/m9.figshare.24183417.v1`.
- **Primary Authors:** Laura van Holstein & Robert A. Foley (Leverhulme Centre for Human Evolutionary Studies, University of Cambridge).

---

## 3. Structural Breakdown of Native Assets

### A. `Occurrence_database.xlsx`
- **Container:** Standard OOXML spreadsheet.
- **Sheets:**
  1. `Database`: 386 rows (1 header row + 385 data rows), 17 columns.
  2. `Notes`: 6 rows (subsite abbreviations index).
- **Column Coordinates:**
  - `0: Species_name`: Binomial taxon label (17 distinct taxa).
  - `1: Site complex`: Macro-region / basin (e.g., Laetoli, Hadar, Turkana, SA, Dmanisi).
  - `2: Site`: Specific geographical or cave site (e.g., Koobi Fora, Sterkfontein, Swartkrans).
  - `3: Site_Max_MA`, `4: Site_Min_Ma`: Macro-site bounding age interval (Ma).
  - `5: Subsite`, `6: Subsite_type`: Specific locality designation (Locality, In situ, IFS).
  - `7: Subsite_Max_MA`, `8: Subsite_Min_Ma`: Subsite bounding ages (sparse).
  - `9: Formation`: Geological formation (e.g., Laetolil, Nachukui, Koobi Fora).
  - `10: Stratigraphic_unit`: Specific sedimentary member/bed (e.g., T7-T8, KBS Member).
  - `11: Strat_Max_MA`, `12: Strat_Min_MA`: Bed-level stratigraphic bounds (169 rows populated).
  - `13: Comments`: Contains vital museum specimen catalog numbers (L.H., KNM-ER, OH, AL, StW, SK, Dmanisi, etc.).
  - `14: Source`: Primary geochronological and paleontological publication citations.
  - `15: longitude`, `16: latitude`: Geospatial coordinates (sparse, 20 rows).

### B. `WB_equivalent_taxonomy.csv`
- **Format:** Comma-separated values.
- **Dimensions:** 18 lines (1 header + 17 taxon rows).
- **Columns:** `species`, `ts` (first appearance date in Ma), `te` (last appearance date in Ma).
- **Scope:** Defines the Wood & Boyle equivalent taxonomic aggregation scheme over the fossil record.

---

## 4. Codified Transforms & Invariant Pipeline

To ensure zero loss of metadata and rigorous traceability, transforms follow a four-tier pipeline:

```
TRANSFORM & ANNOTATION PIPELINE
┌─────────────────────────────────┐
│ Layer 0: Raw Native Files       │  data/raw/van_holstein_2024/
│ (Byte-sealed .xlsx & .csv)      │
└────────────────┬────────────────┘
                 │
                 ▼ (Read-only stdlib streaming parser)
┌─────────────────────────────────┐
│ Layer 1: Invariant Specimen     │  src/hominin_morphodynamics/schema/specimens.py
│ Records (HomininSpecimenRecord) │  - Preserves exact raw coordinates
│                                 │  - Extracts museum catalog codes (KNM, OH, AL, StW, SK)
└────────────────┬────────────────┘  - Flags taphonomic / age uncertainty bounds
                 │
                 ▼ (Explicit annotation transform)
┌─────────────────────────────────┐
│ Layer 2: Paleodeme & Grade      │  src/hominin_morphodynamics/schema/paleodemes.py
│ Projections                     │  - Foley's Ecological Grades (Homo 1, 2, 3, Paranthropus)
│                                 │  - Regional Paleodemes (basin/time slice clusters)
└────────────────┬────────────────┘
                 │
                 ▼ (Inference & calibration)
┌─────────────────────────────────┐
│ Layer 3: Falsifiable Estimators │  src/hominin_morphodynamics/inference/
│ & Audit Diagnostics             │  - Parameter stability audits (PyRate Gl CIs)
└─────────────────────────────────┘  - Horizon-coupled likelihoods
```
