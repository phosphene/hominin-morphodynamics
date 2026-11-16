"""Tests for composite taphonomically conditioned diversification likelihood engine."""

from __future__ import annotations

import math
import pytest

from hominin_morphodynamics.inference.joint_likelihood import (
    JointLikelihoodResult,
    LineageOccurrenceData,
    evaluate_joint_diversification_loglik,
)


@pytest.fixture
def synthetic_hominin_clade():
    """Synthetic 3-lineage clade with differing preservation and basin assignments."""
    return [
        LineageOccurrenceData(
            lineage_id="Australopithecus_afarensis",
            speciation_time_ma=3.85,
            extinction_time_ma=2.95,
            occurrence_times_ma=[3.80, 3.65, 3.40, 3.20, 3.00],
            is_extinct=True,
            basin="afar_rift",
        ),
        LineageOccurrenceData(
            lineage_id="Paranthropus_boisei",
            speciation_time_ma=2.30,
            extinction_time_ma=1.34,
            occurrence_times_ma=[2.25, 2.00, 1.80, 1.50, 1.40],
            is_extinct=True,
            basin="turkana_basin",
        ),
        LineageOccurrenceData(
            lineage_id="Homo_sapiens",
            speciation_time_ma=0.30,
            extinction_time_ma=0.0,
            occurrence_times_ma=[0.25, 0.15, 0.05],
            is_extinct=False,
            basin="other",
        ),
    ]


def test_joint_likelihood_evaluates_finite_and_decomposed(synthetic_hominin_clade):
    """Verify joint likelihood evaluates to finite numbers with expected decomposition."""
    res = evaluate_joint_diversification_loglik(
        lineages=synthetic_hominin_clade,
        mu=0.5,
        preservation_rates={"afar_rift": 5.0, "turkana_basin": 6.0, "default": 3.0},
        lambda0=0.8,
        gl=-0.05,
    )

    assert isinstance(res, JointLikelihoodResult)
    assert math.isfinite(res.log_lik_total)
    assert math.isfinite(res.log_lik_durations)
    assert math.isfinite(res.log_lik_occurrences)
    assert math.isfinite(res.log_lik_conditioning)
    assert res.num_lineages == 3
    assert res.num_occurrences == 13

    # Check that total = durations + occurrences - conditioning
    expected_total = res.log_lik_durations + res.log_lik_occurrences - res.log_lik_conditioning
    assert abs(res.log_lik_total - expected_total) < 1e-6


def test_joint_likelihood_penalizes_poor_preservation_fit(synthetic_hominin_clade):
    """Likelihood of occurrences should peak near empirical sampling frequency."""
    # When q is absurdly high (e.g. 1000 fossils/Myr), expected fossils is huge -> large negative penalty
    res_normal = evaluate_joint_diversification_loglik(
        lineages=synthetic_hominin_clade,
        mu=0.5,
        preservation_rates=5.0,
    )
    res_extreme_q = evaluate_joint_diversification_loglik(
        lineages=synthetic_hominin_clade,
        mu=0.5,
        preservation_rates=1000.0,
    )

    # Extreme mismatch should have substantially worse (more negative) total likelihood
    assert res_normal.log_lik_total > res_extreme_q.log_lik_total


def test_joint_likelihood_requires_positive_parameters(synthetic_hominin_clade):
    """Invalid parameter values (mu <= 0, q <= 0) must raise ValueError."""
    with pytest.raises(ValueError, match="mu must be > 0"):
        evaluate_joint_diversification_loglik(
            lineages=synthetic_hominin_clade,
            mu=-0.1,
            preservation_rates=5.0,
        )

    with pytest.raises(ValueError, match="Preservation rate q must be > 0"):
        evaluate_joint_diversification_loglik(
            lineages=synthetic_hominin_clade,
            mu=0.5,
            preservation_rates=-2.0,
        )
