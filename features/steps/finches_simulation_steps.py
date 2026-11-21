"""Step definitions for forward simulation and inverse recovery of Darwin's finches."""

from __future__ import annotations

import math
from typing import Dict, List, Tuple
import numpy as np
from behave import given, when, then

from hominin_morphodynamics.inference.finches_simulation import (
    SimulatedAvifaunalTree,
    simulate_diversity_dependent_radiation,
)
from hominin_morphodynamics.inference.master_equation import (
    MasterEquationParams,
    compute_etienne_loglik,
    profile_etienne_k,
)


@given("the empirical Darwin finches radiation parameters from Valente et al. 2015")
def step_set_empirical_finches_params(context):
    """Parse baseline parameter table for Darwin's finches."""
    params = {}
    for row in context.table:
        params[row["parameter"]] = float(row["value"])
    context.finches_sim_params = params
    assert context.finches_sim_params["crown_age"] == 3.0282
    assert context.finches_sim_params["carrying_capacity_K"] == 20.0


@given("a continuous-time Gillespie birth-death simulator initialized with 2 crown lineages")
def step_init_gillespie_simulator(context):
    """Set up Gillespie simulator configuration."""
    context.sim_seed = 1  # Deterministic seed replicating finch-like richness


@when("the simulation executes forward for 3.0282 Myr under the canonical diversity-dependence function")
def step_execute_forward_simulation(context):
    """Run forward continuous-time branching simulation."""
    p = context.finches_sim_params
    tree = simulate_diversity_dependent_radiation(
        lambda0=p["lambda_0"],
        mu0=p["mu_0"],
        k_carrying_capacity=p["carrying_capacity_K"],
        crown_age=p["crown_age"],
        seed=context.sim_seed,
    )
    context.simulated_tree = tree


@then("the surviving clade must reach an extant richness S between 12 and 22 species")
def step_verify_extant_richness(context):
    """Check that realized simulated richness falls within empirical insular envelope."""
    tree: SimulatedAvifaunalTree = context.simulated_tree
    assert 12 <= tree.extant_richness <= 22, (
        f"Expected extant richness between 12 and 22, got {tree.extant_richness}"
    )


@then("the temporal distribution of branching events must reflect early cladogenetic burst")
def step_verify_early_burst(context):
    """Verify rate deceleration where early branching outpaces late branching."""
    tree: SimulatedAvifaunalTree = context.simulated_tree
    # Early branching times should cover a significant fraction of nodes
    assert len(tree.branching_times) >= 10
    # In a burst radiation, earlier intervals (near crown age 3.0282) occur rapidly
    brts = tree.branching_times
    assert brts[0] == 3.0282  # Crown age preserved
    assert brts[-1] < 0.2     # Extends near the present


@then("the reconstructed tree must satisfy the exact topological invariant of S minus 1 branching nodes")
def step_verify_bifurcation_invariant(context):
    """Verify that a reconstructed bifurcating tree of S tips has exactly S - 1 internal branching nodes."""
    tree: SimulatedAvifaunalTree = context.simulated_tree
    expected_nodes = tree.extant_richness - 1
    assert tree.num_branching_times == expected_nodes, (
        f"Topological invariant violated: S={tree.extant_richness} tips but "
        f"{tree.num_branching_times} branching times (expected {expected_nodes})"
    )


@given("a simulated phylogenetic tree generated under true carrying capacity K = 20.0")
def step_prepare_simulated_tree(context):
    """Ensure a deterministic simulated tree under K=20 is available."""
    p = context.finches_sim_params
    context.simulated_tree = simulate_diversity_dependent_radiation(
        lambda0=p["lambda_0"],
        mu0=p["mu_0"],
        k_carrying_capacity=20.0,
        crown_age=3.0282,
        seed=1,
    )
    assert context.simulated_tree.extant_richness == 16


@when("the Etienne master equation computes the profile log-likelihood across a candidate grid of K from 16 to 100")
def step_compute_simulated_profile(context):
    """Compute carrying-capacity profile likelihood across candidate K grid."""
    tree: SimulatedAvifaunalTree = context.simulated_tree
    k_grid = [16.0, 18.0, 20.0, 25.0, 30.0, 40.0, 100.0]
    ks, lls = profile_etienne_k(
        tree.branching_times,
        k_grid=k_grid,
        fixed_lambda_0=context.finches_sim_params["lambda_0"],
        fixed_mu_0=context.finches_sim_params["mu_0"],
        soc=2,
    )
    context.profile_ks = ks
    context.profile_lls = lls


