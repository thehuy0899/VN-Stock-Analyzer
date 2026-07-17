from core.management import Management
from datasources.json_datasource import JsonDataSource


class ManagementService:

    @staticmethod
    def get_management(
        ticker: str,
    ) -> Management:

        data = JsonDataSource.management(ticker)
        
        return Management(
            founder_led=data["founder_led"],
            capital_allocation=data["capital_allocation"],
            execution=data["execution"],
            transparency=data["transparency"],
            insider_ownership=data["insider_ownership"],
        )