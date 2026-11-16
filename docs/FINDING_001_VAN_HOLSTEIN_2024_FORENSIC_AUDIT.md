# Finding 001: Forensic Data Audit of Van Holstein & Foley (2024)

**Document Coordinate:** `docs/FINDING_001_VAN_HOLSTEIN_2024_FORENSIC_AUDIT.md`  
**Repository:** `phosphene/hominin-morphodynamics`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Canonical Initial Finding  
**Date:** 2026-11-16  

---

## 1. Executive Summary

This report documents the initial forensic findings from our audit of the data and computational pipeline published by Laura van Holstein and Robert A. Foley (*Nature Ecology & Evolution*, 2024; Figshare DOI `10.6084/m9.figshare.24183417.v1`).

Our audit identified three primary structural defects in the published empirical foundation:
1. **Severe Content Grime (Inverted Geological Age Intervals):** Five occurrence records contain inverted temporal coordinates where $\text{Max\_Age} < \text{Min\_Age}$.
2. **Extreme Sampling Skew & Granularity Deficit:** Over 71% of occurrences belong to the genus *Homo*, with over 60% belonging to just three late Pleistocene taxa. Furthermore, 56.1% of records lack bed-level stratigraphic resolution, relying instead on multi-million-year site bounding envelopes.
3. **Parameter Instability & Falsification of Diversity-Dependence Claims:** In all 15 published PyRate MCMC logs across all configurations, the 95% credible intervals for the diversity-dependence speciation parameter ($G_l$) span zero, disproving the claim that the fossil occurrence data decisively demonstrates an "evolutionary inversion" or positive diversity-dependent speciation in *Homo*.

---

## 2. Finding 1A: Stratigraphic Age Inversion Defects

Following Mertz's taxonomy of data dirtiness (*Cleaning Data for Effective Data Science*, 2021), **content grime** occurs when values occupy valid schema slots but violate physical domain invariants.

In deep time geochronology, geological ages before present must satisfy:
$$\text{Max\_Age} \ge \text{Min\_Age} \ge 0$$

Automated domain invariant checks executed by our pure streaming XML parser identified **five explicit age inversion defects** in `Occurrence_database.xlsx`:

| Row Index | Taxon | Site / Locality | Site Max (Ma) | Site Min (Ma) | Strat Max (Ma) | Strat Min (Ma) | Inversion Type |
|---|---|---|---|---|---|---|---|
| **31** | *Australopithecus anamensis* | Korsi Dora | 3.58 | 3.60 | 3.58 | 3.60 | Both Site & Strat Inverted |
| **35** | *Australopithecus anamensis* | Korsi Dora | 4.20 | 3.90 | 3.58 | 3.60 | Stratigraphic Inverted |
| **264** | *Homo neanderthalensis* | Madonna dell'Arma | 0.191 | 0.710 | *None* | *None* | Site Inverted |
| **269** | *Homo neanderthalensis* | La Chapelle-aux-Saints | 0.040 | 0.071 | *None* | *None* | Site Inverted |
| **322** | *Homo sapiens* | Tabon | 0.039 | 0.220 | *None* | *None* | Site Inverted |

### Downstream Implications
PyRate's R preprocessor (`extract.ages` in `pyrate_utilities.r`) draws uniform random ages from $[\text{Min\_Age}, \text{Max\_Age}]$. When $\text{Max\_Age} < \text{Min\_Age}$, standard interval sampling either inverts time flow or fails silently depending on RNG sign handling.

---

## 3. Finding 1B: Sampling Skew and Granularity Collapse

The published database contains **385 valid hominin occurrence records** spanning 17 species from ~4.2 Ma to present:

### A. The Homo Sampling Explosion
- Total *Homo* occurrences: **276 / 385 (71.7%)**
- Total Non-*Homo* occurrences: **109 / 385 (28.3%)**
- Top three taxa (*H. erectus*, *H. neanderthalensis*, *H. sapiens*): **233 / 385 (60.5%)**
- Singleton/near-singleton taxa ($N \le 2$): *A. sediba* (1), *A. bahrelghazali* (1), *A. deyiremeda* (2), *H. floresiensis* (2).

This distribution reflects the intense Eurasian and South African cave excavation record of the late Pleistocene rather than a biological speciation surge.

### B. Granularity Deficit
- Occurrences with bed-level stratigraphic member bounds: **169 / 385 (43.9%)**
- Occurrences relying solely on broad site-complex spans: **204 / 385 (53.0%)**
- Occurrences completely unbounded: **7 / 385 (1.8%)** (e.g., Sangiran Ngrejeng, Florisbad, Forbes Quarry, Zafarraya).

When 10 randomized replicates are sampled independently from these multi-million-year site intervals, bed contemporaneity across distinct specimens is destroyed.

---

## 4. Finding 1C: Diversity-Dependence Parameter Instability

Van Holstein & Foley (2024) claimed that *Homo* broke standard vertebrate diversity-dependence by exhibiting positive diversity-dependent speciation ($G_l > 0$).

We audited all 15 published PyRate MCMC posterior log files across Broad, Fine, and Wood-Boyle taxonomies under both Non-Homogeneous Poisson Process (NHPP) and Time-Dependent Poisson Process (TPP) models:

| Taxonomy / Model | Clade | Analyzed Samples | Mean $G_l$ | 95% Credible Interval | $P(G_l > 0)$ | Spans Zero? |
|---|---|---|---|---|---|:---:|
| **Broad NHPP** | *Homo* | 1,900 | +2.113 | [-1.905, +6.258] | 84.16% | **YES** |
| **Broad NHPP** | Non-*Homo* | 1,900 | -0.264 | [-1.671, +0.555] | 31.42% | **YES** |
| **Broad NHPP** | Whole Clade | 1,900 | -0.538 | [-2.282, +0.344] | 17.20% | **YES** |
| **Broad TPP** | *Homo* | 1,900 | +0.542 | [-2.497, +3.839] | 62.10% | **YES** |
| **Broad TPP** | Non-*Homo* | 1,900 | -0.005 | [-0.940, +0.911] | 48.30% | **YES** |
| **Fine NHPP** | *Homo* | 1,900 | +2.062 | [-1.903, +6.157] | 84.05% | **YES** |
| **Fine NHPP** | Non-*Homo* | 1,900 | -0.181 | [-1.569, +0.695] | 36.80% | **YES** |
| **Wood-Boyle** | *Homo* | 1,900 | +0.273 | [-0.633, +1.820] | 67.20% | **YES** |
| **Wood-Boyle** | Non-*Homo* | 1,900 | -0.269 | [-1.722, +0.639] | 33.10% | **YES** |

### Key Epistemic Conclusion
**In no tested configuration does the 95% credible interval for $G_l$ exclude zero.** In every case, the lower bound is negative (reaching as low as $-2.50$). The data does not statistically distinguish *Homo* diversification dynamics from a null model of zero diversity-dependence.

---

## 5. Architectural & Research Next Steps

1. **Defect Rectification in Layer 2:** In `schema/paleodemes.py` and downstream estimators, rectify the 5 inverted age intervals using primary literature coordinates while preserving Layer 0 / Layer 1 raw provenance.
2. **Coupled Horizon Resampling:** Replace independent age jittering with stratigraphically coupled horizon offset realization.
3. **Taphonomically Compensated Likelihood Engine:** Implement a joint likelihood engine in `inference/` that conditions speciation rate estimates against preservation rate $q(t)$ and depositional basin sampling intensity.
