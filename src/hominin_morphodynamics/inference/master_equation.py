"""Continuous-time Master Equation solver for Diversity-Dependent Diversification (Etienne 2012).

Solves the exact continuous-time Markov master equation P(n, t) for cladogenesis
under carrying-capacity saturation (lambda(n) = max(0, lambda_0 * (1 - n/K))),
matching the canonical DAISIE/DDD formulation (Etienne et al. 2012, Valente et al. 2015).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence, Tuple

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize_scalar, minimize


@dataclass(frozen=True)
class MasterEquationParams:
    """Parameters for diversity-dependent diversification master equation."""

    lambda_0: float  # Baseline per-lineage speciation rate (Myr^-1)
    mu_0: float  # Baseline per-lineage extinction rate (Myr^-1)
    k_carrying_capacity: float  # Carrying capacity ceiling (K species)
    dd_model: float = 1.3  # 1.3: lambda(n) = lambda_0 * (1 - n/K); 1.0: linear to (lambda-mu)


def _build_etienne_transition_matrix(
    la: float, mu: float, k_cap: float, lx: int, k_lineages: int, dd_model: float = 1.3
) -> np.ndarray:
    """Build tridiagonal generator matrix M for the unobserved lineages at time interval k."""
    nvec = np.arange(lx, dtype=float)
    if dd_model == 1.3:
        lavec = np.maximum(0.0, la * (1.0 - (nvec + k_lineages) / k_cap))
        muvec = np.full(lx, mu, dtype=float)
    else:  # dd_model == 1.0
        lavec = np.maximum(0.0, la - (la - mu) * (nvec + k_lineages) / k_cap)
        muvec = np.full(lx, mu, dtype=float)

    m_matrix = np.zeros((lx, lx), dtype=float)
    # Speciation: from j to j+1 unobserved lineages
    for j in range(lx - 1):
        m_matrix[j + 1, j] = lavec[j] * (nvec[j] + 2.0 * k_lineages)
    # Extinction: from j to j-1 unobserved lineages
    for j in range(1, lx):
        m_matrix[j - 1, j] = muvec[j] * nvec[j]
    # Diagonal: total event rate loss
    for j in range(lx):
        m_matrix[j, j] = -(lavec[j] + muvec[j]) * (nvec[j] + k_lineages)
    # Boundary correction at lx-1
    m_matrix[lx - 1, lx - 1] = -muvec[lx - 1] * (nvec[lx - 1] + k_lineages)
    return m_matrix


def compute_etienne_loglik(
    params: MasterEquationParams,
    branching_times: Sequence[float],
    condition_on_survival: bool = True,
    soc: int = 2,  # 2 for crown age, 1 for stem age
) -> float:
    """Compute exact log-likelihood of branching times under Etienne's master equation.

    Parameters
    ----------
    params : MasterEquationParams
        Model parameters (lambda_0, mu_0, K).
    branching_times : Sequence[float]
        Branching times in Myr before present (positive, descending).
    condition_on_survival : bool
        If True, condition on clade surviving to present with non-extinction conditioning.
    soc : int
        2 for crown age (starts at first split), 1 for stem age (starts at colonization).

    Returns
    -------
    float
        Exact log-likelihood ln L(Theta | brts).
    """
    brts = np.sort(np.abs(np.asarray(branching_times, dtype=float)))[::-1]
    if len(brts) == 0:
        return -np.inf
    if brts[-1] != 0.0:
        brts = np.append(brts, 0.0)

    s_species = len(brts) - 1 + (soc - 2)
    if s_species < 1:
        return -np.inf

    k_cap = params.k_carrying_capacity
    if s_species > math.ceil(k_cap) and params.dd_model == 1.3:
        return -np.inf

    lx = int(math.ceil(k_cap)) + 4
    loglik = math.lgamma(s_species)

    probs = np.zeros(lx, dtype=float)
    probs[0] = 1.0  # At origin/crown age, 0 unobserved lineages

    la = params.lambda_0
    mu = params.mu_0

    for k_idx in range(1, s_species + 2 - soc):
        k1 = k_idx + (soc - 2)
        dt = abs(brts[k_idx] - brts[k_idx - 1])
        if dt > 0:
            m_mat = _build_etienne_transition_matrix(la, mu, k_cap, lx, k1, params.dd_model)
            probs = expm(m_mat * dt).dot(probs)

        if k_idx < (s_species + 2 - soc):
            # Speciation event at branching horizon
            nvec = np.arange(lx, dtype=float)
            if params.dd_model == 1.3:
                lavec = np.maximum(0.0, la * (1.0 - (nvec + k1) / k_cap))
            else:
                lavec = np.maximum(0.0, la - (la - mu) * (nvec + k1) / k_cap)
            probs = lavec * probs
            s_p = float(np.sum(probs))
            if s_p <= 0.0 or np.isnan(s_p):
                return -np.inf
            loglik += math.log(s_p)
            probs /= s_p

    p0 = float(probs[0])
    if p0 <= 0.0 or np.isnan(p0):
        return -np.inf
    loglik += math.log(p0)
    loglik -= math.lgamma(s_species + 1)

    if condition_on_survival:
        probsn = np.zeros(lx, dtype=float)
        probsn[0] = 1.0
        dt_total = abs(brts[0] - brts[-1])
        m_mat_total = _build_etienne_transition_matrix(la, mu, k_cap, lx, soc, params.dd_model)
        probsn = expm(m_mat_total * dt_total).dot(probsn)
        nvec = np.arange(lx, dtype=float)
        if soc == 2:
            aux = (nvec + 2.0) * (nvec + 3.0) / 6.0
        else:
            aux = nvec + 1.0
        probsc = probsn / aux
        norm_sum = float(np.sum(probsc))
        if norm_sum <= 0.0 or np.isnan(norm_sum):
            return -np.inf
        loglik -= math.log(norm_sum)

    return float(loglik)


def profile_etienne_k(
    branching_times: Sequence[float],
    k_grid: Sequence[float],
    fixed_lambda_0: float = 1.2,
    fixed_mu_0: float = 0.1,
    soc: int = 2,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute profile log-likelihood across carrying capacity K."""
    lls = []
    for k in k_grid:
        p = MasterEquationParams(
            lambda_0=fixed_lambda_0,
            mu_0=fixed_mu_0,
            k_carrying_capacity=k,
        )
        ll = compute_etienne_loglik(p, branching_times, condition_on_survival=True, soc=soc)
        lls.append(ll)
    return np.array(k_grid, dtype=float), np.array(lls, dtype=float)
