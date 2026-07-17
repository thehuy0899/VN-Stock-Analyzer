from core.moat import Moat
from datasources.json_datasource import JsonDataSource


class MoatService:

    @staticmethod
    def get_moat(
        ticker: str,
    ) -> Moat:

        data = JsonDataSource.moat(ticker)

        return Moat(
            switching_cost=data["switching_cost"],
            network_effect=data["network_effect"],
            brand=data["brand"],
            cost_advantage=data["cost_advantage"],
            intangible_assets=data["intangible_assets"],
        )