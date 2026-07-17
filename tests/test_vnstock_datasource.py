import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from datasources.vnstock_datasource import VNStockDataSource

data = VNStockDataSource.financial("FPT")

print(data.keys())

print(data["income"].head())

print(data["balance"].head())

print(data["cashflow"].head())