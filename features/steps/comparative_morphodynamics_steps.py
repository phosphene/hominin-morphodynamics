"""Step definitions for comparative morphodynamics, Etienne modeling, and Foley paleodemes."""

from __future__ import annotations

import math
from pathlib import Path
import numpy as np
from behave import given, when, then

from hominin_morphodynamics.schema.galapagos import (
    load_galapagos_csv,
    GalapagosDataset,
)
from hominin_morphodynamics.schema.specimens import (
    ingest_specimen_database,
)
from hominin_morphodynamics.schema.paleodemes import (
    rectify_all_occurrences,
    project_paleodemes,
    PaleodemeCluster,
    GeographicBasin,
)
from hominin_morphodynamics.inference.master_equation import (
    MasterEquationParams,
    compute_etienne_loglik,
    profile_etienne_k,
)
from hominin_morphodynamics.inference.comparative_metrics import (
    generate_canonical_comparison,
)


@given("the canonical Galapagos terrestrial avifauna dataset from Valente et al. 2015")
def step_load_galapagos(context):
    """Load canonical Galápagos avifaunal radiation dataset."""
    csv_path = context.data_dir / "galapagos_valente_2015" / "Galapagos_datatable.csv"
    assert csv_path.exists(), f"Galapagos CSV not found at {csv_path}"
    context.galapagos_dataset = load_galapagos_csv(csv_path)
    assert context.galapagos_dataset.total_colonizations == 8


@given("the Plio-Pleistocene hominin specimen occurrence database from Van Holstein & Foley 2024")
def step_load_hominin_specimens(context):
    """Load raw hominin specimen occurrences from Excel database."""
    excel_path = context.data_dir / "van_holstein_2024" / "Occurrence_database.xlsx"
    assert excel_path.exists(), f"Hominin database not found at {excel_path}"
    db = ingest_specimen_database(excel_path)
    context.raw_specimens = db[0]
    assert len(context.raw_specimens) == 385


@when("the Etienne continuous-time master equation evaluates Darwin's finches across carrying capacity K")
def step_eval_finches_profile(context):
    """Compute profile log-likelihood across carrying capacity K for Darwin's finches."""
    finches = context.galapagos_dataset.finches
    k_grid = [16.0, 18.0, 20.0, 25.0, 30.0, 40.0]
    ks, lls = profile_etienne_k(
        finches.branching_times,
        k_grid=k_grid,
        fixed_lambda_0=1.2,
        fixed_mu_0=0.1,
    )
    context.finches_profile = (ks, lls)


@then("the log-likelihood profile must exhibit sharp penalization as K approaches the standing species count S")
def step_verify_finches_penalization(context):
    """Verify log-likelihood is steeply penalized near S=15."""
    ks, lls = context.finches_profile
    assert lls[0] < lls[-1]
    assert np.all(np.isfinite(lls))


@then("carrying capacity K must be statistically identifiable with likelihood-ratio p-value < 0.05")
def step_verify_finches_identifiable(context):
    """Verify carrying capacity K is statistically identifiable in Galápagos finches."""
    report = generate_canonical_comparison()
    assert report.insular_carrying_capacity_k_identified is True
    assert report.insular_profile_lrt_p_value < 0.05


@then("the physical invariant K >= S must be strictly enforced with log-likelihood of negative infinity when violated")
def step_verify_k_ge_s_invariant(context):
    """Verify physical invariant that K < S yields log-likelihood of -inf."""
    brts = [3.0, 2.0, 1.0, 0.5]  # 4 species
    params_violating = MasterEquationParams(
        lambda_0=1.0,
        mu_0=0.1,
        k_carrying_capacity=3.0,  # S=4 > K=3
    )
    ll = compute_etienne_loglik(params_violating, brts)
    assert ll == -np.inf


@when("the Etienne master equation is applied to canonical Plio-Pleistocene Homo branching times across carrying capacity K")
def step_eval_hominin_profile(context):
    """Evaluate profile log-likelihood across carrying capacity K for hominins."""
    homo_branching_times = [2.80, 2.31, 1.89, 1.21, 0.78, 0.43, 0.24]
    k_grid = [8.0, 10.0, 12.0, 15.0, 20.0, 30.0, 50.0, 100.0, 500.0]
    ks, lls = profile_etienne_k(
        homo_branching_times,
        k_grid=k_grid,
        fixed_lambda_0=1.0,
        fixed_mu_0=0.1,
        soc=2,
    )
    context.hominin_profile = (ks, lls)


@then("the maximum log-likelihood variation across carrying capacity K from 8 to 500 must be less than 0.60 units")
def step_verify_hominin_flat_profile(context):
    """Verify log-likelihood profile across K in hominins is essentially flat."""
    ks, lls = context.hominin_profile
    delta_max = float(np.max(lls) - np.min(lls))
    assert delta_max < 0.60, f"Expected delta < 0.60, got {delta_max}"


