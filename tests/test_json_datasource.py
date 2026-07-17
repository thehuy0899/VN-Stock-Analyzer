import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from datasources.json_datasource import JsonDataSource

print(JsonDataSource.company("FPT"))
print(JsonDataSource.financial("FPT"))
print(JsonDataSource.business("FPT"))
print(JsonDataSource.industry("FPT"))
print(JsonDataSource.moat("FPT"))
print(JsonDataSource.management("FPT"))