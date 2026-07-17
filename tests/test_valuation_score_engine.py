import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.valuation_engine import (
    load_valuation,
)

from engines.valuation_score_engine import (
    calculate_valuation_score,
)

valuation = load_valuation(
    price=120000,
    eps=6000,
    book_value=30000,
)

print(
    calculate_valuation_score(
        valuation
    )
)