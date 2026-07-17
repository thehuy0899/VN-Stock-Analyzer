from dataclasses import dataclass


@dataclass
class Company:
    ticker: str
    name: str
    exchange: str
    sector: str
    industry: str
    market_cap: float
    shares_outstanding: float