"""Forensic parameter audit of diversity-dependence models in hominin diversification.

Audits MCMC posterior chains from PyRate / continuous diversification estimators,
quantifying whether credible intervals on diversity-dependence parameters (Gl)
reliably exclude zero or collapse under taphonomic/sampling skew.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DiversityDependenceAudit:
    config: str
    clade: str
    total_samples: int
    burn_in_samples: int
    analyzed_samples: int
    mean_gl: float
    std_gl: float
    ci_95_lower: float
    ci_95_upper: float
    prob_positive: float
    min_gl: float
    max_gl: float
    spans_zero: bool


def audit_mcmc_log(log_path: Path, burn_in: int = 100) -> DiversityDependenceAudit:
    """Audit single MCMC posterior log file for parameter stability."""
    lines = log_path.read_text().splitlines()
    if not lines:
        raise ValueError(f"Empty log file: {log_path}")

    header = lines[0].split("\t")
    gl_col_idx = None
    for idx, col in enumerate(header):
        if col.startswith("Gl_"):
            gl_col_idx = idx
            break

    if gl_col_idx is None:
        raise KeyError(f"No Gl_* column found in header: {header}")

    data_lines = lines[1:]
    total_samples = len(data_lines)
    post_burn = data_lines[burn_in:]
    analyzed_samples = len(post_burn)

    gl_vals: list[float] = []
    for l in post_burn:
        parts = l.split("\t")
        if len(parts) > gl_col_idx:
            try:
                gl_vals.append(float(parts[gl_col_idx]))
            except ValueError:
                continue

    if not gl_vals:
        raise ValueError(f"No numeric Gl values parsed from {log_path}")

    gl_vals.sort()
    mean_gl = sum(gl_vals) / len(gl_vals)
    variance = sum((x - mean_gl) ** 2 for x in gl_vals) / len(gl_vals)
    std_gl = variance ** 0.5

    lower_idx = int(0.025 * len(gl_vals))
    upper_idx = int(0.975 * len(gl_vals))
    ci_lower = gl_vals[lower_idx]
    ci_upper = gl_vals[upper_idx]

    pos_count = sum(1 for x in gl_vals if x > 0)
    p_pos = pos_count / len(gl_vals)

    clade = "Homo" if "homo" in log_path.name.lower() and "nonhomo" not in log_path.name.lower() else "Non-Homo"
    if "wholeclade" in log_path.name.lower():
        clade = "Whole-Clade"

    config = log_path.parent.parent.name + "_" + log_path.parent.name
    if "Wood-Boyle" in str(log_path):
        config = "Wood-Boyle"

    return DiversityDependenceAudit(
        config=config,
        clade=clade,
        total_samples=total_samples,
        burn_in_samples=burn_in,
        analyzed_samples=analyzed_samples,
        mean_gl=round(mean_gl, 4),
        std_gl=round(std_gl, 4),
        ci_95_lower=round(ci_lower, 4),
        ci_95_upper=round(ci_upper, 4),
        prob_positive=round(p_pos * 100, 2),
        min_gl=round(min(gl_vals), 4),
        max_gl=round(max(gl_vals), 4),
        spans_zero=(ci_lower <= 0 <= ci_upper),
    )


def audit_all_logs(outputs_dir: Path) -> list[DiversityDependenceAudit]:
    """Audit all MCMC logs in an output tree."""
    summaries: list[DiversityDependenceAudit] = []
    for log_file in sorted(outputs_dir.rglob("*.log")):
        if "diversity" in log_file.name or "DD" in log_file.name:
            try:
                summary = audit_mcmc_log(log_file)
                summaries.append(summary)
            except Exception:
                continue
    return summaries
