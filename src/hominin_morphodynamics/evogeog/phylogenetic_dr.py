"""Hominin phylogenetic Tip DR auditing and OLS regression (Tier 1 Forensics).

Delegates pure Newick parsing and Jetz et al. (2012) Tip DR math to
``phosphene.holonomy.macroevo``, keeping disk I/O (Pull) and hominin-specific
outgroup filtering / OLS regression cleanly in ``hominin-morphodynamics``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
from scipy import stats

from phosphene.holonomy.macroevo import (
    newick_tip_paths,
    tip_dr,
    tip_dr_diagnostic,
)


def load_tree_paths_from_file(tree_path: Path) -> Dict[str, List[float]]:
    """Pull an external Newick tree file and extract tip-to-root branch length sequences."""
    content = tree_path.read_text().strip()
    return {taxon: list(lengths) for taxon, lengths in newick_tip_paths(content).items()}


@dataclass(frozen=True)
class TipDRAuditRecord:
    species_name: str
    is_homo: bool
    terminal_branch_ma: float
    tip_dr_regularized: float
    tip_dr_raw: float
    has_polytomy_artifact: bool


def audit_phylogenetic_tree_tips(
    tree_path_or_dict: Path | Dict[str, List[float]],
    regularization_floor: float = 1e-4,
    outgroups: Sequence[str] = ("Gorilla_gorilla", "Pan_troglodytes"),
) -> list[TipDRAuditRecord]:
    """Calculate regularized vs raw Jetz (2012) Tip DR for all ingroup tips in a phylogeny."""
    if isinstance(tree_path_or_dict, Path):
        tip_paths = load_tree_paths_from_file(tree_path_or_dict)
    else:
        tip_paths = tree_path_or_dict

    records: list[TipDRAuditRecord] = []
    for name, path in tip_paths.items():
        if name in outgroups:
            continue

        diag = tip_dr_diagnostic(
            path,
            min_branch_length=regularization_floor,
            singularity_threshold=1e-6,
        )
        dr_raw = tip_dr(path, min_branch_length=1e-15)

        records.append(
            TipDRAuditRecord(
                species_name=name,
                is_homo=name.startswith("Homo"),
                terminal_branch_ma=round(diag.terminal_branch_length, 4),
                tip_dr_regularized=round(diag.diversification_rate, 4),
                tip_dr_raw=round(dr_raw, 2),
                has_polytomy_artifact=diag.has_singularity,
            )
        )

    records.sort(key=lambda r: r.tip_dr_regularized, reverse=True)
    return records


@dataclass(frozen=True)
class RegressionAuditResult:
    model_name: str
    num_observations: int
    r_squared: float
    slope: float
    intercept: float
    p_value: float
    std_err: float
    is_significant: bool


def run_ols_dr_regression(
    records: Sequence[TipDRAuditRecord],
    diversity_vector: Sequence[float],
) -> RegressionAuditResult:
    """Run regression of Tip DR on standing diversity."""
    dr_vals = np.array([r.tip_dr_regularized for r in records])
    div_vals = np.array(diversity_vector)

    slope, intercept, r_val, p_val, std_err = stats.linregress(div_vals, dr_vals)

    return RegressionAuditResult(
        model_name="DR ~ Diversity",
        num_observations=len(records),
        r_squared=round(r_val**2, 4),
        slope=round(slope, 4),
        intercept=round(intercept, 4),
        p_value=round(p_val, 4),
        std_err=round(std_err, 4),
        is_significant=(p_val < 0.05),
    )
