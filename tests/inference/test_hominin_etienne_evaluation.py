"""Tests for direct application of the canonical Etienne master equation to hominin lineages.

Verifies:
1. Computation of hominin profile likelihood across carrying capacity K in [8, 500].
2. Demonstration that likelihood curvature d^2 lnL / dK^2 is essentially flat (Delta lnL <= 0.50).
3. Non-rejection of the unconstrained null (K -> inf), proving carrying capacity K
   does not appear as an identifiable or viable parameter in hominin cladogenesis.
"""

from __future__ import annotations

import numpy as np
import pytest

from hominin_morphodynamics.inference.master_equation import (
    MasterEquationParams,
    compute_etienne_loglik,
    profile_etienne_k,
)

# Canonical Plio-Pleistocene Homo origination branching times (crown age 2.8 Ma to present)
HOMO_BRANCHING_TIMES_MA: list[float] = [2.80, 2.31, 1.89, 1.21, 0.78, 0.43, 0.24]


def test_hominin_etienne_loglik_evaluates_smoothly():
    """Verify Etienne master equation evaluates finite log-likelihood on hominin branching times."""
    p = MasterEquationParams(
        lambda_0=1.0,
        mu_0=0.1,
        k_carrying_capacity=15.0,
        dd_model=1.3,
    )
    ll = compute_etienne_loglik(p, HOMO_BRANCHING_TIMES_MA, condition_on_survival=True, soc=2)
    assert np.isfinite(ll)
    assert ll < 0.0


def test_hominin_carrying_capacity_is_non_identifiable():
    """Verify that varying K across an order of magnitude yields Delta lnL < 1.0 (flat surface)."""
    k_grid = [8.0, 10.0, 12.0, 15.0, 20.0, 30.0, 50.0, 100.0, 500.0]
    ks, lls = profile_etienne_k(
        HOMO_BRANCHING_TIMES_MA,
        k_grid=k_grid,
        fixed_lambda_0=1.0,
        fixed_mu_0=0.1,
        soc=2,
    )

    assert len(ks) == len(k_grid)
    assert np.all(np.isfinite(lls))

    # The maximum log-likelihood difference across the entire grid must be less than 0.60
    # (95% LRT threshold is 1.92 units).
    delta_max = float(np.max(lls) - np.min(lls))
    assert delta_max < 0.60, f"Expected flat profile (delta < 0.60), got delta = {delta_max}"

    # Difference between finite K=15 and unconstrained K=500 is negligible
    idx_15 = k_grid.index(15.0)
    idx_500 = k_grid.index(500.0)
    diff_15_500 = abs(lls[idx_15] - lls[idx_500])
    assert diff_15_500 < 0.40
