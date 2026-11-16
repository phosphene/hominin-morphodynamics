# Mathematical Genealogy, Numerical Challenges & Scoping Bounds of the Six Core Primitives

**Document Coordinate:** `docs/PRIMITIVES_GENEALOGY_NUMERICAL_CHALLENGES_AND_SCOPING.md`  
**Repository:** `phosphene/hominin-morphodynamics`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Canonical Methodological Foundation & Legibility Specification  
**Date:** 2026-11-16  

---

## 1. Architectural Purpose and Scoping Legibility

In quantitative paleobiology and hominin evolutionary ecology, high-level diversification claims—such as whether *Homo* broke diversity-dependent niche saturation—frequently collapse not because of ideological disputes, but because the underlying mathematical equations were implemented with uninspected numerical pathologies or scoped far beyond their physical domain.

This document establishes the **genealogical lineage, mathematical formulation, numerical implementation hazards, and physical scoping limits** for each of our six core primitives in `hominin_morphodynamics.inference.primitives`.

Every primitive must make its mathematical ancestry explicit, isolate its numerical failure modes (catastrophic cancellation, overflow, underflow, singularities), and state exactly what it cannot infer.

---

## 2. Primitive 1: Exponential Diversity-Dependent Hazard

* **Code Coordinate:** `log_diversity_hazard`, `diversity_dependent_hazard`

### A. Intellectual Genealogy
* **P. F. Verhulst (1838) & Raymond Pearl (1920):** Logistic population regulation where growth slows as density approaches carrying capacity $K$.
* **M. S. Bartlett (1949, 1955):** Formalized non-linear, density-dependent transition hazards in continuous-time Markov population processes.
* **R. H. MacArthur & E. O. Wilson (1967):** *The Theory of Island Biogeography*. Introduced ecological niche saturation into macroevolutionary colonization and speciation rates.
* **Rampal S. Etienne et al. (2012):** "A New Dynamic Neutral Theory for a Finite World" (*Am. Nat.*). Formulated exact diversity-dependent diversification likelihoods under linear and exponential decay.
* **Daniele Silvestro et al. (2014, 2019):** Integrated exponential diversity dependence into the fossilized birth-death MCMC engine (PyRate Continuous):
  $$\lambda(D) = \lambda_0 \exp(G_l \cdot D)$$
  $$\mu(D) = \mu_0 \exp(G_m \cdot D)$$
* **Laura van Holstein & Robert A. Foley (2024):** Applied this exact formulation to test whether *Homo* speciation hazard accelerates ($G_l > 0$) rather than decelerates ($G_l < 0$) with species richness.

### B. Mathematical Formulation
$$\lambda(D) = \lambda_0 \cdot \exp(G_l \cdot D)$$
$$\ln \lambda(D) = \ln \lambda_0 + G_l \cdot D$$
Where:
* $\lambda_0 > 0$: Baseline speciation hazard at zero standing diversity.
* $D \ge 0$: Integer count or continuous expectation of contemporaneous standing diversity.
* $G_l \in \mathbb{R}$: Diversity-dependence scaling coefficient.

### C. Numerical Implementation Difficulties & Defensive Engineering
1. **Exponential Overflow / Underflow in Natural Scale:**
   Evaluating $\lambda_0 \exp(G_l \cdot D)$ directly in natural scale quickly triggers IEEE 754 floating-point overflow (`+inf` for large positive $G_l \cdot D$) or unrecoverable denormalized underflow (`0.0` for negative $G_l \cdot D$).
   * *Defense:* Implement the primitive primarily in log-space: $\ln \lambda = \ln \lambda_0 + G_l \cdot D$.
   * *Clamping:* Apply symmetric bounds on the exponent ($G_l \cdot D \in [-50.0, +50.0]$) prior to exponentiation. An exponent of $\pm 50$ represents a $10^{\pm 21}$ rate multiplier, well outside biological feasibility while remaining securely within 64-bit float limits ($\approx 10^{\pm 308}$).
