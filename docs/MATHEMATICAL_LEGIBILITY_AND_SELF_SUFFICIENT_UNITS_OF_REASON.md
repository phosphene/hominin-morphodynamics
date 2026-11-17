# Mathematical Legibility & Self-Sufficient Units of Reason: An Anti-Oracle Modeling Discipline

**Coordinate:** `docs/MATHEMATICAL_LEGIBILITY_AND_SELF_SUFFICIENT_UNITS_OF_REASON.md`  
**Namespace:** `morphodynamics.epistemics`  
**Authors:** Ed Phil (@edphos), Jan (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Living Methodological Standard & Architectural Contract  
**Date:** 2026-11-17  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. The Pathology of the Computational Oracle

In contemporary computational macroevolution and quantitative paleobiology, mathematical modeling frequently degenerates into an **oracle pattern**:
1. An empirical dataset (often sparse and taphonomically irregular) is fed into a massive third-party package (e.g., PyRate, RevBayes, BEAST).
2. The software executes millions of Markov Chain Monte Carlo (MCMC) iterations, reversible-jump birth-death transitions, gamma-distributed preservation hyperpriors, and boundary imputation matrices.
3. Compute clusters run for 14 hours, and the software outputs a smooth Bayesian posterior violin plot or credible interval.
4. The researcher interprets the posterior distribution as an ecological reality (e.g., "adaptive radiation," "negative diversity-dependent extinction"), without ever knowing **what was actually calculated** or whether the empirical data had any purchase on the model parameters.

### The Consequence:
When the mathematical engine is opaque to the scientists using it:
- **Parameter degeneracies are masked:** Flat likelihood surfaces are smoothed over by strong implicit priors.
- **Data unresponsiveness is hidden:** Seven scattered data points are treated as if they contain sufficient information to constrain a multi-parameter exponential hazard function.
- **Researchers lose evaluative agency:** Because they cannot see the objective function, they cannot distinguish between an empirical signal from nature and a mathematical artifact of their software's numerical kernel.

---

## 2. De-Mystifying the Oracle: The PyRate Case Study

To see how computational opacity hides empirical emptiness, consider diversity-dependent speciation in PyRate (Silvestro et al. 2014, 2019; Van Holstein & Foley 2024).

The model posits that the speciation rate of a lineage varies exponentially with standing lineage diversity $D(t)$:
$$\lambda(t) = \lambda_0 \exp\left(G_l \cdot D(t)\right)$$

Beneath the 10 million MCMC steps, the mathematical core is simply a **classical non-homogeneous Poisson process**. For a clade with $n$ speciation events at observed times $\{t_1, t_2, \dots, t_n\}$ evaluated against a standing diversity trajectory $D(t)$ over total clade lifespan $[0, T]$, the exact log-likelihood function is:

$$\ln L(G_l, \lambda_0) = \sum_{i=1}^n \ln \lambda(t_i) - \int_0^T \lambda(t)\, dt$$

Substituting the rate definition and expanding algebraically:

$$\ln L(G_l, \lambda_0) = n \ln \lambda_0 + G_l \sum_{i=1}^n D(t_i) - \lambda_0 \int_0^T \exp\left(G_l \cdot D(t)\right) dt$$

### The Purchase Analysis:
When written in this legible, closed form, the question of whether the data has purchase becomes immediately transparent:
1. **The Event Term:** $G_l \sum_{i=1}^n D(t_i)$. For the genus *Homo*, $n \approx 7$. That sum is literally **seven numbers added together**.
2. **The Integrated Penalty:** $\lambda_0 \int_0^T \exp(G_l \cdot D(t)) dt$. This simply penalizes the model for time spent in unfulfilled high speciation potential.
3. **The Empirical Purchase:** With only seven events spread across 2.5 million years, varying $G_l$ from $-0.5$ to $+0.5$ alters the log-likelihood by less than $1.0$. The likelihood-ratio test against the null hypothesis $G_l = 0$ yields $p = 0.68$.

**The data has zero purchase on the parameter.**  
When laid out in three lines of transparent algebra, any researcher with a basic grasp of calculus can see instantly that fitting an exponential curve through seven noisy points cannot reject the null. PyRate does not discover an empirical signal that classical math misses; it merely buries the flat likelihood valley under stochastic MCMC sampling that samples the prior.

---

## 3. The Four Criteria for Legible Mathematics

To ensure that every mathematical model developed in the Phosphene ecosystem remains a **self-sufficient unit of reason**, all modeling code and specifications must satisfy four binding criteria:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE FOUR LEGIBILITY CRITERIA                                    │
├─────────────────────────────────┬──────────────────────────────────────────────────────┤
│ 1. Explicit Objective Functions │ State the exact likelihood or loss in closed form    │
│ 2. Dimensional Accounting       │ Explicit physical units attached to all parameters   │
│ 3. Deterministic Profiling      │ Evaluate profile likelihoods before stochastic MCMC  │
│ 4. The Caliper and Dirt Test    │ Every variable maps to a direct physical observable  │
└─────────────────────────────────┴──────────────────────────────────────────────────────┘
```

---

### Criterion 1: Expose the Explicit Objective Function
- **Contract:** Never state "we estimated parameter $\theta$ using package $X$." Always write down the exact mathematical objective function being optimized or integrated:
  $$\mathcal{L}(\theta) = f(\text{Data} \mid \theta)$$
- **Rule of Thumb:** If the likelihood function, residual sum of squares, or variational bound cannot be written out explicitly in clean mathematical notation within four lines, the modeling team does not understand what the code is doing.

### Criterion 2: Explicit Dimensional Accounting
- **Contract:** Every variable, parameter, and constant must have an explicit dimensional unit that is preserved through every step of algebraic derivation and code execution.
- **Example:**
  - Baseline rate: $\lambda_0 \in [\text{events} \cdot \text{lineage}^{-1} \cdot \text{Myr}^{-1}]$
  - Diversity-dependence slope: $G_l \in [\text{lineage}^{-1}]$ (fractional change in hazard per co-occurring species)
  - Standing diversity: $D(t) \in [\text{lineages}]$
- **Axiomatic Invariant:** Dimensionless proxy indices whose units mutate inside nested loops are strictly prohibited. The product $G_l \cdot D(t)$ must be strictly dimensionless before exponentiation.

### Criterion 3: Closed-Form & Deterministic Profiling Before Stochastic Sampling
- **Contract:** Before launching any stochastic Bayesian sampler, MCMC chain, or variational approximation, the researcher must calculate and inspect the **deterministic profile likelihood surface** or analytical least-squares landscape.
- **Epistemic Invariant:** If the deterministic likelihood surface is flat, ridge-shaped, or exhibits multiple local optima across empirical data, an MCMC chain will not "solve" the problem. It will simply wander across the unconstrained valley and report the shape of the prior distribution.

### Criterion 4: The Caliper and Dirt Test (J.O. Wisdom Standard)
- **Contract:** Inspired by J.O. Wisdom's analysis of Darwin (1881) on earthworms, every parameter in an empirical equation must map to an actual physical observable:
  - Darwin: $w_{\text{yd}}$ (pounds of dirt weighed on a balance) $\to$ bulk displacement $\to$ compaction factor $\to$ decadal accretion depth measured with a wooden ruler.
  - Cambrian substrate: Burrow diameter $2r$ measured with a caliper on a rock slab $\to$ penetration depth $Z_{\max}$ $\to$ diagenetic biodiffusion coefficient $D_b$.
  - Morphodynamics: Craniodental osteometric caliper distances on homologous landmarks $\to$ allometric residual variance $\to$ sympatric mammalian extinctability survival curves.
- **Negative Invariant:** No model may introduce a parameter that is a proxy of a proxy (e.g., an imputed lineage count derived from an arbitrary Linnaean species name mapped across an unmodeled continental grid).

---

## 4. Operational Invariant for Code Review

Every mathematical PR in `hominin-morphodynamics` must include a literate documentation section containing:
1. The analytical closed-form objective function.
2. A table of dimensional units for all symbols.
3. A profile likelihood plot or grid confirming that the empirical data possesses sufficient purchase ($\Delta \ln L \ge 1.92$ for 95% confidence) to constrain the free parameters above the null hypothesis.
4. Proof that the parameters satisfy the Caliper and Dirt Test.
