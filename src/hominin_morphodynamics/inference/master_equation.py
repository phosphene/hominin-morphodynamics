"""Continuous-time Master Equation solver for Diversity-Dependent Diversification (Etienne 2012).

Re-exports and delegates to phosphene.holonomy.macroevo.master_equation with full backward-compatibility.
"""

from __future__ import annotations

from typing import Sequence, Tuple
import numpy as np

import phosphene.holonomy.macroevo.master_equation as _me
from phosphene.holonomy.macroevo.master_equation import (
    construct_transition_matrix,
    solve_master_equation,
    compute_etienne_branching_loglik,
)


class MasterEquationParams(_me.MasterEquationParams):
    """Parameters for diversity-dependent diversification master equation.

    Supports both original (lambda_0, mu_0, k_carrying_capacity) and holonomy (lambda0, mu0, K) attributes.
    """

    def __init__(
        self,
        lambda_0: float | None = None,
        mu_0: float | None = None,
        k_carrying_capacity: float | None = None,
        lambda0: float | None = None,
        mu0: float | None = None,
        K: float | None = None,
        max_richness: int = 50,
        dd_model: float = 1.3,
    ) -> None:
        eff_l0 = lambda_0 if lambda_0 is not None else (lambda0 if lambda0 is not None else 1.0)
        eff_mu = mu_0 if mu_0 is not None else (mu0 if mu0 is not None else 0.0)
        eff_K = k_carrying_capacity if k_carrying_capacity is not None else (K if K is not None else 50.0)
        object.__setattr__(self, "lambda0", float(eff_l0))
        object.__setattr__(self, "mu0", float(eff_mu))
        object.__setattr__(self, "K", float(eff_K))
        object.__setattr__(self, "max_richness", int(max_richness))
        object.__setattr__(self, "dd_model", float(dd_model))
        self.__post_init__()

    @property
    def lambda_0(self) -> float:
        return self.lambda0

    @property
    def mu_0(self) -> float:
        return self.mu0

    @property
    def k_carrying_capacity(self) -> float:
        return self.K


def compute_etienne_loglik(
    params: MasterEquationParams,
    branching_times: Sequence[float],
    condition_on_survival: bool = True,
    soc: int = 2,
) -> float:
    """Backward compatibility wrapper for compute_etienne_branching_loglik."""
    holonomy_params = _me.MasterEquationParams(
        lambda0=params.lambda0,
        mu0=params.mu0,
        K=params.K,
        max_richness=params.max_richness,
        dd_model=params.dd_model,
    )
    return compute_etienne_branching_loglik(
        holonomy_params,
        branching_times=branching_times,
        condition_on_survival=condition_on_survival,
        soc=soc,
    )


def profile_etienne_k(
    branching_times: Sequence[float],
    k_grid: Sequence[float],
    fixed_lambda_0: float = 1.2,
    fixed_mu_0: float = 0.1,
    soc: int = 2,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute profile log-likelihood across carrying capacity K."""
    return _me.profile_etienne_k(
        branching_times=branching_times,
        k_grid=k_grid,
        fixed_lambda0=fixed_lambda_0,
        fixed_mu0=fixed_mu_0,
        soc=soc,
    )


__all__ = [
    "MasterEquationParams",
    "construct_transition_matrix",
    "solve_master_equation",
    "compute_etienne_branching_loglik",
    "compute_etienne_loglik",
    "profile_etienne_k",
]
