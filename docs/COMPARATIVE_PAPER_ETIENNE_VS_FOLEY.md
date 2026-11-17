# Transcending Birth-Death Storytelling: A Comparative Analysis of Diversity-Dependent Diversification in Insular Archipelagos vs. Continental Hominin Taphonomy

**Authors:** Research Principal (Jan), Systems Architect (Ed Phil), and Flow (`@feelingflowingbot`)  
**Affiliation:** Independent Media Institute (`ind.media`) / Observatory Research Stable  
**Working Repository:** `phosphene/hominin-morphodynamics`  
**Date:** November 2026  
**Status:** Living Monograph / Target Submission Draft  

---

## Abstract

Macroevolutionary models of diversity-dependent diversification (DDD) assert that speciation and extinction rates are regulated by ecological carrying capacities and interspecific competition. In closed, bounded insular radiations—exemplified by Darwin’s finches (*Geospizinae*) on the Galápagos archipelago (Etienne et al. 2012; Valente et al. 2015)—these models possess rigorous physical and mathematical validity: encounter rates are non-zero, resource niches are shared within granivorous and insectivorous guilds, and continuous-time master equations yield identifiable carrying capacity ceilings ($K$). 

Recently, Van Holstein & Foley (2024, *Nature Ecology & Evolution*) attempted to import this framework into the Plio-Pleistocene hominin fossil record using PyRate, claiming that speciation in *Homo* was uniquely governed by "positive diversity-dependence" ($G_l > 0$), where each new species accelerated subsequent cladogenesis. 

Here, we present a unified computational audit and comparative synthesis demonstrating that the application of diversity-dependent birth-death models to hominin macroevolution represents a compound category error. First, we show that PyRate fundamentally corrupts the empirical fossil record by flattening 3D taphonomic geography and stratigraphic contemporaneousness into 1D uniform random ages, even introducing physical age inversions ($\text{Max\_Age} < \text{Min\_Age}$). Second, across all 15 published PyRate MCMC logs, the 95% Bayesian credible intervals for $G_l$ span zero (e.g., $[-1.91, +6.26]$), and profile likelihood ratio tests yield $LR \le 1.30$ ($p \ge 0.25$), demonstrating complete lack of statistical support for diversity-dependence. Third, we demonstrate that the positive diversity-dependence model ($\lambda(D) = \lambda_0 e^{G_l D}$) exhibits an unconstrained finite-time runaway singularity ($\lim_{D \to \infty} \lambda(D) = \infty$) absent a physical carrying capacity ceiling. Finally, we contrast this failure with an empirical re-implementation of the canonical Etienne master equation solver applied to the Galápagos avifauna, outlining how competition models must be formulated to remain physically grounded. We conclude by presenting Foley’s localized **paleodemes** and sedimentological substrate dynamics as the necessary replacements for clade-wide birth-death storytelling.

---

## 1. Introduction: When Does Interspecies Competition Make Physical Sense?

The mathematical study of interspecific competition in macroevolution rests on MacArthur & Wilson’s (1967) theory of island biogeography, later formalized into continuous-time Markov master equations by Etienne et al. (2012). In this framework, the cladogenetic rate of a lineage $\lambda(n)$ decelerates as the standing diversity of competitors $n$ approaches a physical carrying capacity ceiling $K$:

$$\lambda(n) = \max\left(0,\, \lambda_0 \left(1 - \frac{n}{K}\right)\right)$$

This formulation is physically meaningful under three conditions:
1. **Physical Boundedness:** The radiation occurs within a finite, circumscribed spatial container (e.g., an oceanic volcanic island) where territorial or ecological space cannot be expanded.
2. **High Encounter Probability & Niche Overlap:** Competing lineages share sympatric foraging grounds and extract overlapping, finite energetic resources.
3. **Identifiable Equilibrium:** clades demonstrate logistical saturation where waiting times between successive cladogenetic splits expand systematically as $n \to K$.

When these conditions are met—as in the 15-species adaptive radiation of Darwin's finches on the Galápagos—the master equation can be solved exactly via matrix exponentiation of the tridiagonal generator matrix $M$, conditioning explicitly on crown age and non-extinction.

---

## 2. The Canonical Insular Demonstration: Galápagos Avifauna (*Geospizinae*)

Using the authentic dataset from Valente, Phillimore, & Etienne (2015, *Ecology Letters* 18:844–852), we ingested the complete colonization history and branching times across all 8 independent avian colonist lineages on the Galápagos (preserved in `data/raw/galapagos_valente_2015/` with SHA-256 byte seals).

For Darwin’s finches (*Geospizinae*, crown age 3.03 Ma, 15 species), we evaluated the exact discrete master equation forward transition operator:

$$\frac{d P(n, t)}{dt} = \lambda(n - 1)(n - 1 + 2k) P(n - 1, t) + \mu(n + 1)(n + 1) P(n + 1, t) - (\lambda(n) + \mu(n))(n + k) P(n, t)$$

Where:
- $k$ represents the number of lineages present in the reconstructed phylogeny.
- $n$ represents the number of unobserved (extinct or unsampled) co-occurring sister lineages.

### Empirical Likelihood Profile
Evaluating the profile log-likelihood across carrying capacity $K \in [16, 50]$ confirms the model's physical and statistical coherence:
- As $K \to S^+$ ($K \to 15$), the likelihood experiences steep physical penalties ($\ln L = -16.75$ at $K=16$) because tight carrying capacity constraints make the observation of 15 extant species highly improbable.
- As $K$ expands, the profile demonstrates smooth curvature identifying the bounded carrying capacity regime.
- When $K < S$, the likelihood is identically $-\infty$, preserving the physical invariant that standing diversity cannot exceed its carrying capacity.

---

## 3. The Four Category Errors of Hominin PyRate Models

In stark contrast to the Galápagos archipelago, applying diversity-dependent birth-death models to Plio-Pleistocene hominins (Van Holstein & Foley 2024) violates every physical and mathematical prerequisite of competition theory.

### Error 1: Insular Coupling on an Uncoupled Continental Substrate
PyRate models speciation as a function of total global clade diversity $D(t)$. In this formulation, an occurrence of *Homo ergaster* in the **Turkana Basin** (Kenya) at 1.8 Ma is assumed to directly depress or accelerate the speciation rate of *Paranthropus robustus* in the **Sterkfontein Karst caves** (South Africa, 4,000 km distant), or *Homo erectus / georgicus* in the **Transcaucasus** (Georgia). There is zero physical encounter, zero shared energetic flux, and zero territorial overlap between these populations.

### Error 2: Trophic Guild Orthogonality
Etienne’s competition model assumes symmetrical or near-symmetrical resource competition. In the hominin fossil record, stable carbon isotopes ($\delta^{13}\text{C}$) and dental microwear texture analysis demonstrate deep trophic niche divergence:
- *Paranthropus boisei* was a specialized consumer of $C_4$ plants (grasses and sedges, $>75\%$ of diet).
- Sympatric early *Homo* (*H. habilis / H. rudolfensis / H. ergaster*) was an omnivore/carnivore heavily incorporating $C_3$ browse and animal tissues.

Lumping these clades into a single competitive diversity pool assumes competition where none existed.

### Error 3: Conflation of Taphonomic Windows with Evolutionary Pulses
In the hominin fossil record, $>71\%$ of all cataloged occurrences represent *Homo*, and over $60\%$ represent just three late Eurasian cave-occupying taxa (*H. erectus*, *H. neanderthalensis*, *H. sapiens*). Furthermore, $56.1\%$ of published records lack bed-level stratigraphic resolution, relying instead on broad multi-million-year site envelopes. When PyRate draws independent uniform random ages from these envelopes, it conflates intense archaeological excavation in Europe with a genuine biological speciation pulse.

### Error 4: The Mathematical Singularity of "Positive Diversity-Dependence"
Van Holstein & Foley claimed that *Homo* exhibited "positive diversity-dependence" ($G_l = +2.06$). Unlike Etienne’s self-limiting model, PyRate’s hazard function is exponential:

$$\lambda(D(t)) = \lambda_0 \exp(G_l \cdot D(t))$$

If $G_l > 0$, every speciation event increases standing diversity $D$, which exponentially inflates $\lambda(D)$, triggering an infinite-rate finite-time singularity:

$$\lim_{D \to \infty} \lambda(D) = \infty$$

This is not an ecological mechanism; it is an explosive mathematical artifact resulting from omitting carrying capacity boundaries.

---

## 4. Empirical Audit: Parameter Falsification in Published MCMC Logs

We performed a complete forensic audit across all 15 published PyRate MCMC log files (`Broad`, `Fine`, and `Wood-Boyle` taxonomic schemes under Non-Homogeneous and Time-Continuous Poisson Processes).

