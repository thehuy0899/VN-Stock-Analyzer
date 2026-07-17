import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from services.moat_service import (
    MoatService,
)

moat = MoatService.get_moat(
    "FPT"
)

print(moat)