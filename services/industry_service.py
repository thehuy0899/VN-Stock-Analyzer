from core.industry import Industry
from datasources.json_datasource import JsonDataSource


class IndustryService:

    @staticmethod
    def get_industry(
        ticker: str,
    ) -> Industry:

        data = JsonDataSource.industry(ticker)

        return Industry(
            industry=data["industry"],
            growth=data["growth"],
            cyclical=data["cyclical"],
            competition=data["competition"],
            entry_barrier=data["entry_barrier"],
            long_term_outlook=data["long_term_outlook"],
        )