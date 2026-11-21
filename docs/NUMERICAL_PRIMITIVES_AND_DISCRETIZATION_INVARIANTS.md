# Numerical Primitives & Discretization Invariants for Continuous-Time Stochastic Operators

**Coordinate:** `docs/NUMERICAL_PRIMITIVES_AND_DISCRETIZATION_INVARIANTS.md`  
**Namespace:** `morphodynamics.numerics`  
**Authors:** Ed Phil (@edphos), Jan (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Living Methodological Standard & Computational Invariant Specification  
**Date:** 2026-11-21  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. Scope & Objective

Analytical Kolmogorov forward and backward systems are formulated as continuous operators on state and temporal continua:

$$\frac{\partial p}{\partial t} = \mathcal{A}^* p$$

Silicon implementation requires three distinct discretizations:
1. **State-Space Truncation Boundary ($N_{\max} = K$):** Projecting countably infinite lineage states $\{0, 1, \dots, \infty\}$ onto a finite dimension $(K+1)$.
2. **Temporal Matrix Exponential Operator ($\Delta \tau$):** Integrating $\exp(\mathbf{Q}\Delta\tau)$ across continuous waiting times via Padé or uniformization series.
3. **Richardson Discretization Audit ($h \to 0$):** Verifying whether the inferred likelihood surface reflects underlying biological dynamics or numerical mesh placement.

This specification documents the six self-sufficient units of numerical reason that isolate these constraints into deterministic Python primitives.

---

## 2. The Computational Architecture

```
       ┌─────────────────────────────────────────────────────────────────────────┐
       │             CONTINUOUS-TIME STOCHASTIC OPERATOR: dP/dt = Q P            │
       └───────────────────────────────────┬─────────────────────────────────────┘
                                           │
          ┌────────────────────────────────┴────────────────────────────────┐
          ▼                                                                 ▼
┌───────────────────────────┐                                 ┌───────────────────────────┐
│     STATE-SPACE AXIS      │                                 │       TEMPORAL AXIS       │
├───────────────────────────┤                                 ├───────────────────────────┤
│ [1] Truncation Closure    │                                 │ [4] Scaling & Squaring    │
│     (Zero-Flux Metzler Q) │                                 │     (Padé Approximant)    │
│ [2] Dynamic Tail Bound    │                                 │ [5] Jensen Uniformization │
│     (Stiffness Audit)     │                                 │     (Poisson Expansion)   │
│ [3] Simplex Projection    │                                 │ [6] Mesh-Invariance Grid  │
│     (Non-Negative Flux)   │                                 │     (Richardson Step-Down)│
└───────────────────────────┘                                 └───────────────────────────┘
```

---

## 3. The Six Numerical Primitives

### Unit 1: Truncation Closure (`ZeroFluxMetzler`)
- **Precursor:** van Kampen (1992) *Stochastic Processes in Physics and Chemistry*; Dayar & Stewart (2000).
- **Invariant:** The infinite tridiagonal birth-death generator $\mathbf{Q}_\infty$ is truncated at $N_{\max} = K$. To preserve total probability without artificial reflection or mass creation, the boundary rate satisfies $\lambda_K \equiv 0$, and row sums satisfy:
  $$\sum_{j=0}^K q_{ij} = 0 \quad \forall i \in \{0, \dots, K\}$$

### Unit 2: Dynamic Tail & Stiffness Bound (`SpectralStiffnessBound`)
- **Precursor:** Gear (1971) *Numerical Initial Value Problems in ODEs*; Higham (2008).
- **Invariant:** The spectral radius of dissipative modes $|\operatorname{Re}(\omega_{\max})| \approx O(K \cdot \mu_0)$ dictates explicit integration limits:
  $$\Delta t_{\text{critical}} \le \frac{2}{|\operatorname{Re}(\omega_{\max})|}$$
  Auditing stiffness prevents catastrophic divergence when transitioning between explicit steps and matrix exponentiation.

### Unit 3: Simplex Projection (`ProbabilitySimplexProject`)
- **Precursor:** Wang & Carreira-Perpiñán (2013) *ICML*; Duchi et al. (2008).
- **Invariant:** Roundoff truncation in rational Padé approximations can yield subnormal negative probabilities ($p_n \approx -10^{-16}$). Naive clipping ($\max(0, p)$) violates $\|p\|_1 = 1$. The state must be Euclidean-projected onto the probability simplex $\Delta^K = \{p \in \mathbb{R}^{K+1} \mid p \ge 0, \mathbf{1}^T p = 1\}$ before evaluating $\ln p_n$.

### Unit 4: Scaling & Squaring Padé Propagation (`PadeExponential`)
- **Precursor:** Al-Mohy & Higham (2009) *SIAM J. Matrix Anal. Appl.*
- **Invariant:** Direct interval flow $\exp(\mathbf{Q}\Delta\tau)$ evaluated via $[13/13]$ diagonal rational Padé approximants with optimal scaling power $s$:
  $$\exp(\mathbf{Q}\Delta\tau) \approx \left[ R_{13,13}\left(2^{-s} \mathbf{Q}\Delta\tau\right) \right]^{2^s}$$

### Unit 5: Jensen Uniformization Propagator (`UniformizationPropagator`)
- **Precursor:** Jensen (1953) *Skand. Aktuarietidskr.*; Grassmann (1977).
- **Invariant:** Converts the continuous-time generator into a discrete transition matrix $\mathbf{P} = \mathbf{I} + \frac{1}{\gamma} \mathbf{Q}$ where $\gamma = \max_n |q_{nn}|$. Expands interval flow into a Poisson-weighted sum:
  $$P(t + \Delta\tau) = \sum_{j=0}^M e^{-\gamma\Delta\tau} \frac{(\gamma\Delta\tau)^j}{j!} \left(\mathbf{P}^j P(t)\right)$$
  By construction, every term is non-negative, eliminating floating-point negativity artifacts without projection.

### Unit 6: Richardson Mesh-Invariance Audit (`MeshConvergenceAudit`)
- **Precursor:** Richardson (1911) *Philos. Trans. R. Soc. A*; Roache (1998).
- **Invariant:** Evaluates the log-likelihood surface under step halving ($h, h/2, h/4$). The observed order of convergence:
  $$p_{\text{obs}} = \frac{\ln\left(\frac{\ln L_{4h} - \ln L_{2h}}{\ln L_{2h} - \ln L_h}\right)}{\ln 2}$$
  verifies asymptotic stability. If $p_{\text{obs}}$ fails to converge or exhibits oscillatory divergence, the inferential result is an artifact of the discretization mesh.

---

## 4. Empirical Summary Matrix

| Primitive | Mathematical Target | Failure Mode Addressed | Preserved Numerical Invariant |
|---|---|---|---|
| **`ZeroFluxMetzler`** | Generator $\mathbf{Q} \in \mathbb{R}^{(K+1)\times(K+1)}$ | Artificial probability reflection or creation | Conservative row sums $\sum_j q_{ij} = 0$ |
| **`SpectralStiffnessBound`** | Generator Spectrum $\sigma(\mathbf{Q})$ | Explosive explicit solver instability | Step bound $\Delta t \le 2 / \|\operatorname{Re}(\omega_{\max})\|$ |
| **`ProbabilitySimplexProject`** | Distribution $P(t) \in \Delta^K$ | Subnormal negative values crashing $\ln p_n$ | Exact Euclidean projection to simplex $\Delta^K$ |
| **`PadeExponential`** | Interval flow $\exp(\mathbf{Q}\Delta\tau)$ | Accumulated low-order stepping drift | High-order norm accuracy via scaling & squaring |
| **`UniformizationPropagator`** | Poisson series $\sum w_j \mathbf{P}^j$ | Loss of positivity in stiff regimes | Inherent non-negativity across all steps |
| **`MeshConvergenceAudit`** | Grid step $h \to 0$ | Grid-boundary alignment artifacts | Invariance: $\lim_{h \to 0} \hat{\boldsymbol{\theta}}(h) = \boldsymbol{\theta}^*$ |
