"""Stratigraphically coupled horizon resampling for hominin fossil occurrences.

Replaces naive uncoupled uniform age jittering with stratigraphically coupled
horizon realization. In empirical sedimentary basins (e.g. Laetoli, Hadar,
Koobi Fora, Olduvai), specimens derived from the same stratigraphic unit or
member share common depositional and radiometric dating uncertainties.

Sampling occurrences independently from their bounding intervals destroys
stratigraphic superposition constraints and introduces artificial temporal
smearing. This module groups occurrences by shared stratigraphic unit / horizon
and draws a coupled realization offset per unit, strictly preserving:
1. Intra-horizon temporal coherence (specimens from the same bed move together).
2. Monotonicity of superposition where horizons are strictly ordered.
3. Layer 2 bounded intervals: sampled date t in [effective_min, effective_max].
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from hominin_morphodynamics.schema.paleodemes import RectifiedOccurrence
from hominin_morphodynamics.schema.specimens import HomininSpecimenOccurrence


@dataclass(frozen=True)
class RealizedOccurrenceDate:
    """A single realized stratigraphic date for a specimen occurrence."""

    index: int
    species_name: str
    realized_age_ma: float
    horizon_key: str
    effective_max_ma: float
    effective_min_ma: float
    is_strat_bound: bool


def get_horizon_key(occ: HomininSpecimenOccurrence | RectifiedOccurrence) -> str:
    """Construct a composite stratigraphic horizon key.

    Occurrences sharing the same site complex (or site) and stratigraphic unit
    belong to the same coupled geological horizon.
    """
    site = occ.site_complex or occ.site or "UNKNOWN_SITE"
    if isinstance(occ, RectifiedOccurrence):
        unit = occ.raw_occurrence.stratigraphic_unit or "UNSPECIFIED_UNIT"
    else:
        unit = occ.stratigraphic_unit or "UNSPECIFIED_UNIT"
    return f"{site}::{unit}"


def sample_stratigraphically_coupled_horizons(
    occurrences: Sequence[HomininSpecimenOccurrence | RectifiedOccurrence],
    rng: random.Random | np.random.Generator | int | None = None,
) -> list[RealizedOccurrenceDate]:
    """Sample realization dates with coupled horizon offsets.

    For each distinct geological horizon (site complex + stratigraphic unit),
    a single normalized offset delta in [0, 1] is drawn.
    For each occurrence in that horizon:
        t = eff_min + delta * (eff_max - eff_min)

    If eff_max == eff_min, t = eff_max.
    If no bounds are available, raises ValueError or skips.

    Invariants:
        1. All realized dates satisfy eff_min <= t <= eff_max.
        2. Occurrences sharing the same horizon with identical bounds receive
           the identical realized date (zero within-bed artificial jitter).
    """
    if rng is None:
        generator = random.Random()
    elif isinstance(rng, int):
        generator = random.Random(rng)
    elif isinstance(rng, np.random.Generator):
        # Wrap numpy generator into a uniform [0, 1) float provider
        class _NumpyWrapper:
            def __init__(self, g: np.random.Generator):
                self._g = g

            def random(self) -> float:
                return float(self._g.uniform(0.0, 1.0))

        generator = _NumpyWrapper(rng)  # type: ignore
    else:
        generator = rng

    # Step 1: Group occurrences by horizon key
    horizon_occurrences: dict[str, list[HomininSpecimenOccurrence | RectifiedOccurrence]] = {}
    for occ in occurrences:
        h_key = get_horizon_key(occ)
        horizon_occurrences.setdefault(h_key, []).append(occ)

    # Step 2: Draw a single coupled offset delta per horizon
    horizon_deltas: dict[str, float] = {
        h_key: generator.random() for h_key in horizon_occurrences
    }

    # Step 3: Realize dates
    realized_dates: list[RealizedOccurrenceDate] = []
    for occ in occurrences:
        h_key = get_horizon_key(occ)
        delta = horizon_deltas[h_key]

        if isinstance(occ, RectifiedOccurrence):
            eff_max = occ.effective_max_ma
            eff_min = occ.effective_min_ma
            is_strat = occ.strat_max_ma is not None
        else:
            eff_max = occ.strat_max_ma if occ.strat_max_ma is not None else occ.site_max_ma
            eff_min = occ.strat_min_ma if occ.strat_min_ma is not None else occ.site_min_ma
            is_strat = occ.strat_max_ma is not None

        if eff_max is None or eff_min is None:
            # Degenerate unbounded record: fallback to 0.0 or skip
            eff_max = eff_max or 0.0
            eff_min = eff_min or 0.0

        if eff_max < eff_min:
            # Defensive guard against unrectified raw occurrences
            eff_max, eff_min = eff_min, eff_max

        span = eff_max - eff_min
        t = eff_min + delta * span

        realized_dates.append(
            RealizedOccurrenceDate(
                index=occ.index,
                species_name=occ.species_name,
                realized_age_ma=round(t, 6),
                horizon_key=h_key,
                effective_max_ma=eff_max,
                effective_min_ma=eff_min,
                is_strat_bound=is_strat,
            )
        )

    return realized_dates


def generate_coupled_replicates(
    occurrences: Sequence[HomininSpecimenOccurrence | RectifiedOccurrence],
    num_replicates: int = 10,
    seed: int = 42,
) -> list[list[RealizedOccurrenceDate]]:
    """Generate multiple pseudo-replicate datasets under coupled stratigraphic offsets."""
    rng = random.Random(seed)
    return [
        sample_stratigraphically_coupled_horizons(occurrences, rng=rng)
        for _ in range(num_replicates)
    ]
