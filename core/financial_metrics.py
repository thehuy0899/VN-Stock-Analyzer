from dataclasses import dataclass


@dataclass
class FinancialMetrics:
    roa: float
    prev_roa: float

    cfo: float
    net_income: float

    long_term_debt: float
    prev_long_term_debt: float

    current_ratio: float
    prev_current_ratio: float

    shares: float
    prev_shares: float

    gross_margin: float
    prev_gross_margin: float

    asset_turnover: float
    prev_asset_turnover: float