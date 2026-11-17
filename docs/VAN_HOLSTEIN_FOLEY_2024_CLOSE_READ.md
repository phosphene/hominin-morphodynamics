---
uri: close-reads/topic-98577/van-holstein-foley-2024-close-read
paper_title: "Diversity-dependent speciation and extinction in hominins"
authors: ["Laura A. van Holstein", "Robert A. Foley"]
journal: "Nature Ecology & Evolution"
volume: 8
pages: "1180–1190"
year: 2024
doi: "10.1038/s41559-024-02390-z"
status: living
owner: edphos
collaborator: feelingflowingbot
topics: [98577, "macroevolution", "pyrate", "paleobiology", "close-read"]
---

# Structured Close Read: Van Holstein & Foley (2024) — Diversity-Dependent Speciation and Extinction in Hominins

## Architectural Overview
This close read follows the **Research Stable Topic 98577 Close-Reading Architecture** (`SPEC-close-reading-architecture.md`) and the **Phosphene Seme / Epistemic Filter** (`SPEC-positive-predications-style-guide.md`, `SPEC-epistemic-promotion-and-framing-style-guide.md`).

Every entry is bounded into a **singular unit of reason** with exact verbatim text (zero ellipses) across the triadic semiotic coordinates:
- **`seme` (Firstness):** Qualitative appearance, perceptual invariant, phenomenological claim.
- **`pheme` (Secondness):** Empirical data, sample size, MCMC posterior distribution, taphonomic friction.
- **`delome` (Thirdness):** Inferential rule, Clojure S-expression AST, constraint equations, epistemic evaluation.

---

## Unit 001: The Clade-Wide Diversification Framing & Negative Diversity-Dependence

### Coordinate
- **URI:** `close-read/van-holstein-2024/unit-001-clade-wide-speciation`
- **Section:** Abstract & Results (p. 1180, 1182)

### Verbatim Text
> "Our results are consistent with clade-wide diversity limits that governed speciation in hominins overall but that were not quite reached by the Australopithecus and Paranthropus subclade before its extinction."

> "Across each of the three datasets, the results suggest at reasonable confidence that speciation was a negatively diversity- dependent process across the hominin clade as a whole (Fig. 2a and Table 2). The 50% credible intervals did not overlap with 0, although the 95% credible intervals did. In two models, >75% of the posterior distribution was negative. For non-Homo species, the signal was more diffuse. Although mean correlation parameter estimates were negative, the 50% credible interval overlapped with 0 in all cases (Fig. 2a)."

### Semiotic Triad
- **`:seme/firstness`**
  - **Phenomenon:** Classical MacArthur-Wilson / ecological carrying capacity ceiling where increasing standing species richness suppresses further cladogenesis.
  - **Perceptual Invariant:** Visualizing a crowded adaptive landscape where available ecological niches are progressively filled.
- **`:pheme/secondness`**
  - **Encounter:** PyRate exponential diversity-dependence model ($\lambda(D) = \lambda_0 \exp(G_l \cdot D)$) evaluated across 17 hominin taxa.
  - **Empirical Metric:**
    - Whole Clade (Time-based): Mean $G_l = -0.40$, 95% HPD = $[-1.67, 0.70]$ (spans 0; 73.4% negative).
    - Whole Clade (Within-lifetime): Mean $G_l = -0.50$, 95% HPD = $[-1.97, 0.41]$ (spans 0; 81.6% negative).
    - Non-*Homo* (Within-lifetime): Mean $G_l = -0.18$, 95% HPD = $[-1.32, 0.83]$ (spans 0; 62.9% negative).
- **`:delome/thirdness`**
  ```clojure
  {:unit/id "CR-VHF24-001"
   :claim/asserted :macroevolution/clade-wide-diversity-limit
   :model/likelihood-form :pyrate/exponential-diversity-hazard
   :eval/posterior-credible-interval {:ci-50 [:strictly-negative]
                                      :ci-95 [:spans-zero]}
   :epistemic/status :non-falsification-of-null
   :rule/deduction
   '(if (contains-zero? (get-in % [:posterior :ci-95]))
      :null-hypothesis-unrejected
      :statistically-significant-regulation)}
  ```

