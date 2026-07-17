import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from config.financial_scoring import FINANCIAL_SCORE

total = sum(
    item["weight"]
    for item in FINANCIAL_SCORE.values()
)

print(total)