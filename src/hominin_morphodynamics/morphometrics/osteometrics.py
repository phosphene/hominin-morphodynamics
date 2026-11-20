"""Caliper-and-dirt hominin craniodental osteometric records (Tier 3/4).

Satisfies the J.O. Wisdom Caliper and Dirt Test (MATHEMATICAL_LEGIBILITY_AND_SELF_SUFFICIENT_UNITS_OF_REASON.md):
every trait is a directly measurable physical osteometric observable with explicit SI/mm/cc/kg
units, measurement uncertainty (CV), and taphonomic fragility factor — decoupling continuous
morphological variance from arbitrary Linnaean species-count binning.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from hominin_morphodynamics.schema.paleodemes import GeographicBasin
from hominin_morphodynamics.schema.specimens import EcologicalGrade


@dataclass(frozen=True)
class CraniodentalSpecimen:
    """Strongly-typed hominin osteometric specimen record with explicit physical units.

    Dimensions:
        age_ma: [Myr] Radiometric/stratigraphic midpoint age before present (>= 0).
        endocranial_volume_cc: [cm^3] Endocranial capacity (> 0).
        molar_m1_area_mm2: [mm^2] Lower/upper first molar crown area (MD * BL, > 0).
        bicondylar_breadth_mm: [mm] Mandibular/cranial bicondylar breadth (> 0).
        estimated_body_mass_kg: [kg] Postcranial/orbital body mass estimate (> 0).
        measurement_error_cv: [dimensionless] Relative measurement uncertainty CV (> 0).
        taphonomic_fragility: [dimensionless] Taphonomic distortion/fragmentation penalty (>= 1.0).
    """

    specimen_id: str
    taxon: str
    basin: GeographicBasin
    grade: EcologicalGrade
    age_ma: float
    endocranial_volume_cc: float
    molar_m1_area_mm2: float
    bicondylar_breadth_mm: float
    estimated_body_mass_kg: float
    measurement_error_cv: float
    taphonomic_fragility: float
    source_citation: str

    def __post_init__(self) -> None:
        if not math.isfinite(self.age_ma) or self.age_ma < 0.0:
            raise ValueError(f"{self.specimen_id}: age_ma must be finite and >= 0, got {self.age_ma}")
        for field_name in (
            "endocranial_volume_cc",
            "molar_m1_area_mm2",
            "bicondylar_breadth_mm",
            "estimated_body_mass_kg",
            "measurement_error_cv",
        ):
            val = getattr(self, field_name)
            if not math.isfinite(val) or val <= 0.0:
                raise ValueError(f"{self.specimen_id}: {field_name} must be finite and > 0, got {val}")
        if not math.isfinite(self.taphonomic_fragility) or self.taphonomic_fragility < 1.0:
            raise ValueError(
                f"{self.specimen_id}: taphonomic_fragility must be finite and >= 1.0, got {self.taphonomic_fragility}"
            )

    @property
    def trait_vector(self) -> tuple[float, float, float]:
        """Ordered continuous craniodental trait vector (ECV [cc], M1 area [mm^2], BCB [mm])."""
        return (
            self.endocranial_volume_cc,
            self.molar_m1_area_mm2,
            self.bicondylar_breadth_mm,
        )


# Curated published benchmark osteometric specimens across Plio-Pleistocene basins & Foley grades
CANONICAL_HOMININ_OSTEOMETRICS: tuple[CraniodentalSpecimen, ...] = (
    CraniodentalSpecimen(
        specimen_id="AL 288-1",
        taxon="Australopithecus_afarensis",
        basin=GeographicBasin.AFAR_RIFT,
        grade=EcologicalGrade.AUSTRALOPITHECINE,
        age_ma=3.18,
        endocranial_volume_cc=400.0,
        molar_m1_area_mm2=142.0,
        bicondylar_breadth_mm=102.0,
        estimated_body_mass_kg=29.0,
        measurement_error_cv=0.04,
        taphonomic_fragility=1.2,
        source_citation="Johanson et al. (1982); Holloway et al. (2004)",
    ),
    CraniodentalSpecimen(
        specimen_id="AL 444-2",
        taxon="Australopithecus_afarensis",
        basin=GeographicBasin.AFAR_RIFT,
        grade=EcologicalGrade.AUSTRALOPITHECINE,
        age_ma=3.00,
        endocranial_volume_cc=550.0,
        molar_m1_area_mm2=168.0,
        bicondylar_breadth_mm=118.0,
        estimated_body_mass_kg=45.0,
        measurement_error_cv=0.03,
        taphonomic_fragility=1.1,
        source_citation="Kimbel et al. (2004)",
    ),
    CraniodentalSpecimen(
        specimen_id="Sts 5",
        taxon="Australopithecus_africanus",
        basin=GeographicBasin.SOUTH_AFRICA_KARST,
        grade=EcologicalGrade.AUSTRALOPITHECINE,
        age_ma=2.50,
        endocranial_volume_cc=485.0,
        molar_m1_area_mm2=175.0,
        bicondylar_breadth_mm=108.0,
        estimated_body_mass_kg=35.0,
        measurement_error_cv=0.03,
        taphonomic_fragility=1.0,
        source_citation="Broom & Robinson (1950); Holloway et al. (2004)",
    ),
    CraniodentalSpecimen(
        specimen_id="OH 5",
        taxon="Paranthropus_boisei",
        basin=GeographicBasin.OLDUVAI_LAETOLI,
        grade=EcologicalGrade.PARANTHROPUS,
        age_ma=1.75,
        endocranial_volume_cc=530.0,
        molar_m1_area_mm2=258.0,
        bicondylar_breadth_mm=134.0,
        estimated_body_mass_kg=49.0,
        measurement_error_cv=0.02,
        taphonomic_fragility=1.0,
        source_citation="Tobias (1967); Wood (1991)",
    ),
    CraniodentalSpecimen(
        specimen_id="KNM-ER 406",
        taxon="Paranthropus_boisei",
        basin=GeographicBasin.TURKANA,
        grade=EcologicalGrade.PARANTHROPUS,
        age_ma=1.70,
        endocranial_volume_cc=510.0,
        molar_m1_area_mm2=245.0,
        bicondylar_breadth_mm=132.0,
        estimated_body_mass_kg=48.0,
        measurement_error_cv=0.03,
        taphonomic_fragility=1.1,
        source_citation="Wood (1991) Koobi Fora Research Project Vol. 4",
    ),
    CraniodentalSpecimen(
        specimen_id="KNM-ER 1813",
        taxon="Homo_habilis",
        basin=GeographicBasin.TURKANA,
        grade=EcologicalGrade.HOMO_1,
        age_ma=1.90,
        endocranial_volume_cc=510.0,
        molar_m1_area_mm2=150.0,
        bicondylar_breadth_mm=105.0,
        estimated_body_mass_kg=32.0,
        measurement_error_cv=0.03,
        taphonomic_fragility=1.0,
        source_citation="Wood (1991); Holloway et al. (2004)",
    ),
    CraniodentalSpecimen(
        specimen_id="OH 24",
        taxon="Homo_habilis",
        basin=GeographicBasin.OLDUVAI_LAETOLI,
        grade=EcologicalGrade.HOMO_1,
        age_ma=1.85,
        endocranial_volume_cc=590.0,
        molar_m1_area_mm2=156.0,
        bicondylar_breadth_mm=109.0,
        estimated_body_mass_kg=34.0,
        measurement_error_cv=0.06,
        taphonomic_fragility=2.0,
        source_citation="Tobias (1991) Olduvai Gorge Vol. 4",
    ),
    CraniodentalSpecimen(
        specimen_id="D2700",
        taxon="Homo_erectus",
        basin=GeographicBasin.TRANS_CAUCASUS,
        grade=EcologicalGrade.HOMO_2,
        age_ma=1.77,
        endocranial_volume_cc=600.0,
        molar_m1_area_mm2=152.0,
        bicondylar_breadth_mm=112.0,
        estimated_body_mass_kg=45.0,
        measurement_error_cv=0.02,
        taphonomic_fragility=1.0,
        source_citation="Vekua et al. (2002) Science 297:85–89",
    ),
    CraniodentalSpecimen(
        specimen_id="KNM-ER 3733",
        taxon="Homo_erectus",
        basin=GeographicBasin.TURKANA,
        grade=EcologicalGrade.HOMO_2,
        age_ma=1.63,
        endocranial_volume_cc=848.0,
        molar_m1_area_mm2=148.0,
        bicondylar_breadth_mm=121.0,
        estimated_body_mass_kg=56.0,
        measurement_error_cv=0.02,
        taphonomic_fragility=1.0,
        source_citation="Wood (1991); Holloway et al. (2004)",
    ),
    CraniodentalSpecimen(
        specimen_id="KNM-WT 15000",
        taxon="Homo_erectus",
        basin=GeographicBasin.TURKANA,
        grade=EcologicalGrade.HOMO_2,
        age_ma=1.53,
        endocranial_volume_cc=880.0,
        molar_m1_area_mm2=145.0,
        bicondylar_breadth_mm=124.0,
        estimated_body_mass_kg=62.0,
        measurement_error_cv=0.03,
        taphonomic_fragility=1.1,
        source_citation="Walker & Leakey (1993) The Nariokotome Homo erectus Skeleton",
    ),
    CraniodentalSpecimen(
        specimen_id="Kabwe 1",
        taxon="Homo_heidelbergensis",
        basin=GeographicBasin.OTHER,
        grade=EcologicalGrade.HOMO_3,
        age_ma=0.30,
        endocranial_volume_cc=1280.0,
        molar_m1_area_mm2=144.0,
        bicondylar_breadth_mm=128.0,
        estimated_body_mass_kg=68.0,
        measurement_error_cv=0.02,
        taphonomic_fragility=1.0,
        source_citation="Rightmire (1996); Grün et al. (2020) Nature",
    ),
    CraniodentalSpecimen(
        specimen_id="La Chapelle-aux-Saints 1",
        taxon="Homo_neanderthalensis",
        basin=GeographicBasin.WESTERN_EURASIA,
        grade=EcologicalGrade.HOMO_3,
        age_ma=0.055,
        endocranial_volume_cc=1625.0,
        molar_m1_area_mm2=135.0,
        bicondylar_breadth_mm=131.0,
        estimated_body_mass_kg=76.0,
        measurement_error_cv=0.02,
        taphonomic_fragility=1.0,
        source_citation="Boule (1911); Holloway et al. (2004)",
    ),
    CraniodentalSpecimen(
        specimen_id="Skhul V",
        taxon="Homo_sapiens",
        basin=GeographicBasin.WESTERN_EURASIA,
        grade=EcologicalGrade.HOMO_3,
        age_ma=0.11,
        endocranial_volume_cc=1518.0,
        molar_m1_area_mm2=122.0,
        bicondylar_breadth_mm=122.0,
        estimated_body_mass_kg=67.0,
        measurement_error_cv=0.02,
        taphonomic_fragility=1.0,
        source_citation="McCown & Keith (1939); Holloway et al. (2004)",
    ),
)

__all__ = [
    "CraniodentalSpecimen",
    "CANONICAL_HOMININ_OSTEOMETRICS",
]
