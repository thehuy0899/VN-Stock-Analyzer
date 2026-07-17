import json
from pathlib import Path

from core.management import Management


def load_management(
    ticker: str,
) -> Management | None:

    path = (
        Path("knowledge")
        / ticker.upper()
        / "management.json"
    )

    if not path.exists():
        return None

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    return Management(
        founder_led=data.get(
            "founder_led",
            False,
        ),
        capital_allocation=data.get(
            "capital_allocation",
            "",
        ),
        execution=data.get(
            "execution",
            "",
        ),
        transparency=data.get(
            "transparency",
            "",
        ),
        insider_ownership=data.get(
            "insider_ownership",
            "",
        ),
    )