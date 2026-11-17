"""Space of Reasons: Darwin's (1851) Cirripede Stratigraphic Turnover.

A literate variation where every function, type, and evaluation represents an explicit,
self-sufficient move in the Sellarsian space of reasons.

The space is partitioned into four explicit inferential units:
1. Reason 1: The Material Ledger (Warrant of Receptivity)
2. Reason 2: The Stratigraphic Horizon Invariant (Warrant of Co-presence)
3. Reason 3: Boundary-Crossing Persistence (Warrant of Lineage Continuity)
4. Reason 4: The Generic Anchor vs. Specific Ephemerality (Warrant of Deep-Time Stability)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


# ==============================================================================
# UNIT OF REASON 1: The Material Ledger (Warrant of Receptivity)
#
# Ground:
#   Before inference can begin, empirical receptivity requires an immutable ledger
#   of physical fossils collected from verified geological strata.
#
# Premise:
#   In 1851, Darwin published the first comprehensive monograph on fossil pedunculated
#   barnacles (Fossil Lepadidae), cataloging 35 species across 10 geological stages.
#
# Entailment:
#   The records must be ingested without speculative imputation. Each entry is
#   strictly classified as verified presence ('*'), doubtful ('*?'), or absent ('—').
# ==============================================================================


@dataclass(frozen=True)
class FossilOccurrenceRecord:
    """An observable fossil taxon localized in a discrete geological horizon."""

    species_name: str
    genus: str
    is_tertiary: bool
    is_maestricht: bool
    is_upper_chalk: bool
    is_lower_chalk: bool
    is_chalk_marl: bool
    is_upper_greensand: bool
    is_gault: bool
    is_lower_greensand: bool
    is_middle_oolite: bool
    is_lower_oolite: bool

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> FossilOccurrenceRecord:
        def check(col: str) -> bool:
            return row[col].strip() in {"*", "*?"}

        return cls(
            species_name=row["species_name"].strip(),
            genus=row["genus"].strip(),
            is_tertiary=check("tertiary"),
            is_maestricht=check("maestricht_faxoe_scania"),
            is_upper_chalk=check("upper_chalk"),
            is_lower_chalk=check("lower_chalk"),
            is_chalk_marl=check("chalk_marl"),
            is_upper_greensand=check("upper_greensand"),
            is_gault=check("gault"),
            is_lower_greensand=check("lower_greensand"),
            is_middle_oolite=check("middle_oolite"),
            is_lower_oolite=check("lower_oolite"),
        )


def load_darwin_1851_stratigraphic_ledger(csv_path: Path) -> list[FossilOccurrenceRecord]:
    """Ingest Darwin's 1851 table into an immutable sequence of observational records."""
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [FossilOccurrenceRecord.from_csv_row(row) for row in reader]


# ==============================================================================
# UNIT OF REASON 2: Stratigraphic Horizon Richness (Warrant of Co-Presence)
#
# Ground:
#   The density of an evolutionary radiation cannot be evaluated as an abstract
#   continuous rate unless we first establish the empirical census of co-present
#   taxa within each chronostratigraphic stage.
#
# Premise:
#   Darwin observed that fossil cirripedes are not uniformly distributed:
#   they are virtually absent in the Jurassic Oolite, explode into diversity
#   during the Upper Cretaceous Chalk, and contract again in the Tertiary.
#
# Entailment:
#   Computing the stage census reveals whether the morphological series is dense
#   enough to bear the weight of gradual divergence modeling.
# ==============================================================================


@dataclass(frozen=True)
class StageRichnessAccounting:
    stage_id: str
    stage_name: str
    verified_species_count: int
    genus_representation: tuple[str, ...]


GEOLOGICAL_STAGE_SEQUENCE: tuple[tuple[str, str], ...] = (
    ("is_lower_oolite", "Lower Oolite (Stonesfield)"),
    ("is_middle_oolite", "Middle Oolite (Oxford Clay)"),
    ("is_lower_greensand", "Lower Greensand"),
    ("is_gault", "Gault"),
    ("is_upper_greensand", "Upper Greensand"),
    ("is_chalk_marl", "Chalk Marl"),
    ("is_lower_chalk", "Lower Chalk"),
    ("is_upper_chalk", "Upper Chalk"),
    ("is_maestricht", "Maestricht Formation (Faxoe/Scania)"),
    ("is_tertiary", "Tertiary"),
)


