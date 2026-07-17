from datasources.vnstock_datasource import VNStockDataSource
from mappers.financial_mapper import FinancialMapper


class FinancialService:

    @staticmethod
    def get_financial(ticker: str):

        raw = VNStockDataSource.financial(ticker)

        return FinancialMapper.from_vnstock(raw)