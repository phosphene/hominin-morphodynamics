"""BDD environment configuration for hominin-morphodynamics."""

from __future__ import annotations

from pathlib import Path


def before_all(context):
    """Set up repo root and verify data directories."""
    context.repo_root = Path(__file__).parent.parent.resolve()
    context.data_dir = context.repo_root / "data" / "raw"


def before_scenario(context, scenario):
    """Ensure context isolation for each scenario."""
    context.galapagos_dataset = None
    context.raw_specimens = None
    context.rectified_specimens = None
    context.finches_profile = None
    context.hominin_profile = None
    context.paleodeme_clusters = None
