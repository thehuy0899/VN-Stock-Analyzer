import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.management_engine import (
    load_management,
)

print(load_management("HPG"))
print(load_management("FPT"))