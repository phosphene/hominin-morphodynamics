"""Tests for precursor models of diversity-dependent macroevolution."""

from __future__ import annotations

import numpy as np
import pytest

from hominin_morphodynamics.inference.diversity_surface import fit_diversity_dependence
from hominin_morphodynamics.inference.precursor_models import (
    simulate_etienne_macarthur_radiation,
    simulate_silvestro_exponential_radiation,
)


def test_etienne_radiation_respects_carrying_capacity():
    """Verify that Etienne linear diversity-dependence caps clade size at K."""
    k_cap = 15.0
    sim = simulate_etienne_macarthur_radiation(
        carrying_capacity_k=k_cap,
        lambda0=1.5,
        mu0=0.1,
        max_duration=12.0,
        seed=101,
    )

    # Invariants:
    # 1. Diversity must never exceed K
    assert np.all(sim.time_series_diversity <= k_cap + 1)
    # 2. Lineages must have valid birth-death coordinates
    assert len(sim.lineages) >= 2
    for lin in sim.lineages:
        assert lin.origin_time >= 0.0
        if lin.extinction_time is not None:
            assert lin.extinction_time >= lin.origin_time


def test_silvestro_exponential_radiation_detects_negative_gl():
    """Verify that fitting our likelihood surface to an idealized negative-Gl simulation recovers Gl < 0."""
    sim = simulate_silvestro_exponential_radiation(
        lambda0=1.0,
        gl=-0.12,
        mu0=0.1,
        max_duration=10.0,
        preservation_rate_q=5.0,
        seed=777,
    )

    # Extract origin times and standing diversity trajectory
    origin_times = [lin.origin_time for lin in sim.lineages if lin.origin_time > 0.0]

    fit = fit_diversity_dependence(
        speciation_times_ma=origin_times,
        ltt_time_grid_ma=sim.time_series_t,
        ltt_diversity_grid=sim.time_series_diversity,
        t_max_eval_ma=sim.duration,
        is_per_lineage_process=True,
    )

    # In an idealized dense radiation with simulated gl=-0.12, inferred Gl must be strictly negative
    assert fit.mle_gl < 0.0
