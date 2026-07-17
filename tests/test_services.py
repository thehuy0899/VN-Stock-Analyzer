import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from services.industry_service import IndustryService
from services.moat_service import MoatService
from services.management_service import (
    ManagementService,
)

print(
    IndustryService.get_industry(
        "FPT"
    )
)

print(
    MoatService.get_moat(
        "FPT"
    )
)

print(
    ManagementService.get_management(
        "FPT"
    )
)