"""Tests for Layer 2 defect rectification and stratigraphic invariant validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from hominin_morphodynamics.schema.paleodemes import (
    RECTIFIED_INVERSIONS,
    RectifiedOccurrence,
    rectify_all_occurrences,
    rectify_occurrence,
)
from hominin_morphodynamics.schema.specimens import ingest_specimen_database


@pytest.fixture
def raw_occurrences():
    raw_path = (
        Path(__file__).parent.parent.parent
        / "data"
        / "raw"
        / "van_holstein_2024"
        / "Occurrence_database.xlsx"
    )
    occs, _ = ingest_specimen_database(raw_path)
    return occs


def test_rectification_fixes_all_five_inversions(raw_occurrences):
    """Verify that all 5 known inverted records are rectified and satisfy max >= min."""
    rectified = rectify_all_occurrences(raw_occurrences)

    # Check total count matches raw count (385)
    assert len(rectified) == len(raw_occurrences)

    # Identify which records were rectified
    rectified_indices = {r.index for r in rectified if r.is_rectified}
    assert rectified_indices == set(RECTIFIED_INVERSIONS.keys())
    assert len(rectified_indices) == 5

    # Check each rectified record satisfies max >= min
    for r in rectified:
        if r.is_rectified:
            assert r.rectification_note is not None
            if r.site_max_ma is not None and r.site_min_ma is not None:
                assert r.site_max_ma >= r.site_min_ma
            if r.strat_max_ma is not None and r.strat_min_ma is not None:
                assert r.strat_max_ma >= r.strat_min_ma


def test_rectification_preserves_unaffected_records(raw_occurrences):
    """Verify that records without defects are preserved exactly."""
    rectified = rectify_all_occurrences(raw_occurrences)

    for raw, rect in zip(raw_occurrences, rectified):
        if raw.index not in RECTIFIED_INVERSIONS:
            assert not rect.is_rectified
            assert rect.rectification_note is None
            assert rect.site_max_ma == raw.site_max_ma
            assert rect.site_min_ma == raw.site_min_ma
            assert rect.strat_max_ma == raw.strat_max_ma
            assert rect.strat_min_ma == raw.strat_min_ma
            assert rect.species_name == raw.species_name
            assert rect.grade == raw.grade
            assert rect.specimen_codes == raw.specimen_codes


def test_rectified_occurrences_pass_stratigraphic_invariants(raw_occurrences):
    """Ensure that 100% of Layer 2 occurrences satisfy stratigraphic monotonicity."""
    rectified = rectify_all_occurrences(raw_occurrences)

    for r in rectified:
        # Effective dates must also satisfy max >= min
        eff_max = r.effective_max_ma
        eff_min = r.effective_min_ma
        if eff_max is not None and eff_min is not None:
            assert eff_max >= eff_min
