"""Hominin basin-resolved taphonomic diversification likelihood orchestrator.

Resolves depositional basin preservation rates (Pull/Domain layer) and delegates
all mathematical likelihood evaluation to ``phosphene.holonomy.macroevo.joint_taphonomic_loglik``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from phosphene.holonomy.macroevo import (
    LineageObservation,
    joint_taphonomic_loglik,
)


@dataclass(frozen=True)
class LineageOccurrenceData:
    """Empirical occurrence and lifespan coordinates for an analytical hominin lineage."""

    lineage_id: str
    speciation_time_ma: float
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
    """Resolve basin preservation rates and evaluate joint likelihood via ``holonomy.macroevo``."""
    if mu <= 0.0:
        raise ValueError(f"Extinction rate mu must be > 0, got {mu}")

    observations: list[LineageObservation] = []
    for lin in lineages:
        if isinstance(preservation_rates, dict):
            q = preservation_rates.get(lin.basin, preservation_rates.get("default", 1.0))
        else:
            q = float(preservation_rates)
        if q <= 0.0:
            raise ValueError(f"Preservation rate q must be > 0, got {q} for lineage {lin.lineage_id}")

        clamped_occs = tuple(
            t for t in lin.occurrence_times_ma if lin.extinction_time_ma <= t <= lin.speciation_time_ma
        )
        observations.append(
            LineageObservation(
                lineage_id=lin.lineage_id,
                origin_age=lin.speciation_time_ma,
                extinction_age=lin.extinction_time_ma,
                occurrence_times=clamped_occs,
                preservation_rate=q,
                is_extant=(not lin.is_extinct or lin.extinction_time_ma == 0.0),
            )
        )

    breakdown = joint_taphonomic_loglik(
        observations=observations,
        extinction_rate=mu,
        lambda0=lambda0,
        g_l=gl,
    )
    return JointLikelihoodResult(
        log_lik_total=breakdown.total,
        log_lik_durations=breakdown.durations + breakdown.speciation,
        log_lik_occurrences=breakdown.occurrences,
        log_lik_conditioning=breakdown.conditioning,
        num_lineages=breakdown.num_lineages,
        num_occurrences=breakdown.num_occurrences,
    )
