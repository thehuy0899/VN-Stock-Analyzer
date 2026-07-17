import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from investment_pipeline import (
    run_investment_pipeline,
)

result = run_investment_pipeline(
    "FPT"
)

print(result.keys())