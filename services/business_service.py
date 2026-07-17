from core.business import Business
from datasources.json_datasource import JsonDataSource


class BusinessService:

    @staticmethod
    def get_business(
        ticker: str,
    ) -> Business:

        data = JsonDataSource.business(ticker)

        return Business(
            business_model=data["business_model"],
            customer=data["customer"],
            core_product=data["core_product"],
            growth_driver=data["growth_driver"],
            threat=data["threat"],
            pricing_power=data["pricing_power"],
            switching_cost=data["switching_cost"],
            network_effect=data["network_effect"],
            economies_of_scale=data["economies_of_scale"],
            brand_strength=data["brand_strength"],
        )