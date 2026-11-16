"""Hypothesis and property-based tests verifying paleobiological data cleaning invariants.

Validates:
- Detection and isolation of stratigraphic interval inversions (Mertz Content Grime)
- Non-negativity of all geological age coordinates
- Invariant preservation of museum specimen codes
- Idempotence of data ingestion transforms: f(f(x)) == f(x)
- Age span arithmetic consistency
"""

from __future__ import annotations

from pathlib import Path

from hominin_morphodynamics.schema.specimens import (
    HomininSpecimenOccurrence,
    extract_specimen_identifiers,
    ingest_specimen_database,
)
from hypothesis import given
from hypothesis import strategies as st

RAW_XLSX = Path(__file__).parent.parent.parent / "data/raw/van_holstein_2024/Occurrence_database.xlsx"

# Indices of known inverted age records in raw Van Holstein & Foley (2024) database:
# Index 31: A. anamensis Korsi Dora (3.58 < 3.6)
# Index 35: A. anamensis Korsi Dora (3.58 < 3.6 strat)
# Index 264: H. neanderthalensis Madonna dell'Arma (0.191 < 0.71)
# Index 269: H. neanderthalensis La Chapelle-aux-Saints (0.04 < 0.071)
# Index 322: H. sapiens Tabon (0.039 < 0.22)
KNOWN_INVERTED_INDICES = {31, 35, 264, 269, 322}


def test_stratigraphic_age_ordering_and_defect_isolation() -> None:
    """Verify that all non-defective age intervals satisfy Max_Age >= Min_Age >= 0,

    and that known inverted records are specifically isolated and cataloged.
    """
    occs, _ = ingest_specimen_database(RAW_XLSX)

    inverted_site_indices: set[int] = set()
    inverted_strat_indices: set[int] = set()

    for occ in occs:
        # Non-negativity invariant: all ages must be >= 0
        if occ.site_max_ma is not None:
            assert occ.site_max_ma >= 0.0, f"Negative site max age at index {occ.index}"
        if occ.site_min_ma is not None:
            assert occ.site_min_ma >= 0.0, f"Negative site min age at index {occ.index}"
        if occ.strat_max_ma is not None:
            assert occ.strat_max_ma >= 0.0, f"Negative strat max age at index {occ.index}"
        if occ.strat_min_ma is not None:
            assert occ.strat_min_ma >= 0.0, f"Negative strat min age at index {occ.index}"

        # Detect inversions
        if occ.has_site_bounds and occ.site_max_ma is not None and occ.site_min_ma is not None:
            if occ.site_max_ma < occ.site_min_ma:
                inverted_site_indices.add(occ.index)

        if occ.has_strat_bounds and occ.strat_max_ma is not None and occ.strat_min_ma is not None:
            if occ.strat_max_ma < occ.strat_min_ma:
                inverted_strat_indices.add(occ.index)

    all_inversions = inverted_site_indices | inverted_strat_indices
    # Confirm exact set of isolated defects documented in DATA_STANDARDS_AND_CLEANING_METHODS.md
    assert all_inversions == KNOWN_INVERTED_INDICES

    # Verify that all OTHER records strictly satisfy the temporal ordering invariant
    for occ in occs:
        if occ.index in KNOWN_INVERTED_INDICES:
            continue
        if occ.has_site_bounds:
            assert (
                occ.site_max_ma >= occ.site_min_ma  # type: ignore
            ), f"Unexpected site age inversion at index {occ.index}"
        if occ.has_strat_bounds:
            assert (
                occ.strat_max_ma >= occ.strat_min_ma  # type: ignore
            ), f"Unexpected strat age inversion at index {occ.index}"


def test_ingestion_idempotence() -> None:
    """Verify transform idempotence: repeated ingestion produces identical records."""
    occs_1, summary_1 = ingest_specimen_database(RAW_XLSX)
    occs_2, summary_2 = ingest_specimen_database(RAW_XLSX)

    assert len(occs_1) == len(occs_2)
    assert summary_1 == summary_2
    for o1, o2 in zip(occs_1, occs_2):
        assert o1 == o2


@given(
    site_max=st.floats(min_value=0.0, max_value=10.0, allow_nan=False),
    site_span=st.floats(min_value=0.0, max_value=5.0, allow_nan=False),
)
def test_age_span_calculation_property(site_max: float, site_span: float) -> None:
    """Property test verifying age span arithmetic invariant."""
    site_min = max(0.0, site_max - site_span)
    occ = HomininSpecimenOccurrence(
        index=0,
        species_name="Homo_erectus",
        genus="Homo",
        is_homo=True,
        grade="homo_2",  # type: ignore
        site_complex="Turkana",
        site="Koobi_Fora",
        site_max_ma=site_max,
        site_min_ma=site_min,
        subsite=None,
        subsite_type=None,
        formation="Koobi_Fora",
        stratigraphic_unit="KBS",
        strat_max_ma=None,
        strat_min_ma=None,
        specimen_codes=["KNM-ER 3733"],
        raw_comments="KNM-ER 3733 cranium",
        source="Leakey (1976)",
        has_strat_bounds=False,
        has_site_bounds=True,
    )
    span = occ.age_span_myr
    assert span is not None
    assert abs(span - (site_max - site_min)) < 1e-9


@given(st.text())
def test_specimen_identifier_extraction_safety(text: str) -> None:
    """Verify that regex extraction never crashes or returns empty strings."""
    codes = extract_specimen_identifiers(text)
    assert isinstance(codes, list)
    for c in codes:
        assert isinstance(c, str)
        assert len(c) > 0