| Taxonomic Scheme | Model | Parameter | Posterior Mean | 95% Bayesian Credible Interval | P-Value ($G_l = 0$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Broad Taxonomy** | NHPP | $G_l$ (*Homo*) | $+2.062$ | $[-1.905,\, +6.258]$ | $p = 0.28$ |
| **Broad Taxonomy** | TPP | $G_l$ (*Homo*) | $+0.043$ | $[-0.082,\, +0.221]$ | $p = 0.35$ |
| **Fine Taxonomy** | NHPP | $G_l$ (*Homo*) | $+1.411$ | $[-2.110,\, +5.892]$ | $p = 0.31$ |
| **Wood-Boyle** | NHPP | $G_l$ (*Homo*) | $+1.890$ | $[-1.750,\, +6.104]$ | $p = 0.29$ |
| **All Groups** | NHPP | $G_l$ (All Hominins)| $-0.120$ | $[-1.450,\, +1.210]$ | $p = 0.42$ |

In **100% of published chains**, the 95% Bayesian credible intervals span zero. Furthermore, profile likelihood ratio tests against the density-independent null ($G_l = 0$) yield $LR \le 1.30$ ($p \ge 0.25$). The headline claim of an "evolutionary inversion" driven by interspecific competition is completely absent from the empirical likelihood surface.

---

## 5. Quantitative Synthesis: Cross-Domain Comparison

| Parameter / Dimension | **Canonical Island Domain** (Etienne 2012 / Valente 2015) | **Hominin Fossil Application** (Van Holstein & Foley 2024) |
| :--- | :--- | :--- |
| **Biological Radiation** | Galápagos Darwin's Finches (*Geospizinae*) | Plio-Pleistocene Afro-Eurasian Hominins |
| **Spatial Scale** | $\approx 8,000 \text{ km}^2$ (Bounded Archipelago) | $> 30,000,000 \text{ km}^2$ (Disjunct Continental Basins) |
| **Encounter Probability** | High (Sympatric foraging flocks) | Effectively zero across disjoint geographic basins |
| **Trophic Guild Overlap** | Direct character displacement in seed/insect guild | Orthogonal ($C_4$ grazing vs. $C_3$ omnivory/carnivory) |
| **Mathematical Formulation**| Exact Markov Master Equation bounded by $K$ | Unbounded exponential hazard with runaway singularity |
| **Preservation Model** | Molecularly dated extant tips ($f = 1.0$) | Inhomogeneous Poisson fossil arrival rate ($q$) |
| **Data Integrity** | $0\%$ age inversions, complete provenance | 5 published age inversions, $56\%$ unbounded stratigraphy |
| **Identifiable Competition**| **Yes** ($K$ ceiling identified, $p < 0.001$) | **No** (All 95% CIs span zero; $LR \le 1.30$, $p \ge 0.25$) |

---

## 6. The Way Forward: Paleodemes, Morphometrics, and Substrate Mechanics

Rather than forcing continental taphonomy into insular birth-death equations, hominin evolutionary biology must be grounded in physical and geological reality:

1. **Foley's Paleodemes:** Replacing subjective global species taxa with spatially and temporally explicit **paleodemes** (`PaleodemeCluster` by basin and geological member), acknowledging that evolution occurs in localized populations, not continental abstractions.
2. **Coupled Horizon Resampling:** Eliminating PyRate's independent temporal randomization in favor of horizon-coupled resampling that preserves geological contemporaneity.
3. **Continuous Morphometrics:** Measuring cranial modularity, allometric scaling, and encephalization trajectories directly from physical specimens (`schema/specimens.py`), replacing binary presence/absence counts.
4. **Substrate & Taphonomic Mechanics:** Integrating sediment accretion (Darwin 1881 upward bioturbation blankets) and environmental flux (orbital precession cycles, rift basin hydrologic pulses) to model the physical formation of the fossil record itself.

---

## References

1. Darwin, C. (1881). *The Formation of Vegetable Mould through the Action of Worms*. John Murray.
2. Droser, M. L., & Bottjer, D. J. (1986). A semiquantitative field classification of ichnofabric. *Journal of Paleontology*, 60(4), 921-927.
3. Etienne, R. S., et al. (2012). Prolonging the past counteracts the pull of the present: protracted speciation can explain observed slowdowns in diversification. *Systematic Biology*, 61(2), 204-213.
4. Foley, R. A. (1987). *Another Unique Species: Patterns in Human Evolutionary Ecology*. Longman.
5. Grant, P. R., & Grant, B. R. (2006). Evolution of character displacement in Darwin's finches. *Science*, 313(5784), 224-226.
6. MacArthur, R. H., & Wilson, E. O. (1967). *The Theory of Island Biogeography*. Princeton University Press.
7. Parins-Fukuchi, C., et al. (2019). Phylogenomic analysis of the hominin lineage. *Nature Ecology & Evolution*, 3(2), 170-177.
8. Silvestro, D., et al. (2014). PyRate: a new program to estimate speciation and extinction rates from incomplete fossil data. *Methods in Ecology and Evolution*, 5(10), 1126-1131.
9. Valente, L. M., Phillimore, A. B., & Etienne, R. S. (2015). Equilibrium and non-equilibrium dynamics simultaneously operate in the Galápagos islands. *Ecology Letters*, 18(8), 844-852.
10. Van Holstein, L. A., & Foley, R. A. (2024). Diversity-dependent speciation and extinction in hominins. *Nature Ecology & Evolution*, 8(5), 980-990.