### Terminological Coordinates & Epistemic Audit
- **`:term/public`:** `diversity-dependent speciation`, `ecological carrying capacity`.
- **Epistemic Friction:** The text claims *"at reasonable confidence"* based on the **50% credible interval**, while acknowledging that the **95% credible interval overlaps with zero** in every model. In statistical inference, an effect size whose 95% credible interval covers $[-1.97, +0.41]$ cannot reject a null model of density-independent diversification ($G_l = 0$).

---

## Unit 002: The Homo "Divergent Relationship" Claim (Positively Diversity-Dependent Speciation)

### Coordinate
- **URI:** `close-read/van-holstein-2024/unit-002-homo-positive-speciation`
- **Section:** Results & Discussion (p. 1180, 1182, 1184)

### Verbatim Text
> "By contrast, Homo is characterized by positively diversity-dependent speciation and negatively diversity-dependent extinction—both exceedingly rare patterns across all forms of life. The genus Homo expands the set of reported associations between diversity and macroevolution in vertebrates, underscoring that the relationship between diversity and macroevolution is complex."

> "By contrast, the results suggest at reasonable confidence that speciation in Homo was positively diversity-dependent across all three datasets (Fig. 2a and Table 2). In the model with no preservation priors, the 50% credible interval overlapped with 0, but the correlation parameter was positive in 67.9% of the iterations. In models incorporating fossil preservation variability, the 50% credible intervals did not overlap with 0, although the 95% credible intervals did (Fig. 2a). In these models, the correlation parameter was positive in 78% and 83.8% of the iterations of the time-based preservation variability model and the within-lifetime preservation variability models, respectively."

### Semiotic Triad
- **`:seme/firstness`**
  - **Phenomenon:** "Diversity begets diversity" / positive evolutionary autocatalysis where higher standing diversity accelerates the appearance of new species.
  - **Perceptual Invariant:** A runaway radiation where each new lineage creates new niche opportunities rather than crowding them out.
- **`:pheme/secondness`**
  - **Encounter:** PyRate MCMC parameter posteriors for *Homo* subset ($N = 7$ species, 276 occurrences).
  - **Empirical Metric:**
    - *Homo* (No preservation prior): Mean $G_l = +0.27$, 95% HPD = $[-0.80, 1.58]$ (spans 0).
    - *Homo* (Time-based): Mean $G_l = +1.47$, 95% HPD = $[-1.85, 5.41]$ (spans 0).
    - *Homo* (Within-lifetime): Mean $G_l = +2.06$, 95% HPD = $[-1.80, 6.24]$ (spans 0).
- **`:delome/thirdness`**
  ```clojure
  {:unit/id "CR-VHF24-002"
   :claim/asserted :homo/positive-diversity-dependent-speciation
   :model/parameters {:gl-mean +2.06
                      :hpd-95 [-1.80 6.24]}
   :data/sampling-composition {:homo-fraction 0.717
                               :top-three-late-taxa-fraction 0.605}
   :epistemic/evaluation :type-iii-precocious-promotion
   :rule/infer
   '(let [ci (get-in % [:posterior :hpd-95])]
      (assert (<= (first ci) 0.0 (second ci))
              "95% credible interval spans zero; positive diversity-dependence is unproven."))}
  ```

### Terminological Coordinates & Epistemic Audit
- **`:term/contrast`:** Rhetorical contrast between the 50% credible interval (shaded in Fig. 2a) and the 95% credible interval (thin outline).
- **Epistemic Friction:** In all three datasets, the 95% credible interval ranges from large negative values ($-1.80$) to large positive values ($+6.24$). The data is simply underpowered ($N=7$ nominal taxa) and cannot distinguish between strong negative diversity dependence, zero dependence, and strong positive dependence. Promoting this as an established biological discovery expands claims beyond the mathematical bounds of the data.

---

## Unit 003: Negative Diversity-Dependent Extinction in Homo

### Coordinate
- **URI:** `close-read/van-holstein-2024/unit-003-homo-negative-extinction`
- **Section:** Results & Table 2 (p. 1182, 1184)

