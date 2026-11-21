"""Stochastic forward simulation of diversity-dependent insular radiations (Gillespie DGM).

Genealogy:
    Literature: Etienne et al. (2012) Proc. R. Soc. B 279:1300-1309;
                Valente et al. (2015) Nature 521:354-359.
    Rung: Forward Data-Generating Mechanism (DGM) for Simulation-Based Calibration (SBC).

Implements exact continuous-time Gillespie branching simulation of crown radiations
under diversity-dependent diversification (DDD), tracking full tree genealogy,
reconstructing the surviving phylogeny, and extracting branching times.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

import numpy as np


@dataclass(frozen=True)
class SimulatedAvifaunalTree:
    """Immutable result of a forward diversity-dependent diversification simulation."""

    crown_age: float
    branching_times: Tuple[float, ...]
    extant_richness: int
    extinct_richness: int
    total_speciation_events: int
    early_burst_ratio: float  # Fraction of branching events in the first half of total duration

    @property
    def num_branching_times(self) -> int:
        return len(self.branching_times)


def simulate_diversity_dependent_radiation(
    lambda0: float,
    mu0: float,
    k_carrying_capacity: float,
    crown_age: float,
    seed: int = 42,
    max_attempts: int = 500,
) -> SimulatedAvifaunalTree:
    """Simulate a continuous-time bifurcating crown radiation under diversity-dependence.

    Args:
        lambda0: Baseline speciation rate [Myr^-1]
        mu0: Background extinction rate [Myr^-1]
        k_carrying_capacity: Equilibrium carrying capacity K [species]
        crown_age: Island crown age [Myr before present]
        seed: Random seed for deterministic reproducibility
        max_attempts: Max rejection-sampling attempts to condition on crown survival (soc=2)

    Returns:
        SimulatedAvifaunalTree with exact reconstructed branching times.
    """
    if lambda0 <= 0.0:
        raise ValueError(f"lambda0 must be strictly positive, got {lambda0}")
    if mu0 < 0.0:
        raise ValueError(f"mu0 must be non-negative, got {mu0}")
    if k_carrying_capacity <= 2.0:
        raise ValueError(f"k_carrying_capacity must exceed 2.0, got {k_carrying_capacity}")
    if crown_age <= 0.0:
        raise ValueError(f"crown_age must be strictly positive, got {crown_age}")

    rng = random.Random(seed)

    for _ in range(max_attempts):
        t = 0.0
        # Crown condition: 2 lineages born at crown time t=0.0
        birth_t: Dict[int, float] = {1: 0.0, 2: 0.0}
        parent_seg: Dict[int, int] = {1: 0, 2: 0}
        active: List[int] = [1, 2]
        extinct: List[int] = []
        next_id = 3
        total_speciations = 1  # crown node counts as initial speciation

        while t < crown_age and len(active) > 0:
            n = len(active)
            lam_n = max(0.0, lambda0 * (1.0 - n / k_carrying_capacity)) * n
            mu_n = mu0 * n
            total_rate = lam_n + mu_n
            if total_rate <= 0.0:
                break

            dt = rng.expovariate(total_rate)
            t += dt
            if t > crown_age:
                break

            idx = rng.randrange(len(active))
            target = active.pop(idx)

            if rng.random() < (lam_n / total_rate):
                c1, c2 = next_id, next_id + 1
                next_id += 2
                birth_t[c1], birth_t[c2] = t, t
                parent_seg[c1], parent_seg[c2] = target, target
                active.append(c1)
                active.append(c2)
                total_speciations += 1
            else:
                extinct.append(target)

        # Condition on survival of both crown lineages (soc=2)
        if len(active) >= 2:
            extant_tips = set(active)
            tip_counts = {seg: 0 for seg in birth_t}
            for tip in extant_tips:
                curr = tip
                while curr != 0:
                    tip_counts[curr] += 1
                    curr = parent_seg[curr]

            if tip_counts[1] > 0 and tip_counts[2] > 0:
                reconstructed_times = [0.0]  # crown at t=0
                for seg in birth_t:
                    if seg in (1, 2):
                        continue
                    if seg % 2 == 1:
                        c1, c2 = seg, seg + 1
                        if tip_counts[c1] > 0 and tip_counts[c2] > 0:
                            reconstructed_times.append(birth_t[c1])

                # Convert node times to time before present
                brts = tuple(sorted([crown_age - node_t for node_t in reconstructed_times], reverse=True))

                # Compute early burst ratio (fraction of branching events occurring in first half)
                half_time = crown_age / 2.0
                early_nodes = sum(1 for node_t in reconstructed_times if node_t <= half_time)
                burst_ratio = float(early_nodes) / float(len(reconstructed_times))

                return SimulatedAvifaunalTree(
                    crown_age=crown_age,
                    branching_times=brts,
                    extant_richness=len(active),
                    extinct_richness=len(extinct),
                    total_speciation_events=total_speciations,
                    early_burst_ratio=burst_ratio,
                )

    raise RuntimeError(
        f"Failed to generate a surviving crown radiation after {max_attempts} attempts with seed {seed}"
    )


__all__ = [
    "SimulatedAvifaunalTree",
    "simulate_diversity_dependent_radiation",
]
