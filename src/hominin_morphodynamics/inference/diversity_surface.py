"""Evaluation of diversity-dependent speciation and extinction likelihood surfaces.

Replicates and extends the continuous diversity-dependent birth-death models of
Silvestro et al. (2014, 2019) and Van Holstein & Foley (2024).

Implements:
1. Exact profile likelihood estimation for baseline speciation (lambda0)
   and diversity-dependence slope (Gl) under lambda(D) = lambda0 * exp(Gl * D).
2. Numerical quadrature of cumulative speciation hazard over LTT diversity trajectories.
3. Likelihood-Ratio Tests (LRT) and chi-square significance testing against
   the null model of density-independent diversification (Gl = 0).
4. Stratified evaluation comparing whole-clade, non-Homo, and Homo subsets
   across all 5 empirical time datasets (Fine TPP, Fine NHPP, Broad TPP,
   Broad NHPP, and Wood-Boyle).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy import optimize, stats

from hominin_morphodynamics.inference.primitives import log_diversity_hazard


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
    delta_aic: float  # aic_null - aic_full (positive favors full model)


def fit_diversity_dependence(
    speciation_times_ma: Sequence[float],
    ltt_time_grid_ma: np.ndarray,
    ltt_diversity_grid: np.ndarray,
    t_max_eval_ma: float = 3.0,
    config_name: str = "custom",
    clade_group: str = "all",
) -> DiversityModelResult:
    """Fit exponential diversity-dependence model and run Likelihood-Ratio Test against null (Gl=0).

    Model:
        lambda(D(t)) = lambda0 * exp(Gl * D(t))

    Log-Likelihood:
        ln L = sum_{i=1}^N ln lambda(D(ts_i)) - integral_0^T lambda(D(t)) dt

    Invariants:
        1. lambda0 > 0.
        2. Gl is unconstrained in [-10, 10].
        3. Under null model (Gl = 0), lambda0_mle = N / T_eval.
    """
    ts_arr = np.array(speciation_times_ma)
    n_sp = len(ts_arr)
    if n_sp == 0:
        raise ValueError("Cannot fit diversity dependence on empty speciation times sequence.")

    # Sort LTT ascending in time
    order = np.argsort(ltt_time_grid_ma)
    t_grid = ltt_time_grid_ma[order]
    d_grid = ltt_diversity_grid[order]

    # Evaluate standing diversity D(ts) at each speciation event
    def div_at_t(t: float) -> float:
        idx = np.searchsorted(t_grid, t)
        if idx >= len(d_grid):
            idx = len(d_grid) - 1
        return float(d_grid[idx])

    d_at_events = np.array([div_at_t(float(t)) for t in ts_arr])

    # Discretize integration interval [0, t_max_eval_ma]
    mask = t_grid[:-1] <= t_max_eval_ma
    dt = np.diff(t_grid)[mask]
    d_eval = d_grid[:-1][mask]

    def profile_gl(gl: float) -> tuple[float, float]:
        """Profile likelihood over Gl by solving lambda0 analytically."""
        g_d_events = np.clip(gl * d_at_events, -50.0, 50.0)
        g_d_grid = np.clip(gl * d_eval, -50.0, 50.0)
        integral_factor = float(np.sum(np.exp(g_d_grid) * dt))
        if integral_factor <= 0.0 or not np.isfinite(integral_factor):
            return -1e12, 1e-5
        l0 = max(1e-6, n_sp / integral_factor)
        ll = float(np.sum(np.log(l0) + g_d_events) - l0 * integral_factor)
        return ll, l0

    # 1. Null Model (Gl = 0.0)
    ll_null, l0_null = profile_gl(0.0)

    # 2. Full Model (Profile optimization over Gl)
    opt_res = optimize.minimize_scalar(
        lambda gl: -profile_gl(float(gl))[0],
        bounds=(-10.0, 10.0),
        method="bounded",
    )
    mle_gl = float(opt_res.x)
    ll_full, l0_full = profile_gl(mle_gl)

    # If full likelihood is numerically worse than null due to boundary effects, clamp to null
    if ll_full < ll_null:
        ll_full = ll_null
        l0_full = l0_null
        mle_gl = 0.0

    # LRT Statistic: 2 * (ln L_full - ln L_null)
    lrt_stat = max(0.0, 2.0 * (ll_full - ll_null))
    p_val = float(1.0 - stats.chi2.cdf(lrt_stat, df=1))

    # Information criteria: 1 parameter for null, 2 for full
    aic_null = 2 * 1 - 2 * ll_null
    aic_full = 2 * 2 - 2 * ll_full
    delta_aic = aic_null - aic_full

    return DiversityModelResult(
        config_name=config_name,
        clade_group=clade_group,
        num_species=n_sp,
        null_loglik=round(ll_null, 4),
        null_lambda0=round(l0_null, 4),
        full_loglik=round(ll_full, 4),
        full_lambda0=round(l0_full, 4),
        mle_gl=round(mle_gl, 4),
        lrt_stat=round(lrt_stat, 4),
        p_value=round(p_val, 4),
        is_significant_at_05=(p_val < 0.05),
        aic_null=round(aic_null, 4),
        aic_full=round(aic_full, 4),
        delta_aic=round(delta_aic, 4),
    )


def audit_van_holstein_empirical_grid(
    outputs_dir: Path,
) -> list[DiversityModelResult]:
    """Run full empirical replication across all 5 datasets in PyRate/Outputs.

    Evaluates:
    - Homo subset (N=7 taxa)
    - Non-Homo subset (N=10 taxa)
    - Whole Clade (N=17 taxa)
    """
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

        # 1. Homo
        res_homo = fit_diversity_dependence(
            speciation_times_ma=homo_ts,
            ltt_time_grid_ma=t_grid,
            ltt_diversity_grid=d_grid,
            t_max_eval_ma=t_homo,
            config_name=display_name,
            clade_group="Homo",
        )
        results.append(res_homo)

        # 2. Non-Homo
        res_nonhomo = fit_diversity_dependence(
            speciation_times_ma=nonhomo_ts,
            ltt_time_grid_ma=t_grid,
            ltt_diversity_grid=d_grid,
            t_max_eval_ma=t_clade,
            config_name=display_name,
            clade_group="Non-Homo",
        )
        results.append(res_nonhomo)

        # 3. Whole Clade
        res_clade = fit_diversity_dependence(
            speciation_times_ma=all_ts,
            ltt_time_grid_ma=t_grid,
            ltt_diversity_grid=d_grid,
            t_max_eval_ma=t_clade,
            config_name=display_name,
            clade_group="Whole-Clade",
        )
        results.append(res_clade)

    return results
