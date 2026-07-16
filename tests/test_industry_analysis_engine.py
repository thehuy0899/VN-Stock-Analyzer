import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.industry_engine import (
    load_industry,
)

from engines.industry_analysis_engine import (
    analyze_industry,
)

result = analyze_industry(
    load_industry("HPG")
)

print(result)

result = analyze_industry(
    load_industry("FPT")
)

print(result)