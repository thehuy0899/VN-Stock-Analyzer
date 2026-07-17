import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from investment_pipeline import (
    run_investment_pipeline,
)

from report_engine import (
    generate_report,
)

data = run_investment_pipeline(
    "FPT"
)

report = generate_report(
    data["financial"],
    data["business"],
    data["industry"],
    data["moat"],
    data["management"],
)

print(report)