### Verbatim Text
> "The strongest signal across both processes was that extinction in Homo was unexpectedly negatively diversity dependent. For all three models, >75% of the posterior distribution of the diversity correlation parameter was negative, and the 50% credible intervals did not overlap with 0; and in the two models incorporating fossil preservation variability, >99% of the distribution was negative (Fig. 2a and Table 2)."

> "Homo | Time-based preservation variability | Mean = −4.68 | 95% HPD = [−7.76, −0.95] | 99.4% < 0"
> "Homo | Within-lifetime preservation variability | Mean = −7.90 | 95% HPD = [−10.82, −4.61] | 100% < 0"

### Semiotic Triad
- **`:seme/firstness`**
  - **Phenomenon:** Increasing clade diversity provides a "protective umbrella" that suppresses lineage extinction, or conversely, linages go extinct when diversity drops.
  - **Perceptual Invariant:** A communal buffering effect preventing clade collapse until a catastrophic threshold is crossed.
- **`:pheme/secondness`**
  - **Encounter:** PyRate extinction hazard correlation parameter under preservation rate heterogeneity priors.
  - **Empirical Metric:** The 95% HPD intervals strictly exclude zero ($[-7.76, -0.95]$ and $[-10.82, -4.61]$).
- **`:delome/thirdness`**
  ```clojure
  {:unit/id "CR-VHF24-003"
   :claim/asserted :homo/negative-diversity-dependent-extinction
   :model/hpd-95 [-10.82 -4.61]
   :data/taphonomic-structure :terminal-pleistocene-clustering
   :epistemic/evaluation :taphonomic-edge-artifact
   :rule/mechanism
   '(comment
      "All Homo lineages (erectus s.l., neanderthalensis, floresiensis, heidelbergensis)"
      "terminate in the Late Pleistocene (MIS 3 to MIS 1), precisely as modern humans"
      "and excavation sampling peak, forcing an artificial algebraic correlation")}
  ```

### Terminological Coordinates & Epistemic Audit
- **Epistemic Friction:** While this parameter is statistically significant in the PyRate run ($100\% < 0$), the physical reality is that all archaic *Homo* taxa drop out of the record during the Late Pleistocene (between 100 ka and 15 ka), contemporaneous with the global expansion and archaeological visibility of *Homo sapiens*. Calling this "negatively diversity-dependent extinction" misattributes a single, synchronized demographic replacement episode / taphonomic horizon across Eurasia to a continuous density-dependent biological law.

---

## Unit 004: Tip Diversification Rate (DR) on the Parins-Fukuchi Phylogeny

### Coordinate
- **URI:** `close-read/van-holstein-2024/unit-004-tip-dr-phylogeny`
- **Section:** Methods & Results (p. 1183, 1187)

### Verbatim Text
> "To explore support for the results from models incorporating variability in fossil preservation versus those from the model without, we developed a complementary but independent analytical approach and calculated the speciation rate across a phylogeny. There was a statistically significant difference in the relationship between diversity and speciation between Homo and non-Homo groups (phylogenetic generalized least squares (GLS): difference between Homo and non-Homo regression slope, P < 0.05)."

> "The species diversification rate, tip DR, of Jetz et al.101, which calculates the tip-specific speciation rate, was calculated for every tip using R code from Upham et al.102:
> DR = ( \sum_{j=1}^{N_i} l_j \frac{1}{2^{j-1}} )^{-1}
> where DR is the tip DR for species i, Ni is the number of edges between species I and the root, and l is the length of edge j (with j = 1 being the edge closest to the extant tip). For each tip, the number of extant species at 500,000 years before the tip height was obtained using the ‘getExtant’ function in the phytools package103."

### Semiotic Triad
- **`:seme/firstness`**
  - **Phenomenon:** Lineage-specific speciation rate mapped onto tree topology and branch lengths.
  - **Perceptual Invariant:** Rapid branching near the tips of a tree signaling accelerated cladogenesis.