2. **Gradient Vanishing / Exploding in MCMC Proposals:**
   Because the derivative $\frac{\partial \lambda}{\partial G_l} = D \lambda_0 \exp(G_l \cdot D)$ scales exponentially, unbounded MCMC random-walk proposals for $G_l$ jump between near-zero gradients and extreme likelihood cliffs.
   * *Defense:* MCMC samplers must use Hamiltonian Monte Carlo (HMC) with analytical log-space Jacobians or adaptive step sizes conditioned on $D_{\max}$.

### D. Physical and Evidentiary Scoping Bounds
* **What it CAN infer:** Whether, within a single closed ecological guild and bounded geographical basin, an increase in co-occurring lineages correlates with a change in the observed tempo of lineage branching.
* **What it CANNOT infer:**
  1. *Causal Agency:* It cannot prove that species *caused* other species to form. A positive correlation ($G_l > 0$) can be driven entirely by external environmental forcing (e.g., climate-driven habitat fragmentation increasing both allopatric splitting and site preservation simultaneously).
  2. *Global Clade Dynamics from $N \le 10$:* Estimating an exponential feedback parameter on a clade with only 7 to 17 total species over 4 million years has insufficient degrees of freedom to decouple $G_l$ from baseline rate $\lambda_0$.

---

## 3. Primitive 2: Keiding Preservation Conditioning Probability

* **Code Coordinate:** `keiding_sampling_probability`, `keiding_log_conditioning`

### A. Intellectual Genealogy
* **Niels Keiding (1975):** "Maximum Likelihood Estimation in the Birth-and-Death Process" (*Annals of Statistics*). Identified the foundational observational truncation defect of historical birth-death processes: lineages that lived and died without leaving an observation are truncated from the sample register.
* **David M. Raup (1972, 1976):** Demonstrated that raw fossil counts are heavily truncated by the volume of exposed rock and sediment facies.
* **Michael Foote (1997):** "Estimating Taxonomic Durations and Preservation Probability" (*Paleobiology*). Formulated continuous-time Poisson preservation probabilities over stratigraphic intervals.
* **Charles R. Marshall (1990, 1997):** Confidence intervals on fossil ranges conditioned on non-zero sampling density.

### B. Mathematical Formulation
Let $\theta = \int_e^s q(t) \, dt$ be the expected number of preserved fossil occurrences for a lineage spanning speciation time $s$ and extinction time $e$ under preservation rate $q(t)$.

Under an inhomogeneous Poisson process, the probability of sampling $K$ fossils is $\text{Poisson}(K \mid \theta)$. The probability that a lineage is sampled at least once ($K \ge 1$) is:
$$P(K \ge 1 \mid s, e, q) = 1 - \exp(-\theta)$$
In log-space:
$$\ln P(K \ge 1 \mid s, e, q) = \ln(1 - \exp(-\theta))$$

### C. Numerical Implementation Difficulties & Defensive Engineering
1. **Catastrophic Cancellation for Small Sampling Hazards ($\theta \ll 1$):**
   In poorly preserved fossil horizons or for short-lived lineages, $\theta = q \cdot \Delta t$ can be very small (e.g., $\theta = 10^{-6}$ or $10^{-14}$).
   Naive calculation in standard floating-point arithmetic:
   ```python
   # CATASTROPHIC FAILURE:
   1.0 - math.exp(-1e-15)  # Evaluates to 0.0 or loses 14 digits of precision!
   math.log(1.0 - math.exp(-1e-15))  # Returns -inf (division by zero / domain error)!
```
   * *Defense:* Use IEEE 754 kernel primitives specifically engineered for $e^x - 1$:
     $$1 - \exp(-\theta) = - \text{expm1}(-\theta)$$
     $$\ln(1 - \exp(-\theta)) = \ln(- \text{expm1}(-\theta))$$
     For small $\theta$, $-\text{expm1}(-\theta) \approx \theta$, preserving full 53-bit mantissa precision down to $10^{-16}$.
