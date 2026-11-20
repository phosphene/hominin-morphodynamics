"""Macroevolutionary birth-death and preservation primitives.

Delegates strictly to canonical ``phosphene.holonomy.macroevo.primitives`` with zero
duplicated mathematical logic.
"""

from __future__ import annotations

from typing import Sequence

from phosphene.holonomy.macroevo.primitives import (
    TipBranchPath,
    TipDRDiagnostic,
    diversity_hazard,
    equal_splits,
    keiding_observability_prob,
    log_diversity_hazard,
    log_keiding_conditioning,
    log_lineage_duration_density,
    log_poisson_count_pmf,
    log_poisson_process_density,
    log_turnover_survival,
    preservation_effort,
    regularized_inverse_branch_length,
    standing_diversity_trajectory,
    tip_dr,
    tip_dr_diagnostic,
)

# Thin backward-compatibility aliases delegating directly to holonomy
diversity_dependent_hazard = diversity_hazard
keiding_sampling_probability = keiding_observability_prob
keiding_log_conditioning = log_keiding_conditioning
tip_diversification_rate = tip_dr


def poisson_occurrence_loglik(
    occurrence_times: Sequence[float],
    s: float,
    e: float,
    q: float,
) -> float:
    """Delegate directly to ``holonomy.macroevo.primitives.log_poisson_process_density``."""
    return log_poisson_process_density(
        occurrence_times=occurrence_times,
        origin_age=s,
        extinction_age=e,
        preservation_rate=q,
    )


def lineage_duration_loglik(
    s: float,
    e: float,
    mu_mean: float,
    is_extinct: bool = True,
) -> float:
    """Delegate directly to ``holonomy.macroevo.primitives.log_lineage_duration_density``."""
    if s < e:
        raise ValueError(f"Speciation time s ({s}) must be >= extinction time e ({e})")
    if mu_mean <= 0.0:
        raise ValueError(f"Extinction rate mu_mean must be > 0.0, got {mu_mean}")
    return log_lineage_duration_density(
        duration=s - e,
        extinction_rate=mu_mean,
        is_extant=(not is_extinct or e == 0.0),
    )


__all__ = [
    "TipBranchPath",
    "TipDRDiagnostic",
    "equal_splits",
    "tip_dr",
    "tip_dr_diagnostic",
    "tip_diversification_rate",
    "regularized_inverse_branch_length",
    "log_diversity_hazard",
    "diversity_hazard",
    "diversity_dependent_hazard",
    "preservation_effort",
    "keiding_observability_prob",
    "keiding_sampling_probability",
    "log_keiding_conditioning",
    "keiding_log_conditioning",
    "log_poisson_count_pmf",
    "log_poisson_process_density",
    "poisson_occurrence_loglik",
    "log_lineage_duration_density",
    "log_turnover_survival",
    "lineage_duration_loglik",
    "standing_diversity_trajectory",
]
