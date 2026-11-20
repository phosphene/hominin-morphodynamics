"""Continuous hominin morphological disparity trajectories MD_W(t) (Tier 4 Native Inference).

Orchestrates hominin craniodental osteometrics into allometric residuals and
inverse-variance taphonomically weighted continuous disparity trajectories, delegating
all mathematical kernels strictly to ``phosphene.holonomy.morphometrics``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from phosphene.holonomy.morphometrics import (
    AllometricDecomposition,
    MorphologicalDisparity,
    allometric_residuals,
    inverse_variance_weights,
    weighted_morphological_disparity,
)

from hominin_morphodynamics.morphometrics.osteometrics import CraniodentalSpecimen
from hominin_morphodynamics.schema.paleodemes import GeographicBasin
from hominin_morphodynamics.schema.specimens import EcologicalGrade


@dataclass(frozen=True)
class TimeSliceDisparity:
    """Continuous morphological disparity summary for a single Plio-Pleistocene time slice."""

    time_slice_ma: tuple[float, float]  # (max_age_ma, min_age_ma)
    num_specimens: int
    distinct_basins: tuple[GeographicBasin, ...]
    distinct_grades: tuple[EcologicalGrade, ...]
    raw_log_disparity: MorphologicalDisparity
    allometric_residual_disparity: MorphologicalDisparity


@dataclass(frozen=True)
class GradeDisparitySummary:
    """Continuous allometric residual disparity summary for a Foley ecological grade."""

    grade: EcologicalGrade
    num_specimens: int
    specimen_ids: tuple[str, ...]
    disparity: MorphologicalDisparity


@dataclass(frozen=True)
class HomininDisparityReport:
    """Complete Tier 4 continuous morphological disparity analysis over hominin specimens."""

    allometry: AllometricDecomposition
    clade_raw_log_disparity: MorphologicalDisparity
    clade_residual_disparity: MorphologicalDisparity
    time_slices: tuple[TimeSliceDisparity, ...]
    grade_profiles: tuple[GradeDisparitySummary, ...]


def hominin_disparity_report(
    specimens: Sequence[CraniodentalSpecimen],
    time_window_myr: float = 1.0,
) -> HomininDisparityReport:
    """Compute clade-wide, time-sliced, and grade-level continuous disparity via ``holonomy.morphometrics``.

    Steps (Three-Phase Process):
        1. Project ``CraniodentalSpecimen`` records into physical trait & body-mass arrays.
        2. Remove body-size allometry via ``holonomy.morphometrics.allometric_residuals``.
        3. Weight specimens inversely by measurement error CV^2 * taphonomic fragility via
           ``holonomy.morphometrics.inverse_variance_weights``.
        4. Compute weighted centroid variance MD_W and pairwise distance MPD_W clade-wide,
           per temporal horizon, and per Foley ecological grade.
    """
    if len(specimens) < 2:
        raise ValueError(f"At least 2 specimens are required for allometric disparity analysis, got {len(specimens)}")
    if time_window_myr <= 0.0:
        raise ValueError(f"time_window_myr must be > 0.0, got {time_window_myr}")

    traits = np.array([s.trait_vector for s in specimens], dtype=np.float64)
    body_mass = np.array([s.estimated_body_mass_kg for s in specimens], dtype=np.float64)
    weights = inverse_variance_weights(
        measurement_errors=[s.measurement_error_cv for s in specimens],
        taphonomic_fragilities=[s.taphonomic_fragility for s in specimens],
    )

    allometry = allometric_residuals(traits, body_mass, log_transform=True)
    log_traits = np.log(traits)

    clade_raw = weighted_morphological_disparity(log_traits, weights=weights)
    clade_res = weighted_morphological_disparity(allometry.residuals, weights=weights)

    # Time-slice binning
    slice_buckets: dict[int, list[int]] = {}
    for idx, spec in enumerate(specimens):
        t_bin = int(spec.age_ma / time_window_myr)
        slice_buckets.setdefault(t_bin, []).append(idx)

    time_slices: list[TimeSliceDisparity] = []
    for t_bin in sorted(slice_buckets.keys(), reverse=True):
        idxs = slice_buckets[t_bin]
        sub_specs = [specimens[i] for i in idxs]
        sub_w = weights[idxs]
        time_slices.append(
            TimeSliceDisparity(
                time_slice_ma=((t_bin + 1) * time_window_myr, t_bin * time_window_myr),
                num_specimens=len(idxs),
                distinct_basins=tuple(sorted({s.basin for s in sub_specs}, key=lambda b: b.value)),
                distinct_grades=tuple(sorted({s.grade for s in sub_specs}, key=lambda g: g.value)),
                raw_log_disparity=weighted_morphological_disparity(log_traits[idxs], weights=sub_w),
                allometric_residual_disparity=weighted_morphological_disparity(
                    allometry.residuals[idxs], weights=sub_w
                ),
            )
        )

    # Foley ecological grade profiles
    grade_buckets: dict[EcologicalGrade, list[int]] = {}
    for idx, spec in enumerate(specimens):
        grade_buckets.setdefault(spec.grade, []).append(idx)

    grade_profiles: list[GradeDisparitySummary] = []
    for grade in sorted(grade_buckets.keys(), key=lambda g: g.value):
        idxs = grade_buckets[grade]
        grade_profiles.append(
            GradeDisparitySummary(
                grade=grade,
                num_specimens=len(idxs),
                specimen_ids=tuple(specimens[i].specimen_id for i in idxs),
                disparity=weighted_morphological_disparity(
                    allometry.residuals[idxs], weights=weights[idxs]
                ),
            )
        )

    return HomininDisparityReport(
        allometry=allometry,
        clade_raw_log_disparity=clade_raw,
        clade_residual_disparity=clade_res,
        time_slices=tuple(time_slices),
        grade_profiles=tuple(grade_profiles),
    )


__all__ = [
    "TimeSliceDisparity",
    "GradeDisparitySummary",
    "HomininDisparityReport",
    "hominin_disparity_report",
]
