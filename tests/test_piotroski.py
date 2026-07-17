import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.piotroski_engine import analyze

result = analyze(None)

print(result)