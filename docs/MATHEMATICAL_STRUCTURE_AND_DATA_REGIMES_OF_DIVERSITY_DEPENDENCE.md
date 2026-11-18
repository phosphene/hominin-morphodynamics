# Mathematical Structure and Data Regimes of Diversity Dependence

**Coordinate:** `docs/MATHEMATICAL_STRUCTURE_AND_DATA_REGIMES_OF_DIVERSITY_DEPENDENCE.md`  
**Namespace:** `morphodynamics.canonics`  
**Authors:** Ed Phil (@edphos), Marsyas (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Mid-Level Technical Evaluation & Data-Regime Specification  
**Date:** 2026-11-18  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. Scope & Objective

This document formalizes the mid-level technical argument regarding diversity-dependent diversification (DDD): **under what mathematical structure and empirical data regime does the claim of diversity dependence possess empirical meaning?**

It evaluates the mathematical requirements for parameter identifiability independently of secondary narrative interpretations, establishing the boundary between regimes where carrying capacity $K$ is solvable and regimes where the likelihood surface is uninformative.

---

## 2. The Core Mathematical Argument

The diversity-dependence hypothesis asserts that the per-lineage speciation rate $\lambda$ is negatively regulated by standing lineage richness $N$:

$$\frac{\partial \lambda}{\partial N} < 0$$

Under the canonical linear formulation (Etienne et al. 2012), this rate is governed by a state-dependent hazard:

$$\lambda(N_t) = \max\left(0, \, \lambda_0 \left(1 - \frac{N_t}{K}\right)\right)$$

where:
- $\lambda_0$ is the baseline speciation rate in uncolonized or unsaturated ecospace ($N_t \to 0$).
- $K \in \mathbb{N}$ is the discrete carrying-capacity ceiling where cladogenetic speciation terminates ($\lambda(K) = 0$).
- $\mu_0$ is the background extinction rate: $\mu(N_t) = \mu_0$.

To test this hypothesis against empirical data, the likelihood of an observed sequence of waiting times:

$$\Delta t_k = t_{k-1} - t_k$$

must be computed across successive cladogenetic events under the forward Chapman-Kolmogorov master equation for the probability distribution $P(n, t)$:

$$\frac{d p_n(t)}{dt} = \lambda(n-1) p_{n-1}(t) + \mu(n+1) p_{n+1}(t) - [\lambda(n) + \mu(n)] p_n(t)$$

Between observed split horizons $t_k$ and $t_{k-1}$, the probability vector $\mathbf{p}(t)$ evolves via matrix exponentiation:

$$\mathbf{p}(t_{k-1}) = \exp\left(\mathbf{M} \cdot (t_k - t_{k-1})\right) \cdot \mathbf{p}(t_k)$$

and is updated at the split horizon by the speciation rate vector:

$$p_n(t_{k-1}^+) = \lambda(n) \cdot p_n(t_{k-1}^-)$$

---

## 3. The Strict Data Requirements for Identifiability

For the parameter triplet $(\lambda_0, \mu_0, K)$ to be mathematically identifiable from empirical data, the dataset must satisfy two physical and statistical conditions:

1. **A Known, Dense Sequence of State Transitions:**  
   The observation vector must contain sufficiently many branching horizons $\{t_1, t_2, \dots, t_S\}$ across varying richness levels $N$ such that the progressive lengthening of waiting intervals $\Delta t$ as $N \to K$ can be statistically distinguished from pure Poisson process stochasticity.
2. **A Bounded, Accounted-for Lineage Pool:**  
   If lineages enter or leave unobserved without bounded constraints (e.g., severe taphonomic truncation or arbitrary geographic cutoffs), standing diversity $N_t$ is unobserved at time $t$. An unobserved state variable $N_t$ prevents exact computation of the transition matrix $\mathbf{M}(N_t)$.

---

## 4. Evaluation Across Two Empirical Data Regimes

| Technical Dimension | Regime A: Galápagos Insular Avifauna | Regime B: Continental Hominin Fossil Record |
|---|---|---|
| **System Domain** | Closed volcanic archipelago ($A \approx 8,000\text{ km}^2$, $1,000\text{ km}$ offshore) | Open continental landmass (Africa + Eurasia, $A \approx 84,000,000\text{ km}^2$) |
| **Initial Boundary** | Hard subaerial volcanic emergence ($t=0, N=0$ at $\approx 4.0\text{ Ma}$) | Continuous catarrhine primate occupation for $>55\text{ Ma}$ (no $t=0$) |
| **Observation Type** | Molecular gene coalescence of living biological species | Taphonomic discovery of fossil fragments in sedimentary beds |
| **Sampling Completeness** | **$100\%$** ($25/25$ extant species sampled, $0$ missing) | **$< 5\%$** estimated preservation of true biological paleospecies |
| **Data Vector** | $15$ exact branching times for finches packed into $3.0\text{ Myr}$ | $17$ morphospecies across $6.0\text{ Myr}$ (avg. $1.8$ species/horizon) |
| **Waiting Times ($\Delta t$)** | Biological evolutionary tempo between reproductive splits | Sediment thickness and erosional exposure between fossil beds |
| **Profile Likelihood Surface** | **Curved with sharp global maximum** ($\Delta \ln L > 5.0$, $K \approx 15\text{–}23$) | **Completely flat** ($\Delta \ln L \le 0.35, p \ge 0.25$ across all $K$ and $G_l$) |
| **Parameter Solvability** | **Identifiable:** Data contains statistical mass to constrain $K$ | **Unidentifiable:** Data is statistically silent between models |

---

## 5. Epistemic Assessment

- In **Regime A (Galápagos)**, the model parameters can be solved because the physical boundary conditions are real, the census is exhaustive, and the waiting times reflect biological coalescence.
- In **Regime B (Hominins)**, the data lacks the mathematical signal necessary to evaluate diversity-dependent regulation. Because standing species counts never approach an asymptotic threshold and waiting times reflect geological sampling rather than biological splitting, the likelihood function cannot differentiate between density-dependent throttling and density-independent random drift.