2. **Boundary Discontinuity at $\theta = 0$:**
   If a lineage has duration zero ($s = e$) or preservation is zero ($q = 0$), $P(K \ge 1) = 0$, and log-probability is $-\infty$. The code must explicitly catch $\theta \le 0$ and return $-math.inf$ without throwing runtime floating-point exceptions.

### D. Physical and Evidentiary Scoping Bounds
* **What it CAN infer:** The exact Bayesian conditioning factor required to prevent survival bias in lineage duration estimates.
* **What it CANNOT infer:**
  1. *Uniform Preservation Across Lithologies:* Keiding conditioning assumes that within the duration $[e, s]$, sampling follows a Poisson hazard. It breaks down if preservation is strictly episodic (e.g., zero preservation for 500 kyr across an unconformity, followed by a single catastrophic volcanic ash burial).
  2. *Taxonomic Discoverability:* It models the physical preservation of a bone, not the probability that a field paleontologist recognizes it as a distinct species rather than an unidentifiable fragment.

---

## 4. Primitive 3: Inhomogeneous Poisson Occurrence Likelihood

* **Code Coordinate:** `poisson_occurrence_loglik`

### A. Intellectual Genealogy
* **Siméon Denis Poisson (1837):** Probability distribution of rare, independent events in a continuous continuum.
* **David M. Raup, S. J. Gould, D. S. Schopf, & D. S. Simberloff (1973):** "Stochastic Models of Phylogeny and the Evolution of Diversity" (*J. Geology*). Established stochastic simulation of fossil occurrence records.
* **Charles R. Marshall (1990):** Range-extension equations based on Poisson distribution of fossil horizons.
* **Daniele Silvestro et al. (2014):** Formalized the continuous Poisson occurrence likelihood for fossil occurrences embedded within MCMC range estimations.

### B. Mathematical Formulation
Given a lineage active on interval $[e, s]$ (with $s \ge e \ge 0$ in Ma) and a set of $k$ distinct fossil occurrence dates $t_1, t_2, \dots, t_k \in [e, s]$:
$$L(t_{1\dots k} \mid s, e, q) = \left( \prod_{j=1}^k q(t_j) \right) \exp\left( - \int_e^s q(t) \, dt \right)$$
In log-space under piecewise-constant or homogeneous preservation $q$:
$$\ln L(t_{1\dots k} \mid s, e, q) = k \ln q - q \cdot (s - e)$$

### C. Numerical Implementation Difficulties & Defensive Engineering
1. **Lifespan Enclosure Violations (Temporal Leakage):**
   In MCMC proposals for speciation time $s$ or extinction time $e$, proposed boundaries can cross observed fossil dates (i.e., proposing $s < \max(t_j)$ or $e > \min(t_j)$). A fossil cannot physically predate its lineage's origin or postdate its extinction.
   * *Defense:* Strict invariant assertion $e \le t_j \le s \ \forall j$. Any proposal violating this boundary has probability zero ($L = 0 \implies \ln L = -\infty$).
2. **Log-Zero Singularities ($q \le 0$):**
   Preservation rate $q$ must be strictly positive ($q > 0$). If $q \to 0$, $k \ln q \to -\infty$. Ingestion layers must enforce strictly positive priors on preservation intensity.

### D. Physical and Evidentiary Scoping Bounds
* **What it CAN infer:** The joint likelihood of observing $k$ fossil horizons given proposed origination and extinction boundaries under a specified sampling rate.
* **What it CANNOT infer:**
  1. *Horizon Independence:* Real fossil occurrences cluster in discrete depositional bonebeds or volcanic tuffs. Ten fossil fragments recovered from a single cave layer are not ten independent Poisson draws over time; treating them as such artificially inflates $q$ and drastically underestimates age uncertainty.
  2. *Reworking and Taphonomic Transport:* It assumes that fossil age $t_j$ is the true biological death date, ignoring stratigraphic infiltration or hydraulic redeposition of older fossils into younger beds.

