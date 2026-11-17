"""Mathematical derivations and reference models for diversity-dependent diversification.

Decomposes the theoretical foundations from the intellectual precursors of
diversity-dependent macroevolution:
1. MacArthur & Wilson (1967): Equilibrium Theory of Island Biogeography.
2. Walker & Valentine (1984): Adaptive grid saturation and empty ecospace.
3. Etienne et al. (2012): Exact master equations for diversity-dependent
   diversification under carrying capacity K.
4. Silvestro et al. (2014, 2019): Continuous-time inhomogeneous Poisson hazard
   formulation in PyRate (Linear vs Exponential dependence).

Provides reference simulators for:
- Idealized insular adaptive radiation (Galapagos finches / Anolis lizards)
  where physical competition over a closed niche space genuinely drives
  speciation slowdowns (Etienne-MacArthur model).
- Fossil taphonomic Poisson sampling (Silvestro preservation conditioning).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class PrecursorLineageEvent:
    """Lineage event in an idealized diversity-dependent radiation."""

    lineage_id: str
    parent_id: str | None
    origin_time: float  # Forward time from root (0 -> T)
    extinction_time: float | None  # None if survives to present
    num_fossil_occurrences: int = 0
    fossil_occurrence_times: tuple[float, ...] = ()


@dataclass(frozen=True)
class PrecursorCladeSimulation:
    """Complete history of an idealized insular adaptive radiation."""

    model_type: str  # "linear_etienne" | "exponential_silvestro" | "density_independent"
    carrying_capacity_k: float | None
    baseline_lambda0: float
    baseline_mu0: float
    gl_param: float
    duration: float
    lineages: list[PrecursorLineageEvent]
    time_series_t: np.ndarray
    time_series_diversity: np.ndarray


def simulate_etienne_macarthur_radiation(
    carrying_capacity_k: float = 25.0,
    lambda0: float = 1.0,
    mu0: float = 0.15,
    max_duration: float = 10.0,
    preservation_rate_q: float = 2.0,
    seed: int = 42,
) -> PrecursorCladeSimulation:
    """Simulate an idealized insular adaptive radiation under Etienne et al. (2012) dynamics.

    Mathematical Formulation:
        Per-lineage speciation rate:
            lambda(n) = max(0.0, lambda0 * (1.0 - n / K))
        Per-lineage extinction rate:
            mu(n) = mu0 (density-independent baseline)
        Total clade event rates:
            R_speciation(n) = n * lambda(n)
            R_extinction(n) = n * mu0
            R_total(n) = R_speciation + R_extinction

    At carrying capacity n = K, lambda(n) drops to 0.0, halting cladogenesis.
    Equilibrium diversity occurs when lambda(n) = mu0:
        n_eq = K * (1.0 - mu0 / lambda0)

    This represents the *idealized canonical case* of ecological niche-filling
    in a closed, saturated insular ecospace (e.g. Hawaiian honeycreepers, Anolis).
    """
    rng = np.random.default_rng(seed)

    t = 0.0
    current_lineages: dict[str, float] = {"lin_0": t, "lin_1": t}  # Start with 2 sister species
    parent_map: dict[str, str | None] = {"lin_0": None, "lin_1": None}
    extinct_lineages: dict[str, tuple[float, float]] = {}  # id -> (origin, extinction)

    next_id = 2
    time_points = [t]
    div_points = [len(current_lineages)]

    while t < max_duration and len(current_lineages) > 0:
        n = len(current_lineages)
        per_capita_lam = max(0.0, lambda0 * (1.0 - n / carrying_capacity_k))
        r_spec = n * per_capita_lam
        r_ext = n * mu0
        r_tot = r_spec + r_ext

        if r_tot <= 0.0:
            # Radiation frozen at carrying capacity
            t = max_duration
            time_points.append(t)
            div_points.append(n)
            break

        dt = float(rng.exponential(1.0 / r_tot))
        if t + dt >= max_duration:
            t = max_duration
            time_points.append(t)
            div_points.append(n)
            break

        t += dt
        # Event draw
        p_spec = r_spec / r_tot
        if rng.uniform() < p_spec:
            # Speciation: choose random parent lineage to bud a daughter
            parent = rng.choice(list(current_lineages.keys()))
            new_lin_id = f"lin_{next_id}"
            next_id += 1
            current_lineages[new_lin_id] = t
            parent_map[new_lin_id] = parent
        else:
            # Extinction: choose random lineage to go extinct
            victim = rng.choice(list(current_lineages.keys()))
            orig_t = current_lineages.pop(victim)
            extinct_lineages[victim] = (orig_t, t)

        time_points.append(t)
        div_points.append(len(current_lineages))

    # Assemble lineage objects and simulate fossil preservation
    lineage_records: list[PrecursorLineageEvent] = []
    all_keys = list(extinct_lineages.keys()) + list(current_lineages.keys())

    for lid in all_keys:
        if lid in extinct_lineages:
            o_t, e_t = extinct_lineages[lid]
        else:
            o_t = current_lineages[lid]
            e_t = None

        # Poisson fossil sampling over lifespan [o_t, e_t or max_duration]
        lifespan_end = e_t if e_t is not None else max_duration
        lifespan_len = max(0.0, lifespan_end - o_t)
        num_fossils = int(rng.poisson(preservation_rate_q * lifespan_len))
        if num_fossils > 0:
            fossil_times = tuple(sorted(float(x) for x in rng.uniform(o_t, lifespan_end, size=num_fossils)))
        else:
            fossil_times = ()

        lineage_records.append(
            PrecursorLineageEvent(
                lineage_id=lid,
                parent_id=parent_map[lid],
                origin_time=o_t,
                extinction_time=e_t,
                num_fossil_occurrences=num_fossils,
                fossil_occurrence_times=fossil_times,
            )
        )

    return PrecursorCladeSimulation(
        model_type="linear_etienne",
        carrying_capacity_k=carrying_capacity_k,
        baseline_lambda0=lambda0,
        baseline_mu0=mu0,
        gl_param=-lambda0 / carrying_capacity_k,
        duration=max_duration,
        lineages=lineage_records,
        time_series_t=np.array(time_points),
        time_series_diversity=np.array(div_points),
    )


def simulate_silvestro_exponential_radiation(
    lambda0: float = 0.8,
    gl: float = -0.08,
    mu0: float = 0.2,
    max_duration: float = 10.0,
    preservation_rate_q: float = 2.0,
    seed: int = 42,
) -> PrecursorCladeSimulation:
    """Simulate clade diversification under Silvestro et al. (2014) PyRate exponential hazard.

    Mathematical Formulation:
        Per-lineage speciation rate:
            lambda(n) = lambda0 * exp(gl * n)
        Per-lineage extinction rate:
            mu(n) = mu0

    In contrast to Etienne's linear drop to zero at K, the exponential model:
        1. Keeps lambda(n) strictly positive for all finite n (no hard ceiling K).
        2. If gl < 0: Asymptotically decelerates cladogenesis as n increases.
        3. If gl > 0: Superexponential explosion (diversity begets diversity).
    """
    rng = np.random.default_rng(seed)

    t = 0.0
    current_lineages: dict[str, float] = {"lin_0": t, "lin_1": t}
    parent_map: dict[str, str | None] = {"lin_0": None, "lin_1": None}
    extinct_lineages: dict[str, tuple[float, float]] = {}

    next_id = 2
    time_points = [t]
    div_points = [len(current_lineages)]

    while t < max_duration and len(current_lineages) > 0:
        n = len(current_lineages)
        # Clamped exponential hazard
        exponent = np.clip(gl * n, -30.0, 30.0)
        per_capita_lam = lambda0 * math.exp(float(exponent))
        r_spec = n * per_capita_lam
        r_ext = n * mu0
        r_tot = r_spec + r_ext

        if r_tot <= 0.0:
            break

        dt = float(rng.exponential(1.0 / r_tot))
        if t + dt >= max_duration:
            t = max_duration
            time_points.append(t)
            div_points.append(n)
            break

        t += dt
        p_spec = r_spec / r_tot
        if rng.uniform() < p_spec:
            parent = rng.choice(list(current_lineages.keys()))
            new_lin_id = f"lin_{next_id}"
            next_id += 1
            current_lineages[new_lin_id] = t
            parent_map[new_lin_id] = parent
        else:
            victim = rng.choice(list(current_lineages.keys()))
            orig_t = current_lineages.pop(victim)
            extinct_lineages[victim] = (orig_t, t)

        time_points.append(t)
        div_points.append(len(current_lineages))

    lineage_records: list[PrecursorLineageEvent] = []
    all_keys = list(extinct_lineages.keys()) + list(current_lineages.keys())

    for lid in all_keys:
        if lid in extinct_lineages:
            o_t, e_t = extinct_lineages[lid]
        else:
            o_t = current_lineages[lid]
            e_t = None

        lifespan_end = e_t if e_t is not None else max_duration
        lifespan_len = max(0.0, lifespan_end - o_t)
        num_fossils = int(rng.poisson(preservation_rate_q * lifespan_len))
        if num_fossils > 0:
            fossil_times = tuple(sorted(float(x) for x in rng.uniform(o_t, lifespan_end, size=num_fossils)))
        else:
            fossil_times = ()

        lineage_records.append(
            PrecursorLineageEvent(
                lineage_id=lid,
                parent_id=parent_map[lid],
                origin_time=o_t,
                extinction_time=e_t,
                num_fossil_occurrences=num_fossils,
                fossil_occurrence_times=fossil_times,
            )
        )

    return PrecursorCladeSimulation(
        model_type="exponential_silvestro",
        carrying_capacity_k=None,
        baseline_lambda0=lambda0,
        baseline_mu0=mu0,
        gl_param=gl,
        duration=max_duration,
        lineages=lineage_records,
        time_series_t=np.array(time_points),
        time_series_diversity=np.array(div_points),
    )
