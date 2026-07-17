import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from services.financial_service import FinancialService

financial = FinancialService.get_financial("FPT")

print(financial)