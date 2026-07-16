import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from engines.scoring_engine import score_level

print(score_level("Excellent"))
print(score_level("High"))
print(score_level("Medium"))
print(score_level("Low"))
print(score_level("None"))