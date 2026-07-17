import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.dcf_engine import *

revenues = project_revenue(100000, 0.15)

ebits = project_ebit(
    revenues,
    0.25,
)

nopats = project_nopat(
    ebits,
    0.20,
)

fcfs = project_fcf(
    nopats,
    revenues,
    0.05,
    0.02,
)

discounted = discount_fcfs(
    fcfs,
    0.12,
)

tv = terminal_value(
    fcfs[-1],
    0.12,
    0.03,
)

pv_tv = discount_terminal_value(
    tv,
    0.12,
    5,
)

ev = enterprise_value(
    discounted,
    pv_tv,
)

equity = equity_value(
    ev,
    10000,
)

intrinsic = intrinsic_value_per_share(
    equity,
    1000,
)

print(f"Enterprise Value : {ev:,.2f}")
print(f"Equity Value     : {equity:,.2f}")
print(f"Intrinsic/Share  : {intrinsic:,.2f}")