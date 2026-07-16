import json
from pathlib import Path

from core.industry import Industry


def load_industry(
    ticker: str,
) -> Industry | None:

    path = (
        Path("knowledge")
        / ticker.upper()
        / "industry.json"
    )

    if not path.exists():
        return None

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    return Industry(
        industry=data.get(
            "industry",
            "",
        ),
        growth=data.get(
            "growth",
            "",
        ),
        cyclical=data.get(
            "cyclical",
            "",
        ),
        competition=data.get(
            "competition",
            "",
        ),
        entry_barrier=data.get(
            "entry_barrier",
            "",
        ),
        long_term_outlook=data.get(
            "long_term_outlook",
            "",
        ),
    )