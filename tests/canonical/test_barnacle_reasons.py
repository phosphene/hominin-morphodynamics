"""Verification of Darwin's (1851) Cirripede Stratigraphic Units of Reason."""

from __future__ import annotations

from pathlib import Path
import pytest

from hominin_morphodynamics.canonical.barnacle_reasons import (
    assess_boundary_overlap,
    evaluate_generic_architecture_stability,
    evaluate_stage_richness,
    load_darwin_1851_stratigraphic_ledger,
)

CSV_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "raw"
    / "darwin_cirripedia_1851_1854"
    / "darwin_1851_fossil_lepadidae_stratigraphy.csv"
)


def test_unit_of_reason_1_ledger_receptivity():
    """Verify Reason 1: The empirical ledger is ingested without data loss or mutation."""
    assert CSV_PATH.exists(), f"Stratigraphic ledger missing at {CSV_PATH}"
    records = load_darwin_1851_stratigraphic_ledger(CSV_PATH)

    # Darwin cataloged exactly 35 fossil species in his master table
    assert len(records) == 35

    # Three canonical genera represented
    genera = {r.genus for r in records}
    assert genera == {"Scalpellum", "Pollicipes", "Loricula"}


def test_unit_of_reason_2_cretaceous_peak_and_oolitic_scarcity():
    """Verify Reason 2: The empirical peak in the Upper Cretaceous vs Jurassic scarcity."""
    records = load_darwin_1851_stratigraphic_ledger(CSV_PATH)
    richness = evaluate_stage_richness(records)

    stage_map = {s.stage_name: s.verified_species_count for s in richness}

    # Jurassic Oolite is extremely sparse (1 in Lower, 2 in Middle)
    assert stage_map["Lower Oolite (Stonesfield)"] == 1
    assert stage_map["Middle Oolite (Oxford Clay)"] == 2

    # Cretaceous Chalk represents the culminant peak (11 in Upper Chalk, 11 in Maestricht)
    assert stage_map["Upper Chalk"] == 11
    assert stage_map["Maestricht Formation (Faxoe/Scania)"] == 11

    # Total richness in Chalk stages dwarfs Oolite by an order of magnitude
    chalk_total = (
        stage_map["Chalk Marl"]
        + stage_map["Lower Chalk"]
        + stage_map["Upper Chalk"]
        + stage_map["Maestricht Formation (Faxoe/Scania)"]
    )
    assert chalk_total >= 30


def test_unit_of_reason_3_boundary_crossing_and_continuity():
    """Verify Reason 3: Boundary overlap proves biological continuity across chalk horizons."""
    records = load_darwin_1851_stratigraphic_ledger(CSV_PATH)
    overlap = assess_boundary_overlap(records)

    # In the deep Chalk sequence, species persistence is explicitly detected
    upper_chalk_to_maestricht = next(
        o for o in overlap if "Upper Chalk" in o.earlier_stage and "Maestricht" in o.later_stage
    )
    assert upper_chalk_to_maestricht.overlap_count == 6
    assert "Scalpellum maximum" in upper_chalk_to_maestricht.shared_species
    assert "Pollicipes glaber" in upper_chalk_to_maestricht.shared_species

    # Lower Chalk to Upper Chalk also shows continuity
    lower_to_upper = next(
        o for o in overlap if "Lower Chalk" in o.earlier_stage and "Upper Chalk" in o.later_stage
    )
    assert lower_to_upper.overlap_count == 4

    # Major geological disconformities (e.g. Maestricht to Tertiary) show zero species persistence
    maestricht_to_tertiary = next(
        o for o in overlap if "Maestricht" in o.earlier_stage and "Tertiary" in o.later_stage
    )
    assert maestricht_to_tertiary.overlap_count == 0


def test_unit_of_reason_4_generic_stability_across_eras():
    """Verify Reason 4: Genera persist across eras despite complete species turnover."""
    records = load_darwin_1851_stratigraphic_ledger(CSV_PATH)
    stability = evaluate_generic_architecture_stability(records)

    # Pollicipes spans from Lower Oolite (Jurassic) to Upper Chalk / Maestricht
    pollicipes = next(s for s in stability if s.genus == "Pollicipes")
    assert "Lower Oolite" in pollicipes.earliest_stage_detected
    assert pollicipes.total_fossil_species >= 20

    # Scalpellum spans from Lower Greensand through Cretaceous into Tertiary
    scalpellum = next(s for s in stability if s.genus == "Scalpellum")
    assert "Lower Greensand" in scalpellum.earliest_stage_detected
    assert "Tertiary" in scalpellum.latest_stage_detected
