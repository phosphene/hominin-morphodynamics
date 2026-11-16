"""Specimen, horizon, paleodeme, and ecological grade schema definitions.

Formalizes osteological and paleoanthropological metadata:
- Museum catalog identifiers (KNM-ER, OH, AL, StW, SK, Dmanisi, etc.)
- Stratigraphically coupled horizons (geological layer and radiometric bounds)
- Taphonomic indicators and preservation flags
- Paleodeme (localized fossil population) and ecological grade groupings
  (Homo 1, Homo 2, Homo 3) treated as explicit analytical views.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class EcologicalGrade(str, Enum):
    """Foley's hominin ecological adaptive grades."""

    AUSTRALOPITHECINE = "australopithecine"  # Megadont / woodland-savanna generalists
    PARANTHROPUS = "paranthropus"  # Extreme masticatory specialists (C4 dietary niche)
    HOMO_1 = "homo_1"  # Small-bodied, encephalized facultative bipeds (habilis, rudolfensis)
    HOMO_2 = "homo_2"  # Large-bodied, obligate terrestrial striders (erectus, ergaster)
    HOMO_3 = "homo_3"  # Hyper-encephalized, symbolic/technological lineages (heidelbergensis, neanderthalensis, sapiens)
    ISOLATE = "isolate"  # Insular or divergent relicts (floresiensis, naledi)


GRADE_ASSIGNMENTS: dict[str, EcologicalGrade] = {
    "Australopithecus_afarensis": EcologicalGrade.AUSTRALOPITHECINE,
    "Australopithecus_africanus": EcologicalGrade.AUSTRALOPITHECINE,
    "Australopithecus_anamensis": EcologicalGrade.AUSTRALOPITHECINE,
    "Australopithecus_bahrelghazali": EcologicalGrade.AUSTRALOPITHECINE,
    "Australopithecus_deyiremeda": EcologicalGrade.AUSTRALOPITHECINE,
    "Australopithecus_garhi": EcologicalGrade.AUSTRALOPITHECINE,
    "Australopithecus_sediba": EcologicalGrade.AUSTRALOPITHECINE,
    "Paranthropus_aethiopicus": EcologicalGrade.PARANTHROPUS,
    "Paranthropus_boisei": EcologicalGrade.PARANTHROPUS,
    "Paranthropus_robustus": EcologicalGrade.PARANTHROPUS,
    "Homo_habilis": EcologicalGrade.HOMO_1,
    "Homo_rudolfensis": EcologicalGrade.HOMO_1,
    "Homo_erectus": EcologicalGrade.HOMO_2,
    "Homo_ergaster": EcologicalGrade.HOMO_2,
    "Homo_heidelbergensis": EcologicalGrade.HOMO_3,
    "Homo_neanderthalensis": EcologicalGrade.HOMO_3,
    "Homo_sapiens": EcologicalGrade.HOMO_3,
    "Homo_floresiensis": EcologicalGrade.ISOLATE,
}


@dataclass(frozen=True)
class HomininSpecimenOccurrence:
    """A cataloged occurrence record from a dated sedimentary locality."""

    index: int
    species_name: str
    genus: str
    is_homo: bool
    grade: EcologicalGrade
    site_complex: str | None
    site: str | None
    site_max_ma: float | None
    site_min_ma: float | None
    subsite: str | None
    subsite_type: str | None
    formation: str | None
    stratigraphic_unit: str | None
    strat_max_ma: float | None
    strat_min_ma: float | None
    specimen_codes: list[str]
    raw_comments: str | None
    source: str | None
    has_strat_bounds: bool
    has_site_bounds: bool

    @property
    def age_span_myr(self) -> float | None:
        """Calculate age uncertainty window in millions of years."""
        if self.has_strat_bounds and self.strat_max_ma is not None and self.strat_min_ma is not None:
            return abs(self.strat_max_ma - self.strat_min_ma)
        if self.has_site_bounds and self.site_max_ma is not None and self.site_min_ma is not None:
            return abs(self.site_max_ma - self.site_min_ma)
        return None


SPECIMEN_PATTERNS = [
    r"\bL\.H\.\s*\d+(?:,\s*\d+)*",
    r"\bKNM-[A-Z]{2}\s*\d+",
    r"\bOH\s*\d+",
    r"\bA\.?L\.?\s*\d+[-\s]*\d*",
    r"\bLAET\s*\d+-\d+",
    r"\bEP\s*\d+/\d+",
    r"\bStW\s*\d+",
    r"\bSK\s*\d+",
    r"\bTM\s*\d+",
    r"\bMLD\s*\d+",
    r"\bBOU-VP-\d+/\d+",
    r"\bD\s*\d{4}",
    r"\bLB\d+",
    r"\bLucy\b",
    r"\bLittle\s*Foot\b",
]


def extract_specimen_identifiers(comment: str | None) -> list[str]:
    """Extract standard museum catalog and specimen identifiers from comments."""
    if not comment:
        return []
    codes: list[str] = []
    for pat in SPECIMEN_PATTERNS:
        matches = re.findall(pat, comment, re.I)
        codes.extend(matches)
    return sorted(list(set(codes)))


