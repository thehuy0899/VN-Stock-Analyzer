import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.dcf_engine import (
    project_revenue,
)

print(
    project_revenue(
        revenue=100000,
        growth=0.15,
    )
)