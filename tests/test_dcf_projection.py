import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.dcf_engine import (
    project_revenue,
    project_ebit,
    project_nopat,
)

revenues = project_revenue(
    revenue=100000,
    growth=0.15,
)

ebits = project_ebit(
    revenues,
    operating_margin=0.25,
)

nopats = project_nopat(
    ebits,
    tax_rate=0.20,
)

print("Revenue")
print(revenues)

print()

print("EBIT")
print(ebits)

print()

print("NOPAT")
print(nopats)