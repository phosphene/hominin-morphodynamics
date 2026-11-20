"""Cross-domain comparative metrics extractor.

Re-exports and delegates to phosphene.holonomy.macroevo.comparative_metrics.
"""

from __future__ import annotations

from phosphene.holonomy.macroevo.comparative_metrics import (
    DomainComparisonReport,
    generate_canonical_comparison,
)

__all__ = [
    "DomainComparisonReport",
    "generate_canonical_comparison",
]
