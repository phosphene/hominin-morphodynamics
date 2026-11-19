# Hypothesis Testing Patterns, Calibration Standards, and Seam Formalization

## Executive Mandate

This document articulates the numerical and property testing standards adopted across `hominin-morphodynamics`, codifying the transition from loose black-box sanity assertions to rigorous, mathematically bounded property calibration.

In paleobiology and paleoanthropology, analytical pipelines regularly process sparse empirical records ($N=8$ to $N=29$ specimens or splits). Under small sample sizes, uncalibrated floating-point arithmetic, hidden state mutations, and unconstrained generator distributions do not fail noisily; they introduce subtle numerical biases, mask floating-point cancellation, or trigger shrinker failures that masquerade as biological phenomena.

To guarantee that the computational layer never introduces artificial structure, all property and invariant testing adheres strictly to the patterns codified below.

---

## 1. Input Geometry and Generator Hygiene

### 1.1 Strict IEEE-754 Finite-Domain Hygiene (Anti-Pattern: Unguarded Extended-Real Floats)
* **The Failure Mode:** Using default `st.floats()` or bounded ranges without explicitly specifying `allow_nan=False, allow_infinity=False, allow_subnormal=False`.
* **The Consequence:** Default floats include `NaN`, $\pm\infty$, and IEEE-754 subnormal numbers ($< 2.22 \times 10^{-308}$). When an invariant fails, Hypothesis's test-case shrinker attempts bitwise boundary simplifications. If subnormals or infinities are permitted, genuine floating-point cancellation or catastrophic loss of precision collapses into trivial `NaN` absorption or division-by-subnormal overflow.
* **Our Standard:** All float generators are strictly finite and normalized:
  ```python
  st.floats(
      min_value=min_val,
      max_value=max_val,
      allow_nan=False,
      allow_infinity=False,
      allow_subnormal=False,
  )
  ```

### 1.2 Constructive Simplex and Manifold Generation (Anti-Pattern: Rejection Filtering with `assume()`)
* **The Failure Mode:** Drawing independent random numbers and attempting to constrain them via `assume(sum(p) == 1.0)` or `assume(t1 > t2 > t3)`.
* **The Consequence:** Valid algebraic manifolds (such as descending branching times or probability simplexes) occupy a subset of measure zero in Euclidean space. Gating via `assume()` causes $>99\%$ of generated inputs to be rejected, triggering `HealthCheck.filter_too_much` and biasing surviving inputs toward trivial zero vectors.
* **Our Standard:** Parameterize manifolds constructively. For example, descending temporal event schedules are constructed via reverse cumulative sums of strictly positive waiting times:
  $$\Delta t_i > 0 \implies t_j = \sum_{i=j}^n \Delta t_i \quad \text{guarantees} \quad t_1 > t_2 > \dots > t_n > 0$$

### 1.3 Boundary-Relative Parameterization for Shrinker Continuity
* **The Failure Mode:** Testing threshold transitions (e.g., carrying capacity $K$ versus standing lineage richness $k$) by drawing $K$ and $k$ independently.
* **The Consequence:** When Hypothesis shrinks a failing input, it walks choices toward zero. Independent parameter draws cause chaotic jumps across phase boundaries rather than smoothly isolating the critical phase transition.
* **Our Standard:** Parameterize directly relative to the active algebraic or biological boundary:
  $$\text{headroom} = K - k \implies K = k + \text{headroom}$$
  Hypothesis shrinks `headroom` smoothly toward `0.0`, isolating the exact threshold where behavior switches.

---

## 2. Invariant and Oracle Calibration

### 2.1 Closed-Form and Asymptotic Oracle Sandwiches
Every complex numerical algorithm or iterative solver must be bounded by simpler, exact references:
1. **Scalar Limits:** When coupling parameters vanish (e.g., speciation rate $\lambda_0 = 0$), matrix or stochastic equations must collapse to scalar closed forms ($e^{-k \mu_0 \Delta t}$) to machine precision ($\le 10^{-13}$).
2. **Asymptotic Limits:** As capacity $K \to \infty$, density-dependent models must converge onto unconstrained constant-rate birth-death solutions within provable tolerances.

### 2.2 Variational Defect Hunting via `hypothesis.target()`
* **The Failure Mode:** Evaluating numerical invariants with binary assertions alone (`assert abs(x - y) < tol`).
* **The Consequence:** Binary assertions treat all passing inputs identically. Hypothesis wanders randomly through the benign interior of the parameter space rather than exploring stressed regimes.
* **Our Standard:** Formulate discrepancies, cancellations, and near-zero residuals as continuous non-negative functionals:
  ```python
  defect = abs(analytical_val - numerical_val)
  target(defect, label="primitive_cancellation_defect")
  assert defect <= tol
  ```
  This transforms Hypothesis's search engine into an active optimizer hunting for worst-case floating-point distortion.

### 2.3 Buffer Immutability and Stateful Stability
All intermediate state vectors and transition matrices must enforce buffer read-only protections (`arr.flags.writeable = False`). This ensures that iterative steppers, Markov transitions, and property test replays never mutate internal state in place, preventing order-dependent bugs across Hypothesis shrink passes.
