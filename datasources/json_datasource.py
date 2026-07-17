from datasources.base_datasource import BaseDataSource
from data.loader import load_json


class JsonDataSource(BaseDataSource):

    @staticmethod
    def company(ticker: str):
        return load_json(ticker, "company.json")

    @staticmethod
    def financial(ticker: str):
        return load_json(ticker, "financial.json")

    @staticmethod
    def business(ticker: str):
        return load_json(ticker, "business.json")

    @staticmethod
    def industry(ticker: str):
        return load_json(ticker, "industry.json")

    @staticmethod
    def moat(ticker: str):
        return load_json(ticker, "moat.json")

    @staticmethod
    def management(ticker: str):
        return load_json(ticker, "management.json")