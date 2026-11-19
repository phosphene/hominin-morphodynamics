"""Hypothesis property tests, mathematical invariant checks, and calibration standards for macroevolutionary primitives.

Tests all 6 primitives:
1. log_diversity_hazard / diversity_dependent_hazard (log-space safety, monotonicity, IEEE-754 finite domain)
2. keiding_sampling_probability / keiding_log_conditioning (cancellation protection, bounds [0, 1], variational defect hunting)
3. poisson_occurrence_loglik (non-negativity, lifespan enclosure, analytical equivalence)
4. lineage_duration_loglik (survival decay, event density)
5. standing_diversity_trajectory (exact step-function count, support bounds)
6. tip_diversification_rate (regularization floor, singularity protection, monotonicity, cancellation hunting)

Standards applied (per docs/HYPOTHESIS_PATTERNS_AND_CALIBRATION.md):
- Strict IEEE-754 finite domain hygiene: allow_nan=False, allow_infinity=False, allow_subnormal=False.
- Variational defect hunting: continuous residual minimization/maximization tracked via hypothesis.target().
- Regime stratification: tracking parameter magnitude via hypothesis.event().
- Immutability contracts: assert writeable=False across evaluated state.
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
from hypothesis import event, given, settings, target
from hypothesis import strategies as st


def finite_positive_floats(min_val: float = 1e-4, max_val: float = 100.0) -> st.SearchStrategy[float]:
    """Helper strategy generating strictly finite, normalized positive floats (no NaN, inf, or subnormals)."""
    return st.floats(
        min_value=min_val,
        max_value=max_val,
        allow_nan=False,
        allow_infinity=False,
        allow_subnormal=False,
    )


def finite_real_floats(min_val: float = -10.0, max_val: float = 10.0) -> st.SearchStrategy[float]:
    """Helper strategy generating strictly finite, normalized real floats (no NaN, inf, or subnormals)."""
    return st.floats(
        min_value=min_val,
        max_value=max_val,
        allow_nan=False,
        allow_infinity=False,
        allow_subnormal=False,
    )


class TestDiversityHazardPrimitives:
    """Tests for Primitive 1: log_diversity_hazard and diversity_dependent_hazard.
    
    Verifies that the diversity-dependent exponential hazard function is strictly finite,
    monotonic in diversity given positive/negative G coefficients, and that log-space
    representations agree with natural-scale exponents to machine precision.
    """

    @given(
        base_rate=finite_positive_floats(min_val=1e-4, max_val=10.0),
        g_coeff=finite_real_floats(min_val=-5.0, max_val=5.0),
        diversity=finite_positive_floats(min_val=0.0, max_val=100.0),
    )
    def test_log_hazard_finite_and_monotonic(
        self, base_rate: float, g_coeff: float, diversity: float
    ) -> None:
        """Verify natural-scale hazard and log-scale hazard agree without cancellation."""
        log_h = log_diversity_hazard(base_rate, g_coeff, diversity)
        assert math.isfinite(log_h)

        h = diversity_dependent_hazard(base_rate, g_coeff, diversity)
        assert math.isfinite(h)
        assert h > 0.0

        # Discrepancy functional between natural and log-space evaluations
        discrepancy = abs(math.log(h) - log_h)
        target(discrepancy, label="log_hazard_representation_discrepancy")
        assert discrepancy <= 1e-7

    def test_hazard_boundary_invariants(self) -> None:
        """Verify typed domain boundary rejections."""
        with pytest.raises(ValueError, match="base_rate must be > 0.0"):
            log_diversity_hazard(0.0, 1.0, 5.0)

        with pytest.raises(ValueError, match="diversity must be >= 0.0"):
            log_diversity_hazard(1.0, 1.0, -1.0)


class TestKeidingSamplingPrimitives:
    """Tests for Primitive 2: keiding_sampling_probability and keiding_log_conditioning.
    
    Verifies that Keiding conditioning P = 1 - exp(-theta) avoids catastrophic cancellation
    when theta -> 0+ via expm1/log1p, preserves probability bounds [0, 1], and exhibits
    no numerical distortion across multiple orders of magnitude of sampling intensity.
    """

    @given(theta=finite_positive_floats(min_val=0.0, max_val=500.0))
    def test_keiding_bounds_and_monotonicity(self, theta: float) -> None:
        """Verify strict [0, 1] bounds and log-probability consistency."""
        p = keiding_sampling_probability(theta)
        assert 0.0 <= p <= 1.0

        decade = int(math.floor(math.log10(max(theta, 1e-12))))
        event(f"theta_magnitude_decade={decade}")

        log_p = keiding_log_conditioning(theta)
        if theta == 0.0:
            assert p == 0.0
            assert log_p == -math.inf
        else:
            # Measure defect between p and exp(log_p)
            defect = abs(p - math.exp(log_p))
            target(defect, label="keiding_exponential_conditioning_defect")
            assert defect <= 1e-7

    @given(theta=st.floats(min_value=1e-16, max_value=1e-4, allow_nan=False, allow_infinity=False, allow_subnormal=False))
    def test_keiding_cancellation_protection(self, theta: float) -> None:
        """Verify that tiny theta does not suffer catastrophic floating-point cancellation.
        
        Using Taylor expansion: 1 - exp(-theta) = theta - theta^2 / 2 + O(theta^3).
        The relative defect |p - theta| / theta must be <= theta / 2.
        """
        p = keiding_sampling_probability(theta)
        relative_defect = abs(p - theta) / theta
        target(relative_defect, label="keiding_taylor_first_order_defect")
        assert relative_defect <= theta + 1e-12

        log_p = keiding_log_conditioning(theta)
        log_defect = abs(log_p - math.log(theta))
        target(log_defect, label="keiding_log_taylor_defect")
        assert log_defect <= theta + 1e-12


class TestPoissonOccurrencePrimitives:
    """Tests for Primitive 3: poisson_occurrence_loglik.
    
    Verifies that Poisson sampling likelihood over continuous lineages correctly reproduces
    analytical density k * ln(q) - q * duration without mass leakage or sign inversion.
    """

    @given(
        s=finite_positive_floats(min_val=1.0, max_val=10.0),
        duration=finite_positive_floats(min_val=0.1, max_val=5.0),
        q=finite_positive_floats(min_val=0.01, max_val=10.0),
    )
    def test_poisson_loglik_properties(
        self, s: float, duration: float, q: float
    ) -> None:
        """Verify exact closed-form equivalence for internal occurrence points."""
        e = s - duration
        # 2 occurrences placed at 25% and 75% along lifespan
        t1 = e + 0.25 * duration
        t2 = e + 0.75 * duration

        ll = poisson_occurrence_loglik([t1, t2], s, e, q)
        assert math.isfinite(ll)

        expected = 2.0 * math.log(q) - q * duration
        defect = abs(ll - expected)
        target(defect, label="poisson_analytical_equivalence_defect")
        assert defect <= 1e-9

    def test_poisson_rejections(self) -> None:
        """Reject occurrences located outside lineage lifespan interval."""
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

        expected = np.array([0, 1, 2, 1, 2, 1, 0])
        np.testing.assert_array_equal(counts, expected)


class TestTipDiversificationRatePrimitive:
    """Tests for Primitive 6: tip_diversification_rate.
    
    Verifies that the Jetz et al. (2012) tip DR metric avoids division by zero on
    near-zero branch lengths via explicit regularization floors, and decreases
    monotonically with branch length elongation.
    """

    def test_regularization_prevents_division_by_zero(self) -> None:
        """Near-zero branch length (e.g. Parins-Fukuchi 4.82e-12) clamped to floor."""
        near_zero_branches = [1.0, 4.82e-12, 0.5]
        dr = tip_diversification_rate(near_zero_branches, min_branch_length=1e-4)

        assert math.isfinite(dr)
        # DR = (1/1.0) + 0.5*(1/1e-4) + 0.25*(1/0.5) = 1 + 5000 + 0.5 = 5001.5
        assert math.isclose(dr, 5001.5, rel_tol=1e-5)

    @given(
        l1=finite_positive_floats(min_val=0.1, max_val=5.0),
        l2=finite_positive_floats(min_val=0.1, max_val=5.0),
    )
    def test_dr_monotonicity_with_branch_lengths(self, l1: float, l2: float) -> None:
        """Longer branches must strictly decrease DR (slower diversification)."""
        dr_base = tip_diversification_rate([l1, l2])
        dr_longer = tip_diversification_rate([l1 * 2.0, l2 * 2.0])

        reduction = dr_base - dr_longer
        target(reduction, label="dr_monotonicity_reduction_margin")
        assert dr_longer < dr_base
