"""Hominin diversity-dependent speciation likelihood surface evaluation.

Delegates all numerical profile-likelihood math to
``phosphene.holonomy.macroevo.continuous_profile_likelihood_surface``, keeping
hominin-specific dataset orchestration (Pull) cleanly separated.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from phosphene.holonomy.macroevo import continuous_profile_likelihood_surface


@dataclass(frozen=True)
class DiversityModelResult:
    """Statistical summary of a continuous diversity-dependent model evaluation."""

    config_name: str
    clade_group: str
    num_species: int
    null_loglik: float
    null_lambda0: float
    full_loglik: float
    full_lambda0: float
    mle_gl: float
    lrt_stat: float
    p_value: float
    is_significant_at_05: bool
    aic_null: float
    aic_full: float
    delta_aic: float


def fit_diversity_dependence(
    speciation_times_ma: Sequence[float],
    ltt_time_grid_ma: np.ndarray,
    ltt_diversity_grid: np.ndarray,
    t_max_eval_ma: float = 3.0,
    config_name: str = "custom",
    clade_group: str = "all",
    is_per_lineage_process: bool = True,
) -> DiversityModelResult:
    """Fit exponential diversity-dependence model via ``holonomy.macroevo``."""
    surf = continuous_profile_likelihood_surface(
        speciation_times=speciation_times_ma,
        ltt_time_grid=ltt_time_grid_ma,
        ltt_diversity_grid=ltt_diversity_grid,
        t_max_eval=t_max_eval_ma,
        is_per_lineage_process=is_per_lineage_process,
    )
    return DiversityModelResult(
        config_name=config_name,
        clade_group=clade_group,
        num_species=len(speciation_times_ma),
        null_loglik=round(surf.null_log_lik, 4),
        null_lambda0=round(surf.null_lambda0, 4),
        full_loglik=round(surf.max_log_lik, 4),
        full_lambda0=round(surf.best_lambda0, 4),
        mle_gl=round(surf.best_g_l, 4),
        lrt_stat=round(surf.likelihood_ratio, 4),
        p_value=round(surf.p_value, 4),
        is_significant_at_05=surf.excludes_zero(alpha=0.05),
        aic_null=round(surf.aic_null, 4),
        aic_full=round(surf.aic_full, 4),
        delta_aic=round(surf.delta_aic, 4),
    )


def audit_van_holstein_empirical_grid(
    outputs_dir: Path,
) -> list[DiversityModelResult]:
    """Run empirical replication across all 5 Van Holstein & Foley (2024) PyRate datasets."""
    configs = [
        ("Fine_occurrence_level/TPP", "Fine TPP", 3.0, 5.0),
        ("Fine_occurrence_level/NHPP", "Fine NHPP", 3.0, 5.0),
        ("Broad_occurrence_level/TPP", "Broad TPP", 3.0, 5.0),
        ("Broad_occurrence_level/NHPP", "Broad NHPP", 3.0, 5.0),
        ("Wood-Boyle", "Wood-Boyle", 3.0, 5.0),
    ]

    homo_ids = {10, 11, 12, 13, 16, 17, 18}
    results: list[DiversityModelResult] = []

    for rel_path, display_name, t_homo, t_clade in configs:
        times_file = outputs_dir / rel_path / "wholeclade.txt"
        ltt_file = outputs_dir / rel_path / "wholeclade_ltt.txt"

        if not (times_file.exists() and ltt_file.exists()):
            continue

        ltt_data = np.loadtxt(ltt_file, skiprows=1)
        t_grid = ltt_data[:, 0]
        d_grid = ltt_data[:, 1]
        species_data = np.loadtxt(times_file, skiprows=1)

        homo_ts = [row[2] for row in species_data if int(row[1]) in homo_ids]
        nonhomo_ts = [row[2] for row in species_data if int(row[1]) not in homo_ids]
        all_ts = [row[2] for row in species_data]

        for group, ts, t_eval in (
            ("Homo", homo_ts, t_homo),
            ("Non-Homo", nonhomo_ts, t_clade),
            ("Whole-Clade", all_ts, t_clade),
        ):
            results.append(
                fit_diversity_dependence(
                    speciation_times_ma=ts,
                    ltt_time_grid_ma=t_grid,
                    ltt_diversity_grid=d_grid,
                    t_max_eval_ma=t_eval,
                    config_name=display_name,
                    clade_group=group,
                )
            )

    return results
