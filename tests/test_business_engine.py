from core.business import Business
from business_engine import analyze_business


business = Business(
    business_model="Integrated Steel",
    customer="Construction Company",
)

result = analyze_business(business)

print(result)