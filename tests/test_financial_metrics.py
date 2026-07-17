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

print("Revenue :", m.revenue())
print("Profit :", m.net_profit())
print("Operating CF :", m.operating_cf())
print("CAPEX :", m.capex())
print("Free CF :", m.free_cashflow())