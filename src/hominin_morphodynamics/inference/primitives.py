"""Mathematical primitives for macroevolutionary birth-death and preservation.

Re-exports and wraps phosphene.holonomy.macroevo.primitives for hominin-morphodynamics.
"""

from __future__ import annotations

import math
from typing import Sequence
import numpy as np

import phosphene.holonomy.macroevo.primitives as _prims
from phosphene.holonomy.macroevo.primitives import (
    log_diversity_hazard,
    log_keiding_conditioning,
    log_poisson_occurrences,
    log_extinction_density,
    regularized_inverse_branch_length,
)


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
    """
    if q_integral <= 0.0:
        return 0.0
    return float(-np.expm1(-q_integral))


def keiding_log_conditioning(
    q_integral: float,
) -> float:
    """Primitive 2b: Log of Keiding conditioning probability ln(1 - exp(-theta))."""
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
    """Primitive 3: Inhomogeneous/homogeneous Poisson occurrence log-likelihood."""
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
    """Primitive 4: Continuous lineage duration and extinction event log-likelihood."""
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
    """Primitive 5: Standing diversity step-function D(t)."""
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


__all__ = [
    "log_diversity_hazard",
    "diversity_dependent_hazard",
    "keiding_sampling_probability",
    "keiding_log_conditioning",
    "poisson_occurrence_loglik",
    "lineage_duration_loglik",
    "standing_diversity_trajectory",
    "tip_diversification_rate",
    "log_keiding_conditioning",
    "log_poisson_occurrences",
    "log_extinction_density",
    "regularized_inverse_branch_length",
]
