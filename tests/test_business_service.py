from services.business_service import (
    BusinessService,
)

business = (
    BusinessService.get_business(
        "HPG"
    )
)

print(business)