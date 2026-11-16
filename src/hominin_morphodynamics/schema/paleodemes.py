"""Paleodeme and regional basin projection layer for hominin fossil occurrences.

Maps specimen occurrences into Robert Foley's localized fossil populations (paleodemes)
sampled from specific geographic basins and time slices, decoupling regional demographic
signals from aggregate continental species bins.

Provides Layer 2 anomaly isolation and defect rectification for stratigraphic age bounds
while preserving Layer 0 / Layer 1 raw provenance immutable.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Sequence

from hominin_morphodynamics.schema.specimens import (
    EcologicalGrade,
    HomininSpecimenOccurrence,
)


class GeographicBasin(str, Enum):
    """Major sedimentary basins and biogeographic provinces."""

    TURKANA = "turkana_basin"  # Koobi Fora, West Turkana, Ileret
    AFAR_RIFT = "afar_rift"  # Hadar, Middle Awash, Gona, Dikika, Woranso-Mille
    OLDUVAI_LAETOLI = "olduvai_laetoli"  # Olduvai Gorge, Laetoli
    SOUTH_AFRICA_KARST = "south_africa_karst"  # Sterkfontein, Swartkrans, Kromdraai, Makapansgat
    CHAD_CENTRAL = "chad_central"  # Koro Toro, Bahr el Ghazal
    TRANS_CAUCASUS = "trans_caucasus"  # Dmanisi
    EAST_ASIA = "east_asia"  # Sangiran, Trinil, Zhoukoudian, Gongwangling
    WESTERN_EURASIA = "western_eurasia"  # Atapuerca, Mauer, Neander Valley, Levantine caves
    ISLAND_SOUTHEAST_ASIA = "island_southeast_asia"  # Flores (Liang Bua)
    OTHER = "other"


BASIN_MAPPINGS: dict[str, GeographicBasin] = {
    "Turkana": GeographicBasin.TURKANA,
    "East Turkana": GeographicBasin.TURKANA,
    "West Turkana": GeographicBasin.TURKANA,
    "Koobi Fora": GeographicBasin.TURKANA,
    "Ileret": GeographicBasin.TURKANA,
    "Hadar": GeographicBasin.AFAR_RIFT,
    "Middle Awash": GeographicBasin.AFAR_RIFT,
    "Gona": GeographicBasin.AFAR_RIFT,
    "Dikika": GeographicBasin.AFAR_RIFT,
    "Woranso-Mille": GeographicBasin.AFAR_RIFT,
    "Afar": GeographicBasin.AFAR_RIFT,
    "Laetoli": GeographicBasin.OLDUVAI_LAETOLI,
    "Olduvai": GeographicBasin.OLDUVAI_LAETOLI,
    "SA": GeographicBasin.SOUTH_AFRICA_KARST,
    "Sterkfontein": GeographicBasin.SOUTH_AFRICA_KARST,
    "Swartkrans": GeographicBasin.SOUTH_AFRICA_KARST,
    "Kromdraai": GeographicBasin.SOUTH_AFRICA_KARST,
    "Makapansgat": GeographicBasin.SOUTH_AFRICA_KARST,
    "Gladysvale": GeographicBasin.SOUTH_AFRICA_KARST,
    "Malapa": GeographicBasin.SOUTH_AFRICA_KARST,
    "Chad": GeographicBasin.CHAD_CENTRAL,
    "Bahr el Ghazal": GeographicBasin.CHAD_CENTRAL,
    "Koro Toro": GeographicBasin.CHAD_CENTRAL,
    "Dmanisi": GeographicBasin.TRANS_CAUCASUS,
    "Sangiran": GeographicBasin.EAST_ASIA,
    "Trinil": GeographicBasin.EAST_ASIA,
    "Java": GeographicBasin.EAST_ASIA,
    "Zhoukoudian": GeographicBasin.EAST_ASIA,
    "Flores": GeographicBasin.ISLAND_SOUTHEAST_ASIA,
    "Liang Bua": GeographicBasin.ISLAND_SOUTHEAST_ASIA,
    "Atapuerca": GeographicBasin.WESTERN_EURASIA,
    "Gran Dolina": GeographicBasin.WESTERN_EURASIA,
    "Sima de los Huesos": GeographicBasin.WESTERN_EURASIA,
}


def resolve_basin(site_complex: str | None, site: str | None) -> GeographicBasin:
    """Resolve occurrence to biogeographic depositional basin."""
    if site_complex and site_complex in BASIN_MAPPINGS:
        return BASIN_MAPPINGS[site_complex]
    if site and site in BASIN_MAPPINGS:
        return BASIN_MAPPINGS[site]
    return GeographicBasin.OTHER


@dataclass(frozen=True)
class PaleodemeCluster:
    """Foley paleodeme: a geographically and chronologically localized fossil population."""

    basin: GeographicBasin
    grade: EcologicalGrade
    time_slice_ma: tuple[float, float]  # (max_age, min_age)
    occurrence_indices: list[int]
    specimen_codes: list[str]
    distinct_taxa: list[str]

    @property
    def sample_size(self) -> int:
        return len(self.occurrence_indices)


# Primary literature corrections for the 5 inverted stratigraphic records identified in Finding 001
# Format: index -> (rectified_site_max, rectified_site_min, rectified_strat_max, rectified_strat_min, note)
RECTIFIED_INVERSIONS: dict[int, tuple[float | None, float | None, float | None, float | None, str]] = {
    31: (
        3.60,
        3.58,
        3.60,
        3.58,
        "A. anamensis Korsi Dora: transposed min/max in raw entry; rectified to 3.60-3.58 Ma",
    ),
    35: (
        None,
        None,
        3.60,
        3.58,
        "A. anamensis Korsi Dora: transposed strat min/max in raw entry; rectified to 3.60-3.58 Ma",
    ),
    264: (
        0.710,
        0.191,
        None,
        None,
        "H. neanderthalensis Madonna dell'Arma: transposed site bounds; rectified to 0.710-0.191 Ma (MIS 7-9)",
    ),
    269: (
        0.071,
        0.040,
        None,
        None,
        "H. neanderthalensis La Chapelle-aux-Saints: transposed site bounds; rectified to 0.071-0.040 Ma (MIS 3-4)",
    ),
    322: (
        0.220,
        0.039,
        None,
        None,
        "H. sapiens Tabon: transposed site bounds; rectified to 0.220-0.039 Ma (Tabon sequence)",
    ),
}


@dataclass(frozen=True)
class RectifiedOccurrence:
    """Layer 2 projection of a specimen occurrence with validated stratigraphic invariants.

    Preserves raw Layer 0/1 provenance attributes while guaranteeing:
    - site_max_ma >= site_min_ma >= 0.0 (if present)
    - strat_max_ma >= strat_min_ma >= 0.0 (if present)
    - explicit tracking of whether and why the record was rectified.
    """

    raw_occurrence: HomininSpecimenOccurrence
    site_max_ma: float | None
    site_min_ma: float | None
    strat_max_ma: float | None
    strat_min_ma: float | None
    is_rectified: bool
    rectification_note: str | None

    @property
    def index(self) -> int:
        return self.raw_occurrence.index

    @property
    def species_name(self) -> str:
        return self.raw_occurrence.species_name

    @property
    def grade(self) -> EcologicalGrade:
        return self.raw_occurrence.grade

    @property
    def specimen_codes(self) -> list[str]:
        return self.raw_occurrence.specimen_codes

    @property
    def site_complex(self) -> str | None:
        return self.raw_occurrence.site_complex

    @property
    def site(self) -> str | None:
        return self.raw_occurrence.site

    @property
    def effective_max_ma(self) -> float | None:
        """Preferred bed-level max date, falling back to site max date."""
        return self.strat_max_ma if self.strat_max_ma is not None else self.site_max_ma

    @property
    def effective_min_ma(self) -> float | None:
        """Preferred bed-level min date, falling back to site min date."""
        return self.strat_min_ma if self.strat_min_ma is not None else self.site_min_ma


def rectify_occurrence(occ: HomininSpecimenOccurrence) -> RectifiedOccurrence:
    """Rectify stratigraphic age inversions while preserving raw occurrence provenance."""
    idx = occ.index
    if idx in RECTIFIED_INVERSIONS:
        r_smax, r_smin, r_stmax, r_stmin, note = RECTIFIED_INVERSIONS[idx]
        site_max = r_smax if r_smax is not None else occ.site_max_ma
        site_min = r_smin if r_smin is not None else occ.site_min_ma
        strat_max = r_stmax if r_stmax is not None else occ.strat_max_ma
        strat_min = r_stmin if r_stmin is not None else occ.strat_min_ma
        return RectifiedOccurrence(
            raw_occurrence=occ,
            site_max_ma=site_max,
            site_min_ma=site_min,
            strat_max_ma=strat_max,
            strat_min_ma=strat_min,
            is_rectified=True,
            rectification_note=note,
        )

    return RectifiedOccurrence(
        raw_occurrence=occ,
        site_max_ma=occ.site_max_ma,
        site_min_ma=occ.site_min_ma,
        strat_max_ma=occ.strat_max_ma,
        strat_min_ma=occ.strat_min_ma,
        is_rectified=False,
        rectification_note=None,
    )


def rectify_all_occurrences(
    occurrences: Sequence[HomininSpecimenOccurrence],
) -> list[RectifiedOccurrence]:
    """Map a sequence of raw occurrences into verified, rectified Layer 2 occurrences."""
    rectified = [rectify_occurrence(occ) for occ in occurrences]
    # Enforce stratigraphic invariant post-condition
    for r in rectified:
        if r.site_max_ma is not None and r.site_min_ma is not None:
            if r.site_max_ma < r.site_min_ma:
                raise ValueError(
                    f"Invariant violation in rectified occurrence {r.index}: "
                    f"site_max ({r.site_max_ma}) < site_min ({r.site_min_ma})"
                )
        if r.strat_max_ma is not None and r.strat_min_ma is not None:
            if r.strat_max_ma < r.strat_min_ma:
                raise ValueError(
                    f"Invariant violation in rectified occurrence {r.index}: "
                    f"strat_max ({r.strat_max_ma}) < strat_min ({r.strat_min_ma})"
                )
    return rectified


def project_paleodemes(
    occurrences: Sequence[HomininSpecimenOccurrence | RectifiedOccurrence],
    time_window_myr: float = 0.5,
) -> list[PaleodemeCluster]:
    """Group specimen occurrences into spatio-temporal paleodemes."""
    # Bin by basin, grade, and discrete time slice
    buckets: dict[tuple[GeographicBasin, EcologicalGrade, int], list[HomininSpecimenOccurrence | RectifiedOccurrence]] = {}

    for occ in occurrences:
        site_complex = occ.site_complex
        site = occ.site
        basin = resolve_basin(site_complex, site)
        
        if isinstance(occ, RectifiedOccurrence):
            age = occ.effective_max_ma
        else:
            age = occ.strat_max_ma if occ.strat_max_ma is not None else occ.site_max_ma

        if age is None:
            continue
        # Time slice index
        t_bin = int(age / time_window_myr)
        key = (basin, occ.grade, t_bin)
        buckets.setdefault(key, []).append(occ)

    clusters: list[PaleodemeCluster] = []
    for (basin, grade, t_bin), occs in buckets.items():
        max_t = (t_bin + 1) * time_window_myr
        min_t = t_bin * time_window_myr
        indices = [o.index for o in occs]
        specimens: list[str] = []
        for o in occs:
            specimens.extend(o.specimen_codes)
        taxa = sorted(list(set(o.species_name for o in occs)))

        clusters.append(
            PaleodemeCluster(
                basin=basin,
                grade=grade,
                time_slice_ma=(max_t, min_t),
                occurrence_indices=indices,
                specimen_codes=sorted(list(set(specimens))),
                distinct_taxa=taxa,
            )
        )

    return sorted(clusters, key=lambda c: (c.time_slice_ma[0], c.basin.value), reverse=True)
