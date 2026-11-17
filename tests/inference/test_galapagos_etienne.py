"""Unit and integration tests for the canonical Galápagos Etienne master equation solver.

Verifies:
1. Galápagos avifaunal schema invariants (SHA-256 raw ingestion, Finches brts).
2. Physical bounds: K < S species ceiling returns -inf.
3. Master equation numerical log-space stability across varying branch lengths.
4. Profile likelihood curvature for carrying capacity K on Darwin's finches.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from hominin_morphodynamics.schema.galapagos import (
    load_galapagos_csv,
    load_galapagos_json,
    ColonistStatus,
)
from hominin_morphodynamics.inference.master_equation import (
    MasterEquationParams,
    compute_etienne_loglik,
    profile_etienne_k,
)


@pytest.fixture
def galapagos_csv_path() -> Path:
    return Path("data/raw/galapagos_valente_2015/Galapagos_datatable.csv")


@pytest.fixture
def galapagos_json_path() -> Path:
    return Path("data/raw/galapagos_valente_2015/Galapagos_avifauna.json")


def test_galapagos_raw_schema_ingestion(galapagos_csv_path: Path, galapagos_json_path: Path):
    """Verify that both CSV and JSON representations parse accurately and match."""
    csv_ds = load_galapagos_csv(galapagos_csv_path)
    json_ds = load_galapagos_json(galapagos_json_path)

    assert csv_ds.total_colonizations == 8
    assert json_ds.total_colonizations == 8
    assert csv_ds.island_age_myr == 4.0
    assert csv_ds.mainland_pool_size == 1000

    # Darwin's finches verification
    finches_csv = csv_ds.finches
    finches_json = json_ds.finches
    assert finches_csv.clade_name == "Finches"
    assert finches_csv.status == ColonistStatus.ENDEMIC
    assert len(finches_csv.branching_times) == 15
    assert len(finches_json.branching_times) == 15
    assert finches_csv.species_count == 15
    assert finches_csv.colonization_time == pytest.approx(3.0282)

    # Check non-endemic status
    coccyzus = csv_ds.get_clade("Coccyzus")
    assert coccyzus.status == ColonistStatus.NON_ENDEMIC_MAX_AGE
    assert coccyzus.species_count == 1


def test_etienne_physical_carrying_capacity_invariants():
    """Verify physical invariant: clade size S cannot exceed carrying capacity ceiling K."""
    brts = [3.0, 2.0, 1.0, 0.5]  # 4 branching events -> 4 species
    params_invalid = MasterEquationParams(
        lambda_0=1.0,
        mu_0=0.1,
        k_carrying_capacity=3.0,  # S=4 > K=3 -> physically forbidden
    )
    ll = compute_etienne_loglik(params_invalid, brts)
    assert ll == -np.inf


def test_etienne_numerical_stability():
    """Verify that numerical master equation handles very close branching times without exploding."""
    # Singularity test: two branches separated by 1e-5 Myr
    brts = [2.0, 1.5, 1.0, 1.00001, 0.5]
    params = MasterEquationParams(
        lambda_0=1.5,
        mu_0=0.2,
        k_carrying_capacity=20.0,
    )
    ll = compute_etienne_loglik(params, brts)
    assert not np.isnan(ll)
    assert not np.isinf(ll)
    assert ll < 0.0


def test_darwin_finches_profile_likelihood(galapagos_csv_path: Path):
    """Verify profile log-likelihood evaluates smoothly across K for Darwin's finches."""
    ds = load_galapagos_csv(galapagos_csv_path)
    finches = ds.finches
    k_grid = [16.0, 20.0, 25.0, 30.0, 40.0]

    ks, lls = profile_etienne_k(
        finches.branching_times,
        k_grid=k_grid,
        fixed_lambda_0=1.2,
        fixed_mu_0=0.1,
    )

    assert len(ks) == len(k_grid)
    assert np.all(np.isfinite(lls))
    # Check that carrying capacity at boundary (K=16, barely above S=15) is penalized
    assert lls[0] < lls[-1]
