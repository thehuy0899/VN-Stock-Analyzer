from dataclasses import dataclass


@dataclass
class DCFInput:
    revenue: float
    revenue_growth: float
    operating_margin: float
    tax_rate: float
    capex_percent: float
    nwc_percent: float
    wacc: float
    terminal_growth: float
    shares_outstanding: float
    net_debt: float