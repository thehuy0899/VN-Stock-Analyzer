from dataclasses import dataclass


@dataclass
class Valuation:
    pe: float
    pb: float
    eps: float
    book_value: float
    price: float