import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from datasources.json_datasource import JsonDataSource
from mappers.financial_mapper import FinancialMapper

raw = JsonDataSource.financial(
    "FPT"
)

financial = FinancialMapper.from_json(
    raw
)

print(financial)