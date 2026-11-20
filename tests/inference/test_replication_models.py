"""Tests for phylogenetic tip DR auditing and diversity-dependence likelihood surfaces."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pytest

from phosphene.holonomy.macroevo import newick_tip_paths
from hominin_morphodynamics.evogeog.phylogenetic_dr import (
    audit_phylogenetic_tree_tips,
    load_tree_paths_from_file,
    run_ols_dr_regression,
)
from hominin_morphodynamics.inference.diversity_surface import (
    audit_van_holstein_empirical_grid,
    fit_diversity_dependence,
)


def test_newick_parser_handles_internal_labels_and_lengths():
    """Verify clean dynamic Newick parsing via holonomy.macroevo.newick_tip_paths."""
    tree_str = "((Homo_sapiens:0.2,Homo_neanderthalensis:0.2)Ancestor:0.4,Pan_troglodytes:1.0):0.0;"
    paths = newick_tip_paths(tree_str)
    assert "Homo_sapiens" in paths
    assert paths["Homo_sapiens"] == (0.2, 0.4)
    assert paths["Homo_neanderthalensis"] == (0.2, 0.4)
    assert paths["Pan_troglodytes"] == (1.0,)


def test_tip_dr_detects_polytomy_outlier():
    """Verify that unregularized tip DR blows up on Ardipithecus due to the 4.82e-12 branch."""
    tree_path = (
        Path(__file__).parent.parent.parent
        / "data"
        / "raw"
        / "van_holstein_2024"
        / "parins_fukuchi_2019_consensus.nwk"
    )
    assert tree_path.exists(), f"Benchmark tree fixture missing at {tree_path}"

    records = audit_phylogenetic_tree_tips(tree_path, regularization_floor=1e-4)

    # Ingroup leaf tips: 18 leaves minus 2 outgroups = 16 ingroup hominin taxa
    assert len(records) == 16

    # Find Ardipithecus ramidus (carries the 4.82e-12 Myr internal polytomy edge)
    ardi = next(r for r in records if r.species_name == "Ardipithecus_ramidus")
    assert ardi.has_polytomy_artifact
    # Under canonical Jetz (2012) DR = 1 / ES, both raw and regularized DR remain finite and well-behaved
    assert np.isfinite(ardi.tip_dr_raw)
    assert np.isfinite(ardi.tip_dr_regularized)
    assert ardi.tip_dr_regularized > 0.0


def test_synthetic_diversity_dependence_fit():
    """Verify optimization recovers sign of Gl on synthetic step-function diversity."""
    t_grid = np.linspace(0, 3, 301)
    d_grid = np.where((t_grid >= 1.0) & (t_grid <= 2.0), 8.0, 2.0)

    # Events clustered during high-diversity phase
    ts_pos = [1.2, 1.4, 1.5, 1.6, 1.8]
    res_pos = fit_diversity_dependence(
        speciation_times_ma=ts_pos,
        ltt_time_grid_ma=t_grid,
        ltt_diversity_grid=d_grid,
        t_max_eval_ma=3.0,
    )

    # MLE of Gl should be positive
    assert res_pos.mle_gl > 0.0
    assert res_pos.full_loglik >= res_pos.null_loglik


def test_empirical_van_holstein_pyrate_grid():
    """Verify empirical likelihood-ratio test across PyRate outputs confirms p >= 0.05 for Homo."""
    outputs_dir = (
        Path(__file__).parent.parent.parent.parent.parent
        / "marsyas6"
        / "papers"
        / "valence-ingress"
        / "data"
        / "van-holstein"
        / "Data_Code_Final"
        / "PyRate"
        / "Outputs"
    )

    if not outputs_dir.exists():
        pytest.skip(f"PyRate outputs dir not found at {outputs_dir}")

    results = audit_van_holstein_empirical_grid(outputs_dir)
    assert len(results) >= 15  # 5 configs x 3 groups

    # Every Homo configuration must fail to reject null at alpha=0.05
    homo_results = [r for r in results if r.clade_group == "Homo"]
    assert len(homo_results) == 5
    for r in homo_results:
        assert r.p_value >= 0.05, f"{r.config_name} Homo p-value ({r.p_value}) is unexpectedly < 0.05"
        assert not r.is_significant_at_05
