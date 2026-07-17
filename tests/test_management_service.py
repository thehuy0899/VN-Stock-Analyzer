import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from services.management_service import (
    ManagementService,
)

management = ManagementService.get_management(
    "FPT"
)

print(management)