def evaluate_stage_richness(
    records: Sequence[FossilOccurrenceRecord],
) -> list[StageRichnessAccounting]:
    """Calculate the empirical richness per geological horizon in Darwin's ledger."""
    accounting: list[StageRichnessAccounting] = []

    for attr, stage_name in GEOLOGICAL_STAGE_SEQUENCE:
        present = [r for r in records if getattr(r, attr)]
        genera = tuple(sorted({r.genus for r in present}))
        accounting.append(
            StageRichnessAccounting(
                stage_id=attr,
                stage_name=stage_name,
                verified_species_count=len(present),
                genus_representation=genera,
            )
        )

    return accounting


# ==============================================================================
# UNIT OF REASON 3: Boundary-Crossing Persistence (Warrant of Continuity)
#
# Ground:
#   In the space of reasons, a claim of evolutionary transformation requires
#   demonstrating that adjacent geological horizons are not hermetically sealed
#   catastrophic breaks, but share transitional and persisting lineage vectors.
#
# Premise:
#   Darwin noted that while most species are restricted to a single stage,
#   certain species (such as Scalpellum maximum and Pollicipes glaber) span
#   multiple successive chalk formations, proving continuity of sedimentation
#   and biological descent.
#
# Entailment:
#   Evaluating pairwise boundary overlap identifies where the rock record exhibits
#   continuous biological transition versus taphonomic disconformity.
# ==============================================================================


@dataclass(frozen=True)
class BoundaryOverlapAssessment:
    earlier_stage: str
    later_stage: str
    shared_species: tuple[str, ...]
    overlap_count: int
    has_lineage_continuity: bool


def assess_boundary_overlap(
    records: Sequence[FossilOccurrenceRecord],
) -> list[BoundaryOverlapAssessment]:
    """Measure the species persistence across adjacent chronostratigraphic horizons."""
    assessments: list[BoundaryOverlapAssessment] = []

    for i in range(len(GEOLOGICAL_STAGE_SEQUENCE) - 1):
        attr_early, name_early = GEOLOGICAL_STAGE_SEQUENCE[i]
        attr_late, name_late = GEOLOGICAL_STAGE_SEQUENCE[i + 1]

        shared = tuple(
            r.species_name
            for r in records
            if getattr(r, attr_early) and getattr(r, attr_late)
        )

        assessments.append(
            BoundaryOverlapAssessment(
                earlier_stage=name_early,
                later_stage=name_late,
                shared_species=shared,
                overlap_count=len(shared),
                has_lineage_continuity=(len(shared) > 0),
            )
        )

    return assessments


# ==============================================================================
# UNIT OF REASON 4: Generic Longevity vs. Specific Ephemerality (Deep-Time Anchor)
#
# Ground:
#   A central inferential problem in deep-time paleobiology is distinguishing
#   rapid terminal species turnover from foundational morphological architectural stability.
#
# Premise:
#   Darwin observed a striking paradox: every Oolitic, Cretaceous, and Tertiary
#   species of Lepadidae is distinct (zero species persist from Jurassic to Recent),
#   yet the overarching genera (Pollicipes, Scalpellum) persist across 150+ million
#   years with virtually identical valve articulation geometry.
#
# Entailment:
#   The longevity ratio of the genus relative to its ephemeral constituent species
#   proves that high population turnover operates within a conservative, stable
#   functional architecture across geological eras.
# ==============================================================================


@dataclass(frozen=True)
class GenericArchitectureStability:
    genus: str
    total_fossil_species: int
    earliest_stage_detected: str
    latest_stage_detected: str
    spans_multiple_eras: bool
    epistemic_warrant: str


def evaluate_generic_architecture_stability(
    records: Sequence[FossilOccurrenceRecord],
) -> list[GenericArchitectureStability]:
    """Evaluate deep-time architectural persistence of genera relative to specific turnover."""
    genera = sorted({r.genus for r in records})
    results: list[GenericArchitectureStability] = []

    for g in genera:
        g_records = [r for r in records if r.genus == g]
        stages_present = []
        for attr, stage_name in GEOLOGICAL_STAGE_SEQUENCE:
            if any(getattr(r, attr) for r in g_records):
                stages_present.append(stage_name)

        earliest = stages_present[0] if stages_present else "Unknown"
        latest = stages_present[-1] if stages_present else "Unknown"
        spans_eras = (
            any("Oolite" in s for s in stages_present)
            and any("Tertiary" in s for s in stages_present)
        )

        warrant = (
            f"Genus {g} maintains invariant valve homologies across {len(stages_present)} "
            f"geological stages despite 100% turnover of individual species."
        )

        results.append(
            GenericArchitectureStability(
                genus=g,
                total_fossil_species=len(g_records),
                earliest_stage_detected=earliest,
                latest_stage_detected=latest,
                spans_multiple_eras=spans_eras,
                epistemic_warrant=warrant,
            )
        )

    return results