def _parse_xlsx_sheet(xlsx_path: Path, sheet_name: str = "sheet1.xml") -> list[list[Any]]:
    """Pure stdlib zero-dependency openxml parser."""
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(xlsx_path, "r") as z:
        sst_root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        strings: list[str] = []
        for si in sst_root.findall(".//s:si", ns):
            text = "".join(t.text for t in si.findall(".//s:t", ns) if t.text)
            strings.append(text)

        sheet_root = ET.fromstring(z.read(f"xl/worksheets/{sheet_name}"))
        rows: list[list[Any]] = []
        for r in sheet_root.findall(".//s:row", ns):
            row_cells: dict[int, Any] = {}
            for c in r.findall(".//s:c", ns):
                r_coord = c.attrib.get("r", "")
                t_attr = c.attrib.get("t", "")
                v = c.find("s:v", ns)
                val = None
                if v is not None and v.text is not None:
                    if t_attr == "s":
                        val = strings[int(v.text)]
                    else:
                        val = v.text
                col_letters = "".join(ch for ch in r_coord if ch.isalpha())
                col_idx = 0
                for ch in col_letters:
                    col_idx = col_idx * 26 + (ord(ch.upper()) - ord("A") + 1)
                row_cells[col_idx - 1] = val
            if row_cells:
                max_c = max(row_cells.keys())
                row_list = [row_cells.get(i) for i in range(max_c + 1)]
                rows.append(row_list)
    return rows


def ingest_specimen_database(
    xlsx_path: Path,
) -> tuple[list[HomininSpecimenOccurrence], dict[str, Any]]:
    """Ingest raw occurrence workbook into strongly-typed specimen records."""
    rows = _parse_xlsx_sheet(xlsx_path, "sheet1.xml")
    data = [r for r in rows[1:] if any(x is not None for x in r)]

    occurrences: list[HomininSpecimenOccurrence] = []
    for idx, r in enumerate(data):
        sp_raw = r[0] if len(r) > 0 and r[0] is not None else "Unknown"
        sp_name = str(sp_raw).strip().replace(" ", "_")
        genus = sp_name.split("_")[0]
        is_homo = (genus == "Homo")
        grade = GRADE_ASSIGNMENTS.get(sp_name, EcologicalGrade.ISOLATE if is_homo else EcologicalGrade.AUSTRALOPITHECINE)

        def _to_float(val: Any) -> float | None:
            if val is None or str(val).strip() == "" or str(val).strip().lower() == "none":
                return None
            try:
                return float(val)
            except ValueError:
                return None

        def _to_str(val: Any) -> str | None:
            if val is None or str(val).strip() == "" or str(val).strip().lower() == "none":
                return None
            return str(val).strip()

        site_max = _to_float(r[3]) if len(r) > 3 else None
        site_min = _to_float(r[4]) if len(r) > 4 else None
        strat_max = _to_float(r[11]) if len(r) > 11 else None
        strat_min = _to_float(r[12]) if len(r) > 12 else None

        comment_str = _to_str(r[13]) if len(r) > 13 else None
        specimens = extract_specimen_identifiers(comment_str)

        occ = HomininSpecimenOccurrence(
            index=idx,
            species_name=sp_name,
            genus=genus,
            is_homo=is_homo,
            grade=grade,
            site_complex=_to_str(r[1]) if len(r) > 1 else None,
            site=_to_str(r[2]) if len(r) > 2 else None,
            site_max_ma=site_max,
            site_min_ma=site_min,
            subsite=_to_str(r[5]) if len(r) > 5 else None,
            subsite_type=_to_str(r[6]) if len(r) > 6 else None,
            formation=_to_str(r[9]) if len(r) > 9 else None,
            stratigraphic_unit=_to_str(r[10]) if len(r) > 10 else None,
            strat_max_ma=strat_max,
            strat_min_ma=strat_min,
            specimen_codes=specimens,
            raw_comments=comment_str,
            source=_to_str(r[14]) if len(r) > 14 else None,
            has_strat_bounds=(strat_max is not None and strat_min is not None),
            has_site_bounds=(site_max is not None and site_min is not None),
        )
        occurrences.append(occ)

    total = len(occurrences)
    homo_count = sum(1 for o in occurrences if o.is_homo)
    non_homo_count = total - homo_count

    grade_counts: dict[str, int] = {}
    for o in occurrences:
        grade_counts[o.grade.value] = grade_counts.get(o.grade.value, 0) + 1

    species_counts: dict[str, int] = {}
    for o in occurrences:
        species_counts[o.species_name] = species_counts.get(o.species_name, 0) + 1

    summary = {
        "total_occurrences": total,
        "homo_occurrences": homo_count,
        "non_homo_occurrences": non_homo_count,
        "grade_distribution": grade_counts,
        "distinct_species_count": len(species_counts),
        "species_breakdown": dict(
            sorted(species_counts.items(), key=lambda kv: kv[1], reverse=True)
        ),
    }

    return occurrences, summary
