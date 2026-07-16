import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.industry_engine import load_industry
from engines.industry_score_engine import (
    calculate_industry_score,
)

industry = load_industry("HPG")

print(
    calculate_industry_score(
        industry
    )
)

industry = load_industry("FPT")

print(
    calculate_industry_score(
        industry
    )
)