"""Tests for hominin specimen schema and database ingestion."""

from __future__ import annotations

from pathlib import Path

from hominin_morphodynamics.schema.specimens import (
    EcologicalGrade,
    ingest_specimen_database,
)

RAW_XLSX = Path(__file__).parent.parent.parent / "data/raw/van_holstein_2024/Occurrence_database.xlsx"


def test_specimen_database_schema_and_grades() -> None:
    assert RAW_XLSX.exists(), f"Raw occurrence workbook missing: {RAW_XLSX}"
    occurrences, summary = ingest_specimen_database(RAW_XLSX)

    # Invariant: 385 valid occurrences
    assert len(occurrences) == 385
    assert summary["total_occurrences"] == 385

    # Check Foley ecological grade distribution
    grades = summary["grade_distribution"]
    assert grades[EcologicalGrade.HOMO_2.value] == 84  # H. erectus
    assert grades[EcologicalGrade.HOMO_3.value] == 166  # H. heidelbergensis + neanderthalensis + sapiens
    assert grades[EcologicalGrade.PARANTHROPUS.value] == 53  # aethiopicus + boisei + robustus
    assert grades[EcologicalGrade.AUSTRALOPITHECINE.value] == 56

    # Verify specimen code extraction
    with_specimens = [o for o in occurrences if len(o.specimen_codes) > 0]
    assert len(with_specimens) >= 24

    # Verify age span calculation: exactly 378 bounded, 7 occurrences completely unbounded
    bounded_occs = [o for o in occurrences if o.age_span_myr is not None]
    assert len(bounded_occs) == 378
    unbounded_occs = [o for o in occurrences if o.age_span_myr is None]
    assert len(unbounded_occs) == 7
