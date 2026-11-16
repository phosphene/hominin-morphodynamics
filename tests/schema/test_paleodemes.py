"""Tests for paleodeme and basin projections."""

from __future__ import annotations

from pathlib import Path

from hominin_morphodynamics.schema.paleodemes import (
    GeographicBasin,
    project_paleodemes,
)
from hominin_morphodynamics.schema.specimens import (
    EcologicalGrade,
    ingest_specimen_database,
)

RAW_XLSX = Path(__file__).parent.parent.parent / "data/raw/van_holstein_2024/Occurrence_database.xlsx"


def test_paleodeme_projection_invariants() -> None:
    occs, _ = ingest_specimen_database(RAW_XLSX)
    paleodemes = project_paleodemes(occs, time_window_myr=0.5)

    assert len(paleodemes) > 0

    # Ensure major basins are represented
    basins = set(p.basin for p in paleodemes)
    assert GeographicBasin.TURKANA in basins
    assert GeographicBasin.AFAR_RIFT in basins
    assert GeographicBasin.SOUTH_AFRICA_KARST in basins
    assert GeographicBasin.TRANS_CAUCASUS in basins

    # Ensure all occurrences in paleodemes map to valid raw indices
    for p in paleodemes:
        assert p.sample_size > 0
        assert len(p.occurrence_indices) == p.sample_size
        for idx in p.occurrence_indices:
            assert 0 <= idx < len(occs)

    # Check Dmanisi cluster (Homo 2, ~1.8 Ma)
    dmanisi_clusters = [
        p for p in paleodemes if p.basin == GeographicBasin.TRANS_CAUCASUS
    ]
    assert len(dmanisi_clusters) >= 1
    assert any(c.grade == EcologicalGrade.HOMO_2 for c in dmanisi_clusters)
