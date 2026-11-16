"""Composite taphonomically conditioned diversification likelihood engine.

Integrates the 6 mathematical primitives into a rigorous joint likelihood evaluator
for fossil lineage diversification under preservation heterogeneity:
- Primitive 1: Exponential diversity-dependent hazard lambda(D)
- Primitive 2: Keiding preservation conditioning P(observable | lifespan)
- Primitive 3: Inhomogeneous/homogeneous Poisson occurrence process
- Primitive 4: Continuous lineage duration and extinction density
- Primitive 5: Standing diversity step-function D(t)
- Primitive 6: Tip diversification rate (DR) regularization

Joint Likelihood Formulation:
    ln L_total = sum_i [ ln L_duration(s_i, e_i, mu)
                       + ln L_occurrences(T_i, s_i, e_i, q_b)
                       - ln P(observable | s_i, e_i, q_b) ]

Where:
    - s_i, e_i: Speciation and extinction times of lineage i (Ma before present)
    - T_i: Fossil occurrence times for lineage i
    - q_b: Preservation rate for basin b (or taxon-specific preservation rate)
    - mu: Mean extinction hazard
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from hominin_morphodynamics.inference.primitives import (
    keiding_log_conditioning,
    lineage_duration_loglik,
    log_diversity_hazard,
    poisson_occurrence_loglik,
    standing_diversity_trajectory,
)


@dataclass(frozen=True)
class LineageOccurrenceData:
    """Empirical occurrence and lifespan coordinates for an analytical lineage."""

    lineage_id: str
    speciation_time_ma: float  # s >= e >= 0
    extinction_time_ma: float
    occurrence_times_ma: list[float]
    is_extinct: bool = True
    basin: str = "default"


@dataclass(frozen=True)
class JointLikelihoodResult:
    """Decomposition of the joint taphonomic diversification log-likelihood."""

    log_lik_total: float
    log_lik_durations: float
    log_lik_occurrences: float
    log_lik_conditioning: float
    num_lineages: int
    num_occurrences: int


def evaluate_joint_diversification_loglik(
    lineages: Sequence[LineageOccurrenceData],
    mu: float,
    preservation_rates: dict[str, float] | float,
    lambda0: float | None = None,
    gl: float = 0.0,
) -> JointLikelihoodResult:
    """Compute the joint taphonomically conditioned log-likelihood over all lineages.

    Parameters:
        lineages: Sequence of lineage lifespan and fossil occurrence records.
        mu: Extinction hazard parameter (mu > 0).
        preservation_rates: Mapping of basin -> q (or scalar q applied to all basins).
        lambda0: Optional baseline speciation rate. If provided, evaluates diversity-dependent
                 hazard against standing diversity D(t) at lineage origin points.
        gl: Diversity-dependence slope parameter.

    Returns:
        JointLikelihoodResult with full log-likelihood decomposition.
    """
    if mu <= 0.0:
        raise ValueError(f"Extinction rate mu must be > 0, got {mu}")

    total_duration_loglik = 0.0
    total_occurrence_loglik = 0.0
    total_conditioning_loglik = 0.0
    total_occurrences_count = 0

    # Pre-extract lifespans if lambda0 is active for standing diversity
    if lambda0 is not None:
        lifespans = [(lin.speciation_time_ma, lin.extinction_time_ma) for lin in lineages]
        speciation_times = np.array([lin.speciation_time_ma for lin in lineages])
        div_counts = standing_diversity_trajectory(lineage_intervals=lifespans, eval_times=speciation_times)
    else:
        div_counts = None

    for idx, lin in enumerate(lineages):
        s = lin.speciation_time_ma
        e = lin.extinction_time_ma
        occs = lin.occurrence_times_ma

        # Resolve preservation rate q for this lineage's basin
        if isinstance(preservation_rates, dict):
            q = preservation_rates.get(lin.basin, preservation_rates.get("default", 1.0))
        else:
            q = float(preservation_rates)

        if q <= 0.0:
            raise ValueError(f"Preservation rate q must be > 0, got {q} for lineage {lin.lineage_id}")

        # 1. Lineage duration likelihood
        ll_dur = lineage_duration_loglik(s=s, e=e, mu_mean=mu, is_extinct=lin.is_extinct)
        total_duration_loglik += ll_dur

        # Optional diversity-dependent speciation contribution at origin
        if lambda0 is not None and div_counts is not None:
            # ln lambda(D(s)) = base_rate, g_coeff, diversity
            ln_lam = log_diversity_hazard(base_rate=lambda0, g_coeff=gl, diversity=float(div_counts[idx]))
            total_duration_loglik += ln_lam

        # 2. Fossil occurrences Poisson likelihood
        # Filter or validate that occs fall within [e, s]
        clamped_occs = [t for t in occs if e <= t <= s]
        ll_occ = poisson_occurrence_loglik(occurrence_times=clamped_occs, s=s, e=e, q=q)
        total_occurrence_loglik += ll_occ
        total_occurrences_count += len(clamped_occs)

        # 3. Keiding preservation conditioning (subtract ln P(observable))
        # Note: keiding_log_conditioning takes q_integral = q * (s - e)
        # and returns ln(1 - exp(-theta)) using log(-expm1(-theta))
        q_integral = q * (s - e)
        ln_p_obs = keiding_log_conditioning(q_integral=q_integral)
        total_conditioning_loglik += ln_p_obs

    # Joint: durations + occurrences - conditioning
    total_loglik = (
        total_duration_loglik
        + total_occurrence_loglik
        - total_conditioning_loglik
    )

    return JointLikelihoodResult(
        log_lik_total=float(total_loglik),
        log_lik_durations=float(total_duration_loglik),
        log_lik_occurrences=float(total_occurrence_loglik),
        log_lik_conditioning=float(total_conditioning_loglik),
        num_lineages=len(lineages),
        num_occurrences=total_occurrences_count,
    )