---

## 5. Primitive 4: Continuous Lineage Duration and Extinction Density

* **Code Coordinate:** `lineage_duration_loglik`

### A. Intellectual Genealogy
* **David G. Kendall (1948):** Continuous-time Markov formulation of lineage termination hazards.
* **John R. Leighly (1928) & W. A. Thompson (1988):** Classical survival analysis and hazard density modeling.
* **Tanja Stadler (2010):** "Sampling-Through-Time in Birth-Death Trees" (*J. Theor. Biol.*). Established modern time-calibrated survival conditioning for tip dating and fossilized birth-death processes.

### B. Mathematical Formulation
For a lineage originating at speciation time $s_i$ and terminating at extinction time $e_i$:

1. **Cumulative Survival Function:**
   $$S(s_i, e_i) = \exp\left( - \int_{e_i}^{s_i} \mu(t) \, dt \right)$$
   $$\ln S(s_i, e_i) = - \int_{e_i}^{s_i} \mu(t) \, dt \approx - \mu_{\text{mean}} \cdot (s_i - e_i)$$

2. **Extinction Event Likelihood:**
   * If extinct ($e_i > 0$): The event density is the survival probability multiplied by the instantaneous hazard at death $\mu(e_i)$:
     $$\ln L_{\text{dur}} = \ln \mu(e_i) - \mu_{\text{mean}} \cdot (s_i - e_i)$$
   * If extant ($e_i = 0$): The lineage has survived to the present without terminating; the likelihood is purely survival:
     $$\ln L_{\text{dur}} = - \mu_{\text{mean}} \cdot s_i$$

### C. Numerical Implementation Difficulties & Defensive Engineering
1. **The Extant Lineage Boundary Discontinuity at $e = 0$:**
   In fossil clades, extant taxa (e.g., *Homo sapiens* at $e = 0$) must not be evaluated as having undergone an extinction event at time 0. Adding $\ln \mu$ to an extant lineage treats survival to the present as an extinction pulse.
   * *Defense:* Explicit boolean branch `is_extinct` or check $e == 0.0$ routing to the pure survival term without $\ln \mu$.
2. **Negative Duration Invariants:**
   Any state where $s < e$ represents an unphysical time inversion (extinction predating origination). The primitive must immediately raise an error or return $-\infty$.

### D. Physical and Evidentiary Scoping Bounds
* **What it CAN infer:** The likelihood of observed lineage longevities under an assumed background extinction hazard.
* **What it CANNOT infer:**
  1. *Pseudoextinction vs. True Lineage Termination:* In paleoanthropology, *Homo erectus* "extinction" at $\sim 0.1\text{ Ma}$ may represent anagenetic transformation into younger descendants or local regional replacement rather than true biological clade death.
  2. *Mass Extinction Pulses:* A continuous-time hazard $\mu$ cannot distinguish between steady background mortality and an instantaneous catastrophic extinction event without discrete time-slice parameterization.

---

## 6. Primitive 5: Standing Diversity Step-Function Trajectory

* **Code Coordinate:** `standing_diversity_trajectory`

### A. Intellectual Genealogy
* **J. J. Sepkoski, Jr. (1978, 1981):** "A Factor Analytic Description of the Phanerozoic Marine Fossil Record" (*Paleobiology*). Pioneered global standing diversity curves constructed from stratigraphic boundary crossings.
* **Michael J. Benton (1995):** Diversification of continental vertebrates; standing richness across geological stages.
* **John Alroy (2000, 2008):** "Dynamics of Origination and Extinction in the Marine Fossil Record" (*PNAS*). Addressed the "range-through" artifact where diversity is artificially inflated by assuming continuous presence between first and last appearances.

