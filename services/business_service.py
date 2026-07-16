from core.business import Business
from knowledge_loader import load_company_business


class BusinessService:
    """
    Service xử lý dữ liệu Business.
    """

    @staticmethod
    def get_business(
        ticker: str,
    ) -> Business | None:

        return load_company_business(
            ticker
        )