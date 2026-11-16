"""Paleodeme and regional basin projection layer for hominin fossil occurrences.

Maps specimen occurrences into Robert Foley's localized fossil populations (paleodemes)
sampled from specific geographic basins and time slices, decoupling regional demographic
signals from aggregate continental species bins.
"""

from __future__ import annotations

from dataclasses import dataclass
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


def project_paleodemes(
    occurrences: Sequence[HomininSpecimenOccurrence],
    time_window_myr: float = 0.5,
) -> list[PaleodemeCluster]:
    """Group specimen occurrences into spatio-temporal paleodemes."""
    # Bin by basin, grade, and discrete time slice
    buckets: dict[tuple[GeographicBasin, EcologicalGrade, int], list[HomininSpecimenOccurrence]] = {}

    for occ in occurrences:
        basin = resolve_basin(occ.site_complex, occ.site)
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