### B. Mathematical Formulation
Given $M$ lineages with lifespans $[e_i, s_i]$ ($i = 1, \dots, M$), the standing diversity $D(t)$ at any arbitrary continuous time $t \ge 0$ is the exact sum of indicator functions:
$$D(t) = \sum_{i=1}^M \mathbb{I}(e_i \le t \le s_i)$$
Where:
$$\mathbb{I}(e_i \le t \le s_i) = \begin{cases} 1 & \text{if } s_i \ge t \ge e_i \\ 0 & \text{otherwise} \end{cases}$$

### C. Numerical Implementation Difficulties & Defensive Engineering
1. **Discretization and Binning Errors:**
   Many legacy pipelines evaluate diversity by rounding occurrences into coarse 1.0 or 0.5 Myr time bins. This creates severe boundary edge effects (smearing short-lived taxa into adjacent bins or creating artificial diversity spikes at bin boundaries).
   * *Defense:* Vectorized numpy broadcasting against exact closed intervals $[e_i, s_i]$:
     ```python
     mask = (eval_times <= s_i) & (eval_times >= e_i)
     counts[mask] += 1
     ```
     This produces an exact continuous step function without binning artifacts.
2. **Support Boundary Bounds:**
   $D(t)$ must evaluate to strictly non-negative integers ($D(t) \in \{0, 1, 2, \dots\}$) and must be identically zero for all $t > \max(s_i)$ and $t < \min(e_i)$.

### D. Physical and Evidentiary Scoping Bounds
* **What it CAN infer:** The theoretical standing diversity trajectory of a clade given a set of proposed origination and extinction boundaries.
* **What it CANNOT infer:**
  1. *Empirical Realized Richness:* The "range-through" assumption assumes that a lineage is continuously present across its entire span. If *Homo erectus* was absent from East Africa for 400 kyr while surviving in Java, range-through counting treats it as standing African diversity.
  2. *Geographic Sympatry:* Lineages active at the same time $t$ may have been isolated on different continents (e.g., *H. floresiensis* in Indonesia and *H. neanderthalensis* in Europe). Global $D(t)$ does not represent local ecological competition.

---

## 7. Primitive 6: Regularized Tip Diversification Rate (DR) Metric

* **Code Coordinate:** `tip_diversification_rate`

### A. Intellectual Genealogy
* **Daniel P. Faith (1992):** "Conservation Evaluation and Phylogenetic Diversity" (*Biol. Conserv.*). Established branch-length weighting of evolutionary history.
* **C. M. Steel (1993):** Equal-splits measure for distributing phylogenetic diversity along trees.
* **Walter Jetz, G. H. Thomas, J. B. Joy, K. Hartmann, & A. O. Mooers (2012):** "The Global Diversity of Birds in Space and Time" (*Nature*). Introduced the tip Diversification Rate (DR) metric as an inverse measure of terminal and ancestral branch lengths.
* **Laura van Holstein & Robert A. Foley (2024):** Used DR calculated from the Parins-Fukuchi (2019) hominin tree as the dependent variable in phylogenetic regressions against species richness.

### B. Mathematical Formulation
For tip $i$ on a rooted phylogenetic tree, let $l_1, l_2, \dots, l_N$ be the sequence of ancestral branch lengths from the tip to the root ($l_1$ is the terminal branch length, $l_2$ is its immediate ancestral parent, etc.). The DR metric is:
$$\text{DR}_i = \sum_{j=1}^N \left(\frac{1}{2}\right)^{j-1} \frac{1}{l_j} = \frac{1}{l_1} + \frac{1}{2 l_2} + \frac{1}{4 l_3} + \dots + \frac{1}{2^{N-1} l_N}$$

