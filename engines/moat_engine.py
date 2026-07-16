import json
from pathlib import Path

from core.moat import Moat


def load_moat(
    ticker: str,
) -> Moat | None:

    path = (
        Path("knowledge")
        / ticker.upper()
        / "moat.json"
    )

    if not path.exists():
        return None

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    return Moat(
        switching_cost=data.get(
            "switching_cost",
            "",
        ),
        network_effect=data.get(
            "network_effect",
            "",
        ),
        brand=data.get(
            "brand",
            "",
        ),
        cost_advantage=data.get(
            "cost_advantage",
            "",
        ),
        intangible_assets=data.get(
            "intangible_assets",
            "",
        ),
    )