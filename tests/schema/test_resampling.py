"""Tests for stratigraphically coupled horizon resampling."""

from __future__ import annotations

from pathlib import Path

import pytest

from hominin_morphodynamics.schema.paleodemes import rectify_all_occurrences
from hominin_morphodynamics.schema.resampling import (
    generate_coupled_replicates,
    get_horizon_key,
    sample_stratigraphically_coupled_horizons,
)
from hominin_morphodynamics.schema.specimens import ingest_specimen_database


@pytest.fixture
def rectified_occurrences():
    raw_path = (
        Path(__file__).parent.parent.parent
        / "data"
        / "raw"
        / "van_holstein_2024"
        / "Occurrence_database.xlsx"
    )
    raw, _ = ingest_specimen_database(raw_path)
    return rectify_all_occurrences(raw)


def test_realized_dates_fall_strictly_within_bounds(rectified_occurrences):
    """Every realized date must satisfy min_ma <= realized_age <= max_ma."""
    realized = sample_stratigraphically_coupled_horizons(rectified_occurrences, rng=123)

    assert len(realized) == len(rectified_occurrences)
    for r in realized:
        assert r.effective_min_ma <= r.realized_age_ma <= r.effective_max_ma + 1e-6


def test_coupled_horizons_preserve_intra_bed_coherence(rectified_occurrences):
    """Specimens belonging to the identical horizon with matching bounds must get identical dates."""
    realized = sample_stratigraphically_coupled_horizons(rectified_occurrences, rng=999)

    by_horizon: dict[str, list] = {}
    for r in realized:
        by_horizon.setdefault(r.horizon_key, []).append(r)

    # For any horizon where multiple specimens share exact same bounds, their ages must match
    for h_key, dates in by_horizon.items():
        if len(dates) > 1:
            first = dates[0]
            identical_bounds = all(
                d.effective_max_ma == first.effective_max_ma
                and d.effective_min_ma == first.effective_min_ma
                for d in dates
            )
            if identical_bounds:
                for d in dates:
                    assert abs(d.realized_age_ma - first.realized_age_ma) < 1e-6


def test_replicates_are_deterministic_and_variant(rectified_occurrences):
    """Multiple replicates with different seeds produce different draws, seedable is reproducible."""
    rep_a1 = generate_coupled_replicates(rectified_occurrences, num_replicates=2, seed=42)
    rep_a2 = generate_coupled_replicates(rectified_occurrences, num_replicates=2, seed=42)
    rep_b = generate_coupled_replicates(rectified_occurrences, num_replicates=2, seed=77)

    # Seed 42 is perfectly deterministic
    for d1, d2 in zip(rep_a1[0], rep_a2[0]):
        assert d1.realized_age_ma == d2.realized_age_ma

    # Seed 77 differs from Seed 42 for intervals with positive duration
    diffs = [
        abs(d1.realized_age_ma - db.realized_age_ma)
        for d1, db in zip(rep_a1[0], rep_b[0])
        if d1.effective_max_ma > d1.effective_min_ma
    ]
    assert any(diff > 1e-4 for diff in diffs)
