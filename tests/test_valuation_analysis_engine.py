import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.valuation_engine import (
    load_valuation,
)

from engines.valuation_analysis_engine import (
    analyze_valuation,
)

valuation = load_valuation(
    price=120000,
    eps=6000,
    book_value=30000,
)

print(
    analyze_valuation(
        valuation
    )
)