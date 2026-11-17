"""Stratigraphic distribution and faunal continuity of Darwin's (1851) Fossil Lepadidae.

This module provides standard analytical tools to evaluate the stratigraphic ranges,
stage-level richness, and boundary-crossing persistence of fossil pedunculated barnacles
cataloged in Charles Darwin's 1851 Palaeontographical Society monograph.

Mathematical & Methodological Background:
-----------------------------------------
Darwin's 1851 monograph established the first systematic range chart for fossil Cirripedia,
tracking 35 distinct species across 10 chronostratigraphic stages from the Lower Oolite (Jurassic)
to the Tertiary.

1. Stage Richness Census:
   Let S be the set of species and H = {h_1, h_2, ..., h_m} be the ordered sequence of geological
   stages. The empirical richness R(h_j) of stage h_j is the count of verified occurrences:
       R(h_j) = sum_{i=1}^n I(s_i in h_j)
   where I is the indicator function of presence.

2. Boundary Persistence (Faunal Overlap):
   For adjacent stages (h_j, h_{j+1}), the boundary persistence count P(h_j, h_{j+1}) is:
       P(h_j, h_{j+1}) = sum_{i=1}^n I(s_i in h_j and s_i in h_{j+1})
   High overlap indicates continuous deposition and lineage persistence across stage boundaries;
   zero overlap indicates complete faunal turnover or taphonomic hiatus.

3. Generic Longevity Ratio:
   The temporal span of a genus G is measured across stages:
       Span(G) = max(index(h)) - min(index(h)) for h such that exists s in G present in h.
   A genus exhibiting high stage span despite zero species-level persistence across eras
   demonstrates morphological stability under continuous species turnover.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

GEOLOGICAL_STAGES: tuple[tuple[str, str], ...] = (
    ("lower_oolite", "Lower Oolite (Stonesfield)"),
    ("middle_oolite", "Middle Oolite (Oxford Clay)"),
    ("lower_greensand", "Lower Greensand"),
    ("gault", "Gault"),
    ("upper_greensand", "Upper Greensand"),
    ("chalk_marl", "Chalk Marl"),
    ("lower_chalk", "Lower Chalk"),
    ("upper_chalk", "Upper Chalk"),
    ("maestricht_faxoe_scania", "Maestricht Formation (Faxoe/Scania)"),
    ("tertiary", "Tertiary"),
)


@dataclass(frozen=True)
class FossilBarnacleOccurrence:
    """A verified fossil barnacle occurrence record across geological stages."""

    species_name: str
    genus: str
    stage_presences: dict[str, bool]

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> FossilBarnacleOccurrence:
        """Parse a row from the transcribed 1851 stratigraphic CSV."""
        presences = {
            stage_key: row[stage_key].strip() in {"*", "*?"}
            for stage_key, _ in GEOLOGICAL_STAGES
        }
        return cls(
            species_name=row["species_name"].strip(),
            genus=row["genus"].strip(),
            stage_presences=presences,
        )


def load_stratigraphic_occurrences(csv_path: Path) -> list[FossilBarnacleOccurrence]:
    """Load Darwin's 1851 stratigraphic table from CSV into structured occurrence records.

    Parameters
    ----------
    csv_path : Path
        Path to the transcribed CSV file (darwin_1851_fossil_lepadidae_stratigraphy.csv).

    Returns
    -------
    list[FossilBarnacleOccurrence]
        Parsed occurrence records for all cataloged species.
    """
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [FossilBarnacleOccurrence.from_csv_row(row) for row in reader]


@dataclass(frozen=True)
class StageSummary:
    """Summary statistics for a single chronostratigraphic stage."""

    stage_key: str
    stage_name: str
    richness: int
    genera: tuple[str, ...]


def calculate_stage_richness(
    occurrences: Sequence[FossilBarnacleOccurrence],
) -> list[StageSummary]:
    """Compute empirical species richness and generic representation per geological stage.

    Parameters
    ----------
    occurrences : Sequence[FossilBarnacleOccurrence]
        Fossil occurrence dataset.

    Returns
    -------
    list[StageSummary]
        Chronologically ordered summary for each stage.
    """
    summaries: list[StageSummary] = []
    for stage_key, stage_name in GEOLOGICAL_STAGES:
        present = [
            occ for occ in occurrences if occ.stage_presences.get(stage_key, False)
        ]
        genera = tuple(sorted({occ.genus for occ in present}))
        summaries.append(
            StageSummary(
                stage_key=stage_key,
                stage_name=stage_name,
                richness=len(present),
                genera=genera,
            )
        )
    return summaries


@dataclass(frozen=True)
class BoundaryOverlap:
    """Faunal continuity statistics across adjacent geological stage boundaries."""

    earlier_stage_name: str
    later_stage_name: str
    shared_species: tuple[str, ...]
    shared_count: int


def calculate_boundary_overlaps(
    occurrences: Sequence[FossilBarnacleOccurrence],
) -> list[BoundaryOverlap]:
    """Calculate the number and identity of shared species between adjacent stages.

    Parameters
    ----------
    occurrences : Sequence[FossilBarnacleOccurrence]
        Fossil occurrence dataset.

    Returns
    -------
    list[BoundaryOverlap]
        Overlap metrics for all adjacent stage pairs (h_j, h_{j+1}).
    """
    overlaps: list[BoundaryOverlap] = []
    for i in range(len(GEOLOGICAL_STAGES) - 1):
        k1, name1 = GEOLOGICAL_STAGES[i]
        k2, name2 = GEOLOGICAL_STAGES[i + 1]

        shared = tuple(
            occ.species_name
            for occ in occurrences
            if occ.stage_presences.get(k1, False) and occ.stage_presences.get(k2, False)
        )
        overlaps.append(
            BoundaryOverlap(
                earlier_stage_name=name1,
                later_stage_name=name2,
                shared_species=shared,
                shared_count=len(shared),
            )
        )
    return overlaps


@dataclass(frozen=True)
class GenusStratigraphicRange:
    """Stratigraphic range and longevity metrics for a genus."""

    genus: str
    species_count: int
    first_appearance_stage: str
    last_appearance_stage: str
    stage_span_count: int


def calculate_genus_ranges(
    occurrences: Sequence[FossilBarnacleOccurrence],
) -> list[GenusStratigraphicRange]:
    """Compute the total species count and stage range for each genus.

    Parameters
    ----------
    occurrences : Sequence[FossilBarnacleOccurrence]
        Fossil occurrence dataset.

    Returns
    -------
    list[GenusStratigraphicRange]
        Range statistics for each observed genus.
    """
    genera = sorted({occ.genus for occ in occurrences})
    stage_keys = [k for k, _ in GEOLOGICAL_STAGES]
    stage_names = {k: name for k, name in GEOLOGICAL_STAGES}

    ranges: list[GenusStratigraphicRange] = []
    for g in genera:
        g_occs = [occ for occ in occurrences if occ.genus == g]
        indices_present = []
        for idx, k in enumerate(stage_keys):
            if any(occ.stage_presences.get(k, False) for occ in g_occs):
                indices_present.append(idx)

        first_stage = stage_names[stage_keys[indices_present[0]]]
        last_stage = stage_names[stage_keys[indices_present[-1]]]
        span = indices_present[-1] - indices_present[0] + 1

        ranges.append(
            GenusStratigraphicRange(
                genus=g,
                species_count=len(g_occs),
                first_appearance_stage=first_stage,
                last_appearance_stage=last_stage,
                stage_span_count=span,
            )
        )
    return ranges
