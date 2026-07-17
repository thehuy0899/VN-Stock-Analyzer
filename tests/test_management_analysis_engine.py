import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.management_engine import (
    load_management,
)

from engines.management_analysis_engine import (
    analyze_management,
)

print(
    analyze_management(
        load_management("HPG")
    )
)

print(
    analyze_management(
        load_management("FPT")
    )
)