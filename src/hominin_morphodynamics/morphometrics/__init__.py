"""Tier 4 continuous morphological disparity and craniodental osteometrics.

Built directly on ``phosphene.holonomy.morphometrics`` (Kendall shape space Procrustes,
OLS allometric residualization, and Foote weighted disparity MD_W / MPD_W).
"""

from hominin_morphodynamics.morphometrics.disparity_trajectory import (
    GradeDisparitySummary,
    HomininDisparityReport,
    TimeSliceDisparity,
    hominin_disparity_report,
)
from hominin_morphodynamics.morphometrics.osteometrics import (
    CANONICAL_HOMININ_OSTEOMETRICS,
    CraniodentalSpecimen,
)

__all__ = [
    "CraniodentalSpecimen",
    "CANONICAL_HOMININ_OSTEOMETRICS",
    "TimeSliceDisparity",
    "GradeDisparitySummary",
    "HomininDisparityReport",
    "hominin_disparity_report",
]