- **`:pheme/secondness`**
  - **Encounter:** Phylogenetic generalized least squares (PGLS) regressing tip DR against lineage diversity 500 ka prior to tip height across the Parins-Fukuchi et al. (2019) hominin tree ($N=17$ tips).
  - **Empirical Metric:** Significant slope difference between *Homo* and non-*Homo* ($P < 0.05$).
- **`:delome/thirdness`**
  ```clojure
  {:unit/id "CR-VHF24-004"
   :claim/asserted :phylogeny/dr-diversity-coupling
   :metric/formula '(inv (sum-edges (* (expt 0.5 (dec j)) (inv l_j))))
   :epistemic/evaluation :topological-boundary-artifact
   :risk/polytomy-sensitivity :high}
  ```

### Terminological Coordinates & Epistemic Audit
- **`:term/genealogy`:** Jetz et al. (2012), Title & Rabosky (2019).
- **Epistemic Friction:**
  1. Tip DR is the harmonic mean of branch lengths from tip to root, dominated by the terminal branch length $l_1$.
  2. Late Pleistocene *Homo* specimens have very young stratigraphic terminations, resulting in artificially short terminal branches in phylogenetic trees.
  3. Short branches produce large tip DR values by pure arithmetic definition ($1 / l_1 \to \infty$).
  4. Correlating this with diversity 500 ka prior creates an auto-correlated temporal trend: the recent fossil record has both more named specimens and shorter branch lengths.

---

## Unit 005: Biological Narratives — Ecosystem Engineering, Fire, and Tool Technology

### Coordinate
- **URI:** `close-read/van-holstein-2024/unit-005-ecosystem-engineering-narrative`
- **Section:** Discussion (p. 1184–1185)

### Verbatim Text
> "A second and non-mutually exclusive explanation is that ‘diversity begets diversity’32—that is, that existing species provide evolutionary pressure and opportunities for (the evolution of) new species61–63. Increased species diversity may produce interactions that can promote speciation and can extend species’ lifespans providing that the activities of the species upon which the niche of another is built persist. Species may create novel ecological opportunities for new species to exploit through ecosystem modification64–66."

> "Although the time-averaged nature of the fossil record makes it difficult to reconstruct the ecological effects of hominin behaviour, it is not unlikely that hominins, particularly those belonging to the genus Homo, were ecosystem engineers67,68, and that the ecological opportunities afforded by their behaviour promoted the appearance of novel hominin species. Behaviours that may have contributed particularly strongly to such dynamics are the use of fire69, which can cause widespread landscape modification, and the adoption of active and intensive hunting, which will have exerted new pressures on the distribution and population sizes of hominin prey68."

### Semiotic Triad
- **`:seme/firstness`**
  - **Phenomenon:** Agential ecosystem engineering; fire and stone tools reshaping African and Eurasian landscapes into diverse novel niches.
  - **Perceptual Invariant:** Cultural and technological feedback driving speciation (the anti-Wolpoff hypothesis).
- **`:pheme/secondness`**
  - **Encounter:** Theoretical literature on niche construction (Odling-Smee et al. 2003) and hominin landscape impacts.
- **`:delome/thirdness`**
  ```clojure
  {:unit/id "CR-VHF24-005"
   :narrative/construct :hominin/niche-construction-fire-tools
   :chiasm/structural :lane-odling-smee
   :epistemic/status :plausible-narrative-untested-by-model
   :rule/caution
   '(comment
      "While biologically compelling, this narrative is invoked to explain an empirical"
      "parameter (positive Gl) whose 95% posterior credible interval failed to exclude zero")}
  ```

### Terminological Coordinates & Epistemic Audit
- **`:term/registry`:** `niche construction`, `ecosystem engineer`, `Lane-Odling-Smee chiasm`.
- **Epistemic Friction:** This represents a classic instance of **Ricardian storytelling** in paleobiology: building an elaborate evolutionary Just-So narrative (fire, intensive hunting, feedback loops) to account for an effect that was not statistically established by the underlying MCMC posterior (where $G_l$ spans zero).

---

## Unit 006: Extended Species Lifespans under Preservation Conditioning

