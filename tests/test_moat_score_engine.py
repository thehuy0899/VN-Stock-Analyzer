import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.moat_engine import load_moat
from engines.moat_score_engine import (
    calculate_moat_score,
)

print(
    calculate_moat_score(
        load_moat("HPG")
    )
)

print(
    calculate_moat_score(
        load_moat("FPT")
    )
)