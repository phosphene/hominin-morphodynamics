"""Tests for the cross-domain comparative metrics extractor."""

from __future__ import annotations

import pytest
from hominin_morphodynamics.inference.comparative_metrics import (
    DomainComparisonReport,
    generate_canonical_comparison,
)


def test_cross_domain_comparison_generation():
    """Verify that the cross-domain report generates with expected quantitative metrics."""
    report = generate_canonical_comparison()
    assert isinstance(report, DomainComparisonReport)

    # Check Insular metrics
    assert report.insular_carrying_capacity_k_identified is True
    assert report.insular_profile_lrt_p_value < 0.05
    assert report.insular_spatial_extent_km2 < 10000.0

    # Check Continental Hominin metrics
    assert report.hominin_carrying_capacity_identified is False
    assert report.hominin_profile_lrt_p_value >= 0.25
    assert report.hominin_spatial_extent_km2 > 10000000.0

    # Check dictionary serialization
    d = report.to_dict()
    assert "insular_model" in d
    assert "continental_hominin_model" in d
    assert "category_error_verdict" in d
    assert d["insular_model"]["k_identified"] is True
    assert d["continental_hominin_model"]["k_identified"] is False