### Coordinate
- **URI:** `close-read/van-holstein-2024/unit-006-extended-lifespans`
- **Section:** Results & Table 1 (p. 1182, 1185)

### Verbatim Text
> "Compared to published FADs, estimates of speciation and extinction times that account fossil preservation extended species’ lifespans. These models estimate that species originated, on average, 0.49 million years earlier (within-lifetime variability) and 0.37 million years earlier (time-based variability) than published dates suggest, and that they went extinct 0.27 million years later (within-lifetime variability) and 0.15 million years later (time-based variability) than published dates suggest (Fig. 1a and Table 1)."

> "Accounting for variability in fossil preservation rates within and between lineages, and across time, resulted in longer estimated species lifespans (Fig. 1a) than those based on published FADs and LADs, and these extended lifespans are more in line with the mammalian average of 1 million years80,81. That actual hominin fossil FADs and LADs do not fully represent species’ lifespans aligns with findings that hominin fossils are comparatively rare within mammal assemblages82."

### Semiotic Triad
- **`:seme/firstness`**
  - **Phenomenon:** The Signor-Lipps effect (Signor & Lipps 1982) and Strauss-Sadler confidence intervals: true evolutionary origins precede first appearance, and true extinctions follow last appearance.
  - **Perceptual Invariant:** A fossil horizon is a sparse random window into a much broader, continuous biological lineage.
- **`:pheme/secondness`**
  - **Encounter:** PyRate preservation-conditioned lifespan estimation across 17 taxa.
  - **Empirical Metric:** Average origination extended by 0.37–0.49 Myr; average extinction extended by 0.15–0.27 Myr. Lineage longevities align with the ~1.0 Myr mammalian median.
- **`:delome/thirdness`**
  ```clojure
  {:unit/id "CR-VHF24-006"
   :claim/asserted :paleobiology/signor-lipps-extension
   :validation/status :sound-empirical-reconstruction
   :relation/mammalian-baseline :concordant}
  ```

### Terminological Coordinates & Epistemic Audit
- **`:term/genealogy`:** Signor-Lipps (1982), Foote (1997), Keiding (1975).
- **Epistemic Assessment:** This is the most **epistemically robust and valuable contribution** of the entire paper. The elongation of hominin lifespans beyond raw FAD/LAD boundaries is mathematically sound, consistent with taphonomic sampling theory, and restores hominin species durations to normal mammalian longevity distributions.

---

## Collective Summary & Seme Matrix

| Unit ID | Subject / Heading | Asserted Claim | Statistical Reality / Epistemic Ground | Seme Verdict |
|---|---|---|---|---|
| **CR-001** | Clade-Wide Speciation | Negatively diversity-dependent cladogenesis | 95% HPD spans zero ($[-1.97, +0.41]$) in all models | Type II/III Overclaim; Null model ($G_l = 0$) unrejected |
| **CR-002** | *Homo* Speciation Rate | Positively diversity-dependent ("diversity begets diversity") | 95% HPD spans zero ($[-1.80, +6.24]$); 60.5% occurrences from top-3 late taxa | Precocious Promotion; Unpowered MCMC ($N=7$) |
| **CR-003** | *Homo* Extinction Rate | Negatively diversity-dependent extinction | Significant in PyRate ($95\%\text{ HPD} = [-10.82, -4.61]$), but reflects Late Pleistocene coeval replacement | Taphonomic Edge Artifact / Synchronized Demographic Event |
| **CR-004** | Phylogeny & Tip DR | Tip DR confirms positive diversity correlation | Tip DR algebraically dominated by short terminal branches ($1/l_1$); sensitive to polytomies | Topological / Temporal Edge Artifact |
| **CR-005** | Ecological Narratives | Fire, tools, and niche construction explain positive $G_l$ | Plausible biological mechanisms invoked to explain an unverified empirical parameter | Ricardian Just-So Storytelling |
| **CR-006** | Lifespan Estimation | Preservation conditioning extends hominin durations by ~0.5 Myr | Taphonomically sound; restores durations to mammalian average (~1.0 Myr) | Epistemically Sound & Valid Contribution |
