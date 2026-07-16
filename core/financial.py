from dataclasses import dataclass


@dataclass
class Financial:

    revenue: float = 0

    profit: float = 0

    operating_cashflow: float = 0

    free_cashflow: float = 0

    roe: float = 0

    roic: float = 0