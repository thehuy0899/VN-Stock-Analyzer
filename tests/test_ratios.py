import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from datasources.vnstock_datasource import VNStockDataSource
from metrics.financial_metrics import FinancialMetrics

raw = VNStockDataSource.financial("FPT")

year = raw["income"].columns[-4]

m = FinancialMetrics(
    raw["income"],
    raw["balance"],
    raw["cashflow"],
    year,
)

print("ROE :", round(m.roe() * 100, 2), "%")
print("ROA :", round(m.roa() * 100, 2), "%")