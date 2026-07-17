import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from services.industry_service import (
    IndustryService,
)

industry = IndustryService.get_industry(
    "FPT"
)

print(industry)