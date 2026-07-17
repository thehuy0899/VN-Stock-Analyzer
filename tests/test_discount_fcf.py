import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.dcf_engine import (
    project_revenue,
    project_ebit,
    project_nopat,
    project_fcf,
    discount_fcfs,
)

revenues = project_revenue(100000, 0.15)
ebits = project_ebit(revenues, 0.25)
nopats = project_nopat(ebits, 0.20)

fcfs = project_fcf(
    nopats,
    revenues,
    capex_percent=0.05,
    nwc_percent=0.02,
)

discounted = discount_fcfs(
    fcfs,
    wacc=0.12,
)

print(discounted)
print(sum(discounted))