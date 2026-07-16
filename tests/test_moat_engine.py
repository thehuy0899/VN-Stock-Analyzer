import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.moat_engine import load_moat

print(load_moat("HPG"))
print(load_moat("FPT"))