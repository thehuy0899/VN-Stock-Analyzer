import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from services.company_service import (
    CompanyService,
)

company = CompanyService.get_company(
    "FPT"
)

print(company)
print(company.name)
print(company.exchange)
print(company.market_cap)