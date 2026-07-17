import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from core.business import Business

from engines.business_engine import (
    analyze_business,
)

business = Business(
    business_model="IT Services",
    customer=["Enterprise"],
    core_product=["Software"],
    growth_driver=["AI"],
    threat=["Competition"],
    pricing_power="High",
    switching_cost="High",
    network_effect="Low",
    economies_of_scale="High",
    brand_strength="High",
)

print(
    analyze_business(
        business
    )
)