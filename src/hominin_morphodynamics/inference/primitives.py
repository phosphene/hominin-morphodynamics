"""Mathematical primitives for macroevolutionary birth-death and preservation.

Pure functional implementations of canonical diversification and observation equations.
Decomposed from first principles:
- Kendall (1948): Continuous-time Markov birth-death process
- Keiding (1975): Survival conditioning for observable lineages
- Foote (1997): Continuous preservation and sampling probabilities
- Silvestro et al. (2014, 2019): Diversity-dependent hazard functions
- Jetz et al. (2012): Tip diversification rate (DR) metric

All primitives are numerically stable, operating in log-space where appropriate,
using expm1/log1p to prevent catastrophic floating-point cancellation.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def log_diversity_hazard(
    base_rate: float,
    g_coeff: float,
    diversity: float,
    clamp_bound: float = 50.0,
) -> float:
    """Primitive 1: Numerically stable log-hazard under exponential diversity-dependence.

    Formula:
        lambda(D) = lambda_0 * exp(G_l * D)
        ln lambda(D) = ln(lambda_0) + G_l * D

    Invariants:
        1. base_rate must be strictly positive.
        2. diversity must be non-negative.
        3. Returns finite log-hazard clamped within [-clamp_bound, +clamp_bound]
           to prevent IEEE 754 overflow/underflow.
    """
    if base_rate <= 0.0:
        raise ValueError(f"base_rate must be > 0.0, got {base_rate}")
    if diversity < 0.0:
        raise ValueError(f"diversity must be >= 0.0, got {diversity}")

    exponent = g_coeff * diversity
    clamped_exponent = max(-clamp_bound, min(clamp_bound, exponent))
    return math.log(base_rate) + clamped_exponent


def diversity_dependent_hazard(
    base_rate: float,
    g_coeff: float,
    diversity: float,
    clamp_bound: float = 50.0,
) -> float:
    """Primitive 1b: Natural-scale hazard rate lambda(D) = lambda_0 * exp(G_l * D)."""
    return math.exp(log_diversity_hazard(base_rate, g_coeff, diversity, clamp_bound))


def keiding_sampling_probability(
    q_integral: float,
) -> float:
    """Primitive 2: Keiding (1975) preservation conditioning probability.

    Calculates P(K >= 1 | theta) = 1 - exp(-theta), where theta = int_e^s q(t) dt.

    Uses -expm1(-theta) to avoid catastrophic cancellation when theta << 1.

    Invariants:
        1. Returns 0.0 when q_integral <= 0.0.
        2. Strictly bounded in [0.0, 1.0].
        3. Monotonically increasing with q_integral.
    """
    if q_integral <= 0.0:
        return 0.0
    return float(-np.expm1(-q_integral))


def keiding_log_conditioning(
    q_integral: float,
) -> float:
    """Primitive 2b: Log of Keiding conditioning probability ln(1 - exp(-theta)).

    Uses log(-expm1(-theta)) to eliminate cancellation artifacts.
    Returns -inf when q_integral <= 0.0.
    """
    if q_integral <= 0.0:
        return -math.inf
    p = -np.expm1(-q_integral)
    if p <= 0.0:
        return -math.inf
    return float(math.log(p))


def poisson_occurrence_loglik(
    occurrence_times: Sequence[float],
    s: float,
    e: float,
    q: float,
) -> float:
    """Primitive 3: Inhomogeneous/homogeneous Poisson occurrence log-likelihood.

    Given fossil occurrence dates t_1, ..., t_k within active lifespan [e, s]
    (with s >= e >= 0 in Ma before present):
        ln L = sum_{j=1}^k ln q - q * (s - e)

    Invariants:
        1. All occurrence times must fall within [e, s].
        2. q must be strictly positive.
        3. When k == 0, returns -q * (s - e).
    """
    if s < e:
        raise ValueError(f"Speciation time s ({s}) must be >= extinction time e ({e})")
    if q <= 0.0:
        raise ValueError(f"Preservation rate q must be > 0.0, got {q}")

    duration = s - e
    expected_fossils = q * duration

    k = len(occurrence_times)
    if k == 0:
        return -expected_fossils

    for t in occurrence_times:
        if not (e <= t <= s):
            raise ValueError(f"Occurrence time {t} outside lineage lifespan [{e}, {s}]")

    return k * math.log(q) - expected_fossils


def lineage_duration_loglik(
    s: float,
    e: float,
    mu_mean: float,
    is_extinct: bool = True,
) -> float:
    """Primitive 4: Continuous lineage duration and extinction event log-likelihood.

    Under constant or mean extinction hazard mu:
        - If extinct (e > 0 or is_extinct): ln L = ln(mu) - mu * (s - e)
        - If extant (e == 0 and not is_extinct): ln L = -mu * (s - e)

    Invariants:
        1. s >= e >= 0.
        2. mu_mean > 0.
    """
    if s < e:
        raise ValueError(f"Speciation time s ({s}) must be >= extinction time e ({e})")
    if mu_mean <= 0.0:
        raise ValueError(f"Extinction rate mu_mean must be > 0.0, got {mu_mean}")

    duration = s - e
    survival_term = -mu_mean * duration

    if not is_extinct or e == 0.0:
        return float(survival_term)

    return float(math.log(mu_mean) + survival_term)


def standing_diversity_trajectory(
    lineage_intervals: Sequence[tuple[float, float]],
    eval_times: Sequence[float] | np.ndarray,
) -> np.ndarray:
    """Primitive 5: Standing diversity step-function D(t).

    Calculates exact active lineage count at each time point in eval_times.
    Lineage i is active at t if s_i >= t >= e_i.

    Invariants:
        1. Non-negative integer values.
        2. Exact step function matching closed intervals [e, s].
    """
    times = np.asarray(eval_times, dtype=np.float64)
    counts = np.zeros(len(times), dtype=np.int64)

    for s, e in lineage_intervals:
        if s < e:
            continue
        mask = (times <= s) & (times >= e)
        counts[mask] += 1

    return counts


def tip_diversification_rate(
    branch_lengths: Sequence[float],
    min_branch_length: float = 1e-6,
) -> float:
    """Primitive 6: Jetz et al. (2012) tip Diversification Rate (DR) metric.

    Formula:
        DR_i = sum_{j=1}^N (1/2)^{j-1} * (1 / l_j)
    where l_1 is terminal branch length, l_2 is parent branch, etc.

    Numerical defense:
        Regularizes branch lengths below min_branch_length to prevent
        infinite division singularities on near-zero internal branches (polytomies).

    Invariants:
        1. Empty sequence returns 0.0.
        2. All branch lengths regularized to at least min_branch_length > 0.
        3. Monotonically decreases as branch lengths increase (longer branches = slower diversification).
    """
    if not branch_lengths:
        return 0.0
    if min_branch_length <= 0.0:
        raise ValueError(f"min_branch_length must be > 0.0, got {min_branch_length}")

    dr = 0.0
    for j, l in enumerate(branch_lengths):
        reg_l = max(min_branch_length, float(l))
        weight = 0.5 ** j
        dr += weight / reg_l

    return float(dr)