### C. Numerical Implementation Difficulties & Defensive Engineering
1. **The Polytomy / Zero-Branch Singularity ($\lim_{l_j \to 0} \text{DR} = \infty$):**
   Phylogenetic trees estimated from morphology often contain near-zero internal branch lengths where rapid cladogenesis or missing data prevents resolving hard polytomies.
   * *The Published Defect:* In the Parins-Fukuchi (2019) tree used by Van Holstein & Foley, the ancestral node between *A. anamensis* and the *Ardipithecus* / *A. afarensis* split has a branch length of:
     $$l_j = 4.82458517581 \times 10^{-12} \text{ Myr}$$
     Evaluating unregularized DR on this tree causes $\text{DR}_{\text{Ardi}}$ to explode to:
     $$\text{DR}_{\text{Ardi}} \approx \frac{1}{2 \times 4.82 \times 10^{-12}} \approx 1.04 \times 10^{11}$$
     This single numerical explosion completely distorted their regression, forcing Foley to manually drop *Ardipithecus* from their R script (`data_noardi <- data[-1, ]`).
   * *Defense:* Implement an explicit branch-length regularization floor $\epsilon > 0$ (`min_branch_length = 1e-4` Myr):
     $$l_j^{\text{reg}} = \max(\epsilon, l_j)$$
     This bounds DR to finite values and prevents near-zero machine-precision artifacts from generating massive false-positive diversification spikes.
2. **Strict Monotonicity:**
   DR must be strictly monotonically decreasing with branch lengths: doubling all branch lengths must halve DR.

### D. Physical and Evidentiary Scoping Bounds
* **What it CAN infer:** A heuristic summary metric of how recently and frequently lineage branching occurred along a tip's ancestral path.
* **What it CANNOT infer:**
  1. *True Instantaneous Speciation Rates:* DR is a metric of tree shape, not a mechanistic speciation rate. It conflates rapid speciation with low extinction, and is heavily distorted by incomplete taxon sampling (missing fossil tips artificially inflate ancestral branch lengths, artificially depressing DR).
  2. *Direction of Causation:* Correlating DR with historical species richness does not prove that richness drove diversification; it merely shows that lineages on bushy parts of a tree have shorter branch lengths.

---

## 8. Summary Audit Matrix: Legibility and Safeguards

```
PRIMITIVES LEGIBILITY AND DEFENSIVE REHEARSAL MATRIX
┌───────────┬───────────────────────────────┬───────────────────────────────┬──────────────────────────────────┐
│ Primitive │ Canonical Precursors          │ Numerical Traps               │ Engineering Safeguards           │
├───────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ 1: Hazard │ Verhulst (1838), Silvestro    │ Exponential overflow (+inf),  │ Log-space evaluation; symmetric  │
│           │ et al. (2014), Foley (2024)   │ denormalized underflow (0.0)  │ clamping exponent to [-50, +50]  │
├───────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ 2: Keiding│ Keiding (1975), Foote (1997), │ Catastrophic cancellation in  │ IEEE 754 expm1/log1p kernels:    │
│           │ Raup (1972)                   │ 1 - exp(-theta) for theta<<1  │ -expm1(-theta); log(-expm1)      │
├───────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ 3: Poisson│ Poisson (1837), Raup (1973),  │ Temporal leakage (t outside   │ Strict [e, s] boundary gating;   │
│           │ Silvestro et al. (2014)       │ lifespan); ln(0) on q <= 0    │ enforce positive priors on q     │
├───────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ 4: Survival│ Kendall (1948), Stadler (2010)│ Extant taxa evaluated as      │ Explicit is_extinct branch gating│
│           │                               │ extinct at t=0 (false pulse)  │ routing to pure survival term    │
├───────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ 5: D(t)   │ Sepkoski (1978), Alroy (2000) │ Time-bin smearing artifacts;  │ Vectorized step-function array   │
│           │                               │ boundary leakage              │ over exact closed [e, s] bounds  │
├───────────┼───────────────────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ 6: DR     │ Jetz (2012), Faith (1992),    │ Polytomy singularity (1/0) on │ Regularization floor (eps > 0);  │
│           │ Parins-Fukuchi (2019)         │ near-zero internal branches   │ prevents 10^11 outlier explosions│
└───────────┴───────────────────────────────┴───────────────────────────────┴──────────────────────────────────┘
```
