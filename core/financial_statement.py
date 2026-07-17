from dataclasses import dataclass


@dataclass
class FinancialStatement:
    revenue: float
    gross_profit: float
    operating_income: float
    net_income: float

    total_assets: float
    current_assets: float

    total_liabilities: float
    current_liabilities: float
    long_term_debt: float

    equity: float

    operating_cashflow: float
    free_cashflow: float

    shares_outstanding: float