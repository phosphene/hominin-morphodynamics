"""Tree parsing, path extraction, and Tip Diversification Rate (DR) auditing.

Replicates and audits the phylogenetic diversification analyses in Van Holstein & Foley (2024)
based on the Parins-Fukuchi et al. (2019) hominin tree.

Engineering & Methodological Contracts:
1. Dynamic Newick parsing: no hardcoded tree literals or ad-hoc branch path dictionaries.
2. Clean separation of external artifacts: trees are ingested as external files/fixtures.
3. Numerical singularity diagnostics: explicitly detects and exposes polytomy machine-epsilon
   artifacts (< 1e-6 Myr / picoseconds) that cause Jetz et al. (2012) tip DR to explode to 10^11.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
from scipy import stats

from hominin_morphodynamics.inference.primitives import tip_diversification_rate


@dataclass
class PhyloNode:
    """Minimal typed node representing an unrooted or rooted phylogenetic tree."""

    name: Optional[str] = None
    branch_length: float = 0.0
    children: List[PhyloNode] = field(default_factory=list)
    parent: Optional[PhyloNode] = None


def parse_newick(newick_str: str) -> PhyloNode:
    """Parse standard Newick string into a PhyloNode hierarchy.

    Supports internal node labels and branch lengths: (A:1.0,(B:2.0)C:1.5):0.0;
    """
    s = newick_str.strip()
    if s.endswith(";"):
        s = s[:-1]

    tokens: list[str] = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in "(),:;":
            tokens.append(c)
            i += 1
        elif c.isspace():
            i += 1
        else:
            j = i
            while j < n and s[j] not in "(),:; \t\r\n":
                j += 1
            tokens.append(s[i:j])
            i = j

    curr = PhyloNode()
    root = curr
    idx, num_tokens = 0, len(tokens)
    while idx < num_tokens:
        tok = tokens[idx]
        if tok == ";":
            idx += 1
            break
        elif tok == "(":
            child = PhyloNode(parent=curr)
            curr.children.append(child)
            curr = child
            idx += 1
        elif tok == ",":
            curr = curr.parent
            child = PhyloNode(parent=curr)
            curr.children.append(child)
            curr = child
            idx += 1
        elif tok == ")":
            curr = curr.parent
            idx += 1
            if idx < num_tokens and tokens[idx] not in "(),:;":
                curr.name = tokens[idx]
                idx += 1
            if idx < num_tokens and tokens[idx] == ":":
                idx += 1
                curr.branch_length = float(tokens[idx])
                idx += 1
        elif tok == ":":
            idx += 1
            curr.branch_length = float(tokens[idx])
            idx += 1
        else:
            curr.name = tok
            idx += 1

    return root


def extract_tip_paths(
    node: PhyloNode,
    paths: Optional[Dict[str, List[float]]] = None,
    current_path: Optional[List[float]] = None,
) -> Dict[str, List[float]]:
    """Extract sequence of branch lengths from named node up to root [terminal, parent, ...]."""
    if paths is None:
        paths = {}
    if current_path is None:
        current_path = []

    if node.name:
        paths[node.name] = [node.branch_length] + current_path

    for child in node.children:
        child_path = [node.branch_length] + current_path if node.parent is not None else []
        extract_tip_paths(child, paths, child_path)

    return paths


def load_tree_paths_from_file(tree_path: Path) -> Dict[str, List[float]]:
    """Load and parse an external Newick tree file, returning tip-to-root branch length sequences."""
    content = tree_path.read_text().strip()
    root = parse_newick(content)
    return extract_tip_paths(root)


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
    """Calculate regularized vs raw tip DR for all ingroup tips in a phylogeny."""
    if isinstance(tree_path_or_dict, Path):
        tip_paths = load_tree_paths_from_file(tree_path_or_dict)
    else:
        tip_paths = tree_path_or_dict

    records: list[TipDRAuditRecord] = []

    for name, path in tip_paths.items():
        if name in outgroups:
            continue

        is_homo = name.startswith("Homo")
        term_l = path[0]

        # Regularized DR using Primitive 6
        dr_reg = tip_diversification_rate(path, min_branch_length=regularization_floor)

        # Raw DR (unregularized)
        dr_raw = tip_diversification_rate(path, min_branch_length=1e-15)

        has_artifact = any(l < 1e-6 for l in path)

        records.append(
            TipDRAuditRecord(
                species_name=name,
                is_homo=is_homo,
                terminal_branch_ma=round(term_l, 4),
                tip_dr_regularized=round(dr_reg, 4),
                tip_dr_raw=round(dr_raw, 2),
                has_polytomy_artifact=has_artifact,
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
