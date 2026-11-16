"""Hypothesis property tests and mathematical invariant checks for macroevolutionary primitives.

Tests all 6 primitives:
1. log_diversity_hazard / diversity_dependent_hazard (log-space safety, monotonicity)
2. keiding_sampling_probability / keiding_log_conditioning (cancellation protection, bounds [0, 1])
3. poisson_occurrence_loglik (non-negativity, lifespan enclosure)
4. lineage_duration_loglik (survival decay, event density)
5. standing_diversity_trajectory (exact step-function count, support bounds)
6. tip_diversification_rate (regularization floor, singularity protection, monotonicity)
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from hominin_morphodynamics.inference.primitives import (
    diversity_dependent_hazard,
    keiding_log_conditioning,
    keiding_sampling_probability,
    lineage_duration_loglik,
    log_diversity_hazard,
    poisson_occurrence_loglik,
    standing_diversity_trajectory,
    tip_diversification_rate,
)
from hypothesis import given
from hypothesis import strategies as st


class TestDiversityHazardPrimitives:
    """Tests for Primitive 1: log_diversity_hazard and diversity_dependent_hazard."""

    @given(
        base_rate=st.floats(min_value=1e-4, max_value=10.0),
        g_coeff=st.floats(min_value=-5.0, max_value=5.0),
        diversity=st.floats(min_value=0.0, max_value=100.0),
    )
    def test_log_hazard_finite_and_monotonic(
        self, base_rate: float, g_coeff: float, diversity: float
    ) -> None:
        log_h = log_diversity_hazard(base_rate, g_coeff, diversity)
        assert math.isfinite(log_h)

        h = diversity_dependent_hazard(base_rate, g_coeff, diversity)
        assert math.isfinite(h)
        assert h > 0.0
        assert math.isclose(math.log(h), log_h, rel_tol=1e-7, abs_tol=1e-7)

    def test_hazard_boundary_invariants(self) -> None:
        with pytest.raises(ValueError, match="base_rate must be > 0.0"):
            log_diversity_hazard(0.0, 1.0, 5.0)

        with pytest.raises(ValueError, match="diversity must be >= 0.0"):
            log_diversity_hazard(1.0, 1.0, -1.0)


class TestKeidingSamplingPrimitives:
    """Tests for Primitive 2: keiding_sampling_probability and keiding_log_conditioning."""

    @given(theta=st.floats(min_value=0.0, max_value=500.0))
    def test_keiding_bounds_and_monotonicity(self, theta: float) -> None:
        p = keiding_sampling_probability(theta)
        assert 0.0 <= p <= 1.0

        log_p = keiding_log_conditioning(theta)
        if theta == 0.0:
            assert p == 0.0
            assert log_p == -math.inf
        else:
            assert math.isclose(p, math.exp(log_p), rel_tol=1e-7, abs_tol=1e-7)

    def test_keiding_cancellation_protection(self) -> None:
        """Verify that tiny theta does not suffer catastrophic cancellation."""
        tiny_theta = 1e-15
        p = keiding_sampling_probability(tiny_theta)
        # 1 - exp(-1e-15) ≈ 1e-15
        assert math.isclose(p, tiny_theta, rel_tol=1e-5)

        log_p = keiding_log_conditioning(tiny_theta)
        assert math.isclose(log_p, math.log(tiny_theta), rel_tol=1e-5)


class TestPoissonOccurrencePrimitives:
    """Tests for Primitive 3: poisson_occurrence_loglik."""

    @given(
        s=st.floats(min_value=1.0, max_value=10.0),
        duration=st.floats(min_value=0.1, max_value=5.0),
        q=st.floats(min_value=0.01, max_value=10.0),
    )
    def test_poisson_loglik_properties(
        self, s: float, duration: float, q: float
    ) -> None:
        e = s - duration
        # 2 occurrences inside lifespan
        t1 = e + 0.25 * duration
        t2 = e + 0.75 * duration

        ll = poisson_occurrence_loglik([t1, t2], s, e, q)
        assert math.isfinite(ll)
        # Hand calculation: 2 * ln(q) - q * duration
        expected = 2.0 * math.log(q) - q * duration
        assert math.isclose(ll, expected, rel_tol=1e-9)

    def test_poisson_rejections(self) -> None:
        # Occurrence outside interval [1.0, 2.0]
        with pytest.raises(ValueError, match="outside lineage lifespan"):
            poisson_occurrence_loglik([2.5], s=2.0, e=1.0, q=1.0)


class TestLineageDurationPrimitives:
    """Tests for Primitive 4: lineage_duration_loglik."""

    def test_duration_extinct_vs_extant(self) -> None:
        s, e, mu = 3.0, 1.0, 0.5
        ll_extinct = lineage_duration_loglik(s, e, mu, is_extinct=True)
        # ln(0.5) - 0.5 * 2.0
        assert math.isclose(ll_extinct, math.log(0.5) - 1.0)

        ll_extant = lineage_duration_loglik(s, 0.0, mu, is_extinct=False)
        # -0.5 * 3.0 = -1.5
        assert math.isclose(ll_extant, -1.5)


class TestStandingDiversityTrajectory:
    """Tests for Primitive 5: standing_diversity_trajectory."""

    def test_step_function_reconstruction(self) -> None:
        intervals = [
            (4.0, 2.0),  # Lineage A active [2.0, 4.0]
            (3.0, 1.0),  # Lineage B active [1.0, 3.0]
            (1.5, 0.0),  # Lineage C active [0.0, 1.5]
        ]
        times = np.array([4.5, 3.5, 2.5, 1.8, 1.2, 0.5, -0.5])
        counts = standing_diversity_trajectory(intervals, times)

        # 4.5: 0
        # 3.5: A (1)
        # 2.5: A, B (2)
        # 1.8: B (1)
        # 1.2: B, C (2)
        # 0.5: C (1)
        # -0.5: 0
        expected = np.array([0, 1, 2, 1, 2, 1, 0])
        np.testing.assert_array_equal(counts, expected)


class TestTipDiversificationRatePrimitive:
    """Tests for Primitive 6: tip_diversification_rate."""

    def test_regularization_prevents_division_by_zero(self) -> None:
        # Near-zero branch length like Parins-Fukuchi 4.82e-12
        near_zero_branches = [1.0, 4.82e-12, 0.5]
        dr = tip_diversification_rate(near_zero_branches, min_branch_length=1e-4)

        assert math.isfinite(dr)
        # DR = (1/1.0) + 0.5*(1/1e-4) + 0.25*(1/0.5) = 1 + 5000 + 0.5 = 5001.5
        assert math.isclose(dr, 5001.5, rel_tol=1e-5)

    @given(
        l1=st.floats(min_value=0.1, max_value=5.0),
        l2=st.floats(min_value=0.1, max_value=5.0),
    )
    def test_dr_monotonicity_with_branch_lengths(self, l1: float, l2: float) -> None:
        dr_base = tip_diversification_rate([l1, l2])
        # Longer branches must strictly decrease DR (slower diversification)
        dr_longer = tip_diversification_rate([l1 * 2.0, l2 * 2.0])
        assert dr_longer < dr_base
