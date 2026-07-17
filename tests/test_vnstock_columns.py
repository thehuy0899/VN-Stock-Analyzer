import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from datasources.vnstock_datasource import VNStockDataSource

raw = VNStockDataSource.financial("FPT")

print("===== INCOME =====")
print(raw["income"].head(30))

print("\n===== BALANCE =====")
print(raw["balance"].head(30))

print("\n===== CASHFLOW =====")
print(raw["cashflow"].head(30))