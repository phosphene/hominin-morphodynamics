"""Tests for diversity-dependence parameter stability audit."""

from __future__ import annotations

from pathlib import Path

from hominin_morphodynamics.inference.pyrate_audit import (
    audit_all_logs,
    audit_mcmc_log,
)

# Resolve repo-local raw data first, falling back to workspace path if present
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_OUTPUTS = REPO_ROOT / "data/raw/van_holstein_2024/PyRate/Outputs"
WORKSPACE_OUTPUTS = Path(
    "/home/node/.openclaw/workspace/work/marsyas6/papers/valence-ingress/data/van-holstein/Data_Code_Final/PyRate/Outputs"
)
PUBLISHED_OUTPUTS = LOCAL_OUTPUTS if LOCAL_OUTPUTS.exists() else WORKSPACE_OUTPUTS


def test_diversity_dependence_credible_intervals_span_zero() -> None:
    assert PUBLISHED_OUTPUTS.exists(), f"Published outputs missing: {PUBLISHED_OUTPUTS}"
    audits = audit_all_logs(PUBLISHED_OUTPUTS)
    assert len(audits) >= 12

    homo_runs = [a for a in audits if a.clade == "Homo"]
    assert len(homo_runs) >= 4

    # Formal falsification check: in no configuration does Gl's 95% CI exclude zero
    for run in homo_runs:
        assert run.spans_zero is True
        assert run.min_gl < 0.0


def test_broad_nhpp_audit_parameters() -> None:
    log_file = PUBLISHED_OUTPUTS / "Broad_occurrence_level/NHPP/homo_diversity_0_expSp_expEx_HP.log"
    res = audit_mcmc_log(log_file, burn_in=100)

    assert res.clade == "Homo"
    assert res.analyzed_samples == 1900
    assert res.prob_positive > 80.0
    assert res.ci_95_lower < 0.0
    assert res.ci_95_upper > 5.0