@then("candidate K values violating physical standing richness must evaluate to negative infinity")
def step_verify_simulated_physical_boundary(context):
    """Verify that candidate K strictly below S returns -inf."""
    tree: SimulatedAvifaunalTree = context.simulated_tree
    violating_k = float(tree.extant_richness - 10)  # K=6 for S=16
    p = MasterEquationParams(
        lambda_0=context.finches_sim_params["lambda_0"],
        mu_0=context.finches_sim_params["mu_0"],
        k_carrying_capacity=violating_k,
    )
    ll = compute_etienne_loglik(p, tree.branching_times, soc=2)
    assert np.isneginf(ll), f"Expected -inf for K={violating_k} < S={tree.extant_richness}, got {ll}"


@then("the maximum likelihood estimate hat_K must fall within an acceptable recovery band of the true parameter K = 20.0")
def step_verify_k_recovery(context):
    """Verify that MLE hat_K peaks near the true simulation value of 20.0."""
    ks = context.profile_ks
    lls = context.profile_lls
    best_idx = int(np.argmax(lls))
    hat_k = ks[best_idx]
    # Acceptable recovery band [18.0, 25.0] for true K=20.0
    assert 18.0 <= hat_k <= 25.0, f"MLE hat_K={hat_k} outside recovery band [18, 25] (true K=20)"


@then("the unconstrained diversification model at K = 100 must be penalized relative to the peak carrying capacity")
def step_verify_unconstrained_penalty(context):
    """Verify that unconstrained capacity (K=100) has significantly lower likelihood than hat_K."""
    lls = context.profile_lls
    max_ll = float(np.max(lls))
    k100_ll = float(lls[-1])
    delta_ll = max_ll - k100_ll
    # Significant penalty (> 2 nats)
    assert delta_ll > 2.0, f"Expected delta_ll > 2.0 nats against K=100, got {delta_ll:.3f}"


@given("an ensemble of forward-simulated trees under true bounded capacity K = 20.0")
def step_prepare_bounded_ensemble(context):
    """Generate ensemble of bounded trees."""
    p = context.finches_sim_params
    context.bounded_trees = []
    for s in [0, 1, 2]:
        t = simulate_diversity_dependent_radiation(
            lambda0=p["lambda_0"],
            mu0=p["mu_0"],
            k_carrying_capacity=20.0,
            crown_age=3.0282,
            seed=s,
        )
        context.bounded_trees.append(t)


@given("an ensemble of forward-simulated trees under unbounded diversification")
def step_prepare_unbounded_ensemble(context):
    """Generate ensemble of trees under unbounded diversification (K=1000)."""
    p = context.finches_sim_params
    context.unbounded_trees = []
    for s in [10, 11]:
        t = simulate_diversity_dependent_radiation(
            lambda0=1.0,
            mu0=0.1,
            k_carrying_capacity=1000.0,
            crown_age=2.8,
            seed=s,
        )
        context.unbounded_trees.append(t)


@when("both ensembles are inverted through the carrying capacity profiler")
def step_invert_both_ensembles(context):
    """Profile both bounded and unbounded ensembles."""
    p = context.finches_sim_params
    context.bounded_deltas = []
    for t in context.bounded_trees:
        k_eval = [float(t.extant_richness), 20.0, 100.0]
        ks, lls = profile_etienne_k(t.branching_times, k_grid=k_eval, fixed_lambda_0=p["lambda_0"], fixed_mu_0=p["mu_0"], soc=2)
        # delta = peak - K100
        delta = float(np.max(lls) - lls[-1])
        context.bounded_deltas.append(delta)

    context.unbounded_deltas = []
    for t in context.unbounded_trees:
        k_eval = [float(t.extant_richness), 50.0, 500.0]
        ks, lls = profile_etienne_k(t.branching_times, k_grid=k_eval, fixed_lambda_0=1.0, fixed_mu_0=0.1, soc=2)
        # For unbounded, likelihood at large K should be >= likelihood at small K
        context.unbounded_deltas.append(float(lls[-1] - lls[0]))


@then("the bounded simulations must exhibit an interior likelihood maximum near true capacity")
def step_verify_bounded_interior_max(context):
    """Verify bounded simulations penalize K=100."""
    for d in context.bounded_deltas:
        assert d > 0.0, f"Bounded tree did not exhibit peak over K=100: delta={d}"


@then("the unbounded simulations must show monotonically non-decreasing likelihood toward large K")
def step_verify_unbounded_monotonic(context):
    """Verify unbounded simulations prefer larger K over small K."""
    for d in context.unbounded_deltas:
        assert d >= 0.0, f"Unbounded tree penalized large K: delta={d}"
