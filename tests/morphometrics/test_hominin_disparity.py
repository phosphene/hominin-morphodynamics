"""L5 Consumer verification tests for Tier 4 hominin continuous morphological disparity."""

from __future__ import annotations

import dataclasses
import math
import numpy as np
import pytest

from hominin_morphodynamics.morphometrics import (
    CANONICAL_HOMININ_OSTEOMETRICS,
    CraniodentalSpecimen,
    hominin_disparity_report,
)
from hominin_morphodynamics.schema.specimens import EcologicalGrade


def test_canonical_osteometrics_caliper_and_dirt_invariants() -> None:
    assert len(CANONICAL_HOMININ_OSTEOMETRICS) >= 12
    for spec in CANONICAL_HOMININ_OSTEOMETRICS:
        assert spec.age_ma >= 0.0
        assert spec.endocranial_volume_cc > 0.0
        assert spec.molar_m1_area_mm2 > 0.0
        assert spec.bicondylar_breadth_mm > 0.0
        assert spec.estimated_body_mass_kg > 0.0
        assert spec.measurement_error_cv > 0.0
        assert spec.taphonomic_fragility >= 1.0

    with pytest.raises(ValueError):
        dataclasses.replace(CANONICAL_HOMININ_OSTEOMETRICS[0], taphonomic_fragility=0.5)


def test_hominin_disparity_report_allometric_variance_reduction_and_trajectories() -> None:
    report = hominin_disparity_report(CANONICAL_HOMININ_OSTEOMETRICS, time_window_myr=1.0)

    # Allometric residualization must remove body-size variance (residual disparity < raw log disparity)
    assert report.clade_residual_disparity.weighted_variance < report.clade_raw_log_disparity.weighted_variance
    assert report.clade_residual_disparity.weighted_variance > 0.0
    assert report.clade_residual_disparity.mean_pairwise_distance > 0.0

    # Endocranial volume scales positively with body mass across hominins
    assert report.allometry.slopes[0] > 0.5
    assert not report.allometry.residuals.flags.writeable

    # Temporal slices span Plio-Pleistocene (at least 3 distinct 1-Myr windows)
    assert len(report.time_slices) >= 3
    for ts in report.time_slices:
        assert ts.allometric_residual_disparity.weighted_variance >= 0.0
        assert ts.allometric_residual_disparity.effective_sample_size <= ts.num_specimens + 1e-12

    # All 5 major Foley ecological grades are represented
    grades = {gp.grade for gp in report.grade_profiles}
    assert {
        EcologicalGrade.AUSTRALOPITHECINE,
        EcologicalGrade.PARANTHROPUS,
        EcologicalGrade.HOMO_1,
        EcologicalGrade.HOMO_2,
        EcologicalGrade.HOMO_3,
    }.issubset(grades)


def test_taphonomic_fragility_downweights_distorted_specimen() -> None:
    """Increasing taphonomic fragility on a fragmented specimen reduces its leverage on centroid & N_eff."""
    base_report = hominin_disparity_report(CANONICAL_HOMININ_OSTEOMETRICS)
    penalized = list(CANONICAL_HOMININ_OSTEOMETRICS)
    # Heavily penalize OH 24 (crushed cranium) fragility
    oh24_idx = next(i for i, s in enumerate(penalized) if s.specimen_id == "OH 24")
    penalized[oh24_idx] = dataclasses.replace(penalized[oh24_idx], taphonomic_fragility=20.0)
    pen_report = hominin_disparity_report(penalized)

    assert math.isfinite(pen_report.clade_residual_disparity.weighted_variance)
    assert pen_report.clade_residual_disparity.effective_sample_size < (
        base_report.clade_residual_disparity.effective_sample_size
    )