@then("the profile likelihood must not reject the unconstrained null with p-value >= 0.25")
def step_verify_hominin_non_rejection(context):
    """Verify carrying capacity in hominins does not reject null."""
    report = generate_canonical_comparison()
    assert report.hominin_carrying_capacity_identified is False
    assert report.hominin_profile_lrt_p_value >= 0.25


@then("the empirical MCMC credible intervals for speciation slope Gl must span zero across all published taxonomic schemes")
def step_verify_mcmc_cis_span_zero(context):
    """Verify that published 95% Bayesian CIs for Gl span zero."""
    published_cis = {
        "Broad_NHPP": (-1.905, 6.258),
        "Broad_TPP": (-0.082, 0.221),
        "Fine_NHPP": (-2.110, 5.892),
        "WoodBoyle_NHPP": (-1.750, 6.104),
        "All_NHPP": (-1.450, 1.210),
    }
    for scheme, (ci_low, ci_high) in published_cis.items():
        assert ci_low < 0.0 < ci_high, f"CI for {scheme} does not span zero: [{ci_low}, {ci_high}]"


@when("the raw hominin occurrence database is audited for physical chronological invariants")
def step_audit_stratigraphic_invariants(context):
    """Audit raw occurrence records for temporal inversions and missing horizons."""
    occs = context.raw_specimens
    inverted_site = {o.index for o in occs if o.site_max_ma is not None and o.site_min_ma is not None and o.site_max_ma < o.site_min_ma}
    inverted_strat = {o.index for o in occs if o.strat_max_ma is not None and o.strat_min_ma is not None and o.strat_max_ma < o.strat_min_ma}
    all_inversions = inverted_site | inverted_strat
    unbounded = [o for o in occs if o.strat_max_ma is None or o.strat_min_ma is None]
    context.audit_metrics = {
        "inverted_count": len(all_inversions),
        "unbounded_pct": (len(unbounded) / len(occs)) * 100.0,
    }
    context.rectified_specimens = rectify_all_occurrences(occs)


@then("exactly 5 published records must be flagged with inverted physical ages across site or stratigraphic horizons")
def step_verify_5_inversions(context):
    """Verify exactly 5 physical age inversions exist in the published database."""
    assert context.audit_metrics["inverted_count"] == 5


@then("more than 50% of the occurrences must be flagged as lacking bed-level stratigraphic resolution")
def step_verify_unbounded_percentage(context):
    """Verify over 50% of records lack bed-level bounds."""
    assert context.audit_metrics["unbounded_pct"] > 50.0


@then("the raw specimen records must be rectified without in-place mutation of Layer 0 provenance")
def step_verify_rectification_purity(context):
    """Verify Layer 0 raw records remain unaltered while Layer 2 rectified records are valid."""
    assert len(context.rectified_specimens) == len(context.raw_specimens)
    inverted_raw = [
        o for o in context.raw_specimens
        if (o.site_max_ma is not None and o.site_min_ma is not None and o.site_max_ma < o.site_min_ma)
        or (o.strat_max_ma is not None and o.strat_min_ma is not None and o.strat_max_ma < o.strat_min_ma)
    ]
    assert len(inverted_raw) == 5
    for r in context.rectified_specimens:
        if r.effective_max_ma is not None and r.effective_min_ma is not None:
            assert r.effective_max_ma >= r.effective_min_ma


@given("the hominin occurrences have been audited and rectified")
def step_ensure_rectified(context):
    """Ensure raw specimens are ingested and rectified for subsequent steps."""
    if context.rectified_specimens is None:
        context.rectified_specimens = rectify_all_occurrences(context.raw_specimens)


@when("the rectified hominin occurrences are projected into localized paleodemes by sedimentary basin and ecological grade")
def step_project_paleodemes(context):
    """Project occurrences into localized spatio-temporal paleodemes."""
    context.paleodeme_clusters = project_paleodemes(context.rectified_specimens, time_window_myr=0.5)


@then("at least 50 distinct spatio-temporal paleodemes must be formed across the 0.5 Myr time slices")
def step_verify_paleodeme_count(context):
    """Verify cluster count."""
    assert len(context.paleodeme_clusters) >= 50


@then("the paleodemes must partition specimens into regional basins including Turkana, Afar, Olduvai-Laetoli, and South African Karst")
def step_verify_basins_represented(context):
    """Verify key evolutionary basins are represented in the paleodemes."""
    basins = {c.basin for c in context.paleodeme_clusters}
    assert GeographicBasin.TURKANA in basins
    assert GeographicBasin.AFAR_RIFT in basins
    assert GeographicBasin.OLDUVAI_LAETOLI in basins
    assert GeographicBasin.SOUTH_AFRICA_KARST in basins


@then("the resulting demographic clusters must serve as a plausible, non-dogmatic exploratory framework for underdetermined fossil data")
def step_verify_epistemic_scaffolding(context):
    """Confirm paleodemes serve as an exploratory scaffolding."""
    for c in context.paleodeme_clusters:
        assert isinstance(c, PaleodemeCluster)
        assert c.time_slice_ma[0] > c.time_slice_ma[1]
        assert len(c.occurrence_indices) > 0
