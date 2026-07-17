import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from datasources.vnstock_datasource import VNStockDataSource

raw = VNStockDataSource.financial("FPT")

balance = raw["balance"]

print(balance[["item", "2025"]].to_string(index=False))