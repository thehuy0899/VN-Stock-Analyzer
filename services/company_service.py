from core.company import Company
from datasources.json_datasource import JsonDataSource


class CompanyService:

    @staticmethod
    def get_company(
        ticker: str,
    ):

        data = JsonDataSource.company(ticker)

        return Company(
            ticker=data["ticker"],
            name=data["name"],
            exchange=data["exchange"],
            sector=data["sector"],
            industry=data["industry"],
            market_cap=data["market_cap"],
            shares_outstanding=data["shares_outstanding"],
        )