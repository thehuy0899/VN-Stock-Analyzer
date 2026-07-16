import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.industry_engine import load_industry

print(load_industry("HPG"))
print(load_industry("FPT"))