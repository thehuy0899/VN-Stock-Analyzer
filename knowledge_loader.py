import json
from pathlib import Path

from core.business import Business


def load_json(
    ticker: str,
    filename: str,
):

    filepath = (
        Path("knowledge")
        / ticker.upper()
        / filename
    )

    if not filepath.exists():
        return None

    with open(
        filepath,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


def load_company_business(
    ticker: str,
):

    data = load_json(
        ticker,
        "business.json",
    )

    if data is None:
        return None

    return Business(
        business_model=data.get(
            "business_model",
            "",
        ),
        customer=", ".join(
            data.get(
                "customer",
                [],
            )
        ),
        core_product=", ".join(
            data.get(
                "core_product",
                [],
            )
        ),
        growth_driver=", ".join(
            data.get(
                "growth_driver",
                [],
            )
        ),
        bottleneck=", ".join(
            data.get(
                "bottleneck",
                [],
            )
        ),
        threat=", ".join(
            data.get(
                "threat",
                [],
            )
        ),
        pricing_power=data.get(
            "pricing_power",
            "",
        ),
        switching_cost=data.get(
            "switching_cost",
            "",
        ),
        network_effect=data.get(
            "network_effect",
            "",
        ),
        economies_of_scale=data.get(
            "economies_of_scale",
            "",
        ),
        brand_strength=data.get(
            "brand_strength",
            "",
        ),
    )