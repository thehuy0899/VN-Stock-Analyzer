from core.moat import Moat


LEVEL_SCORE = {
    "High": 100,
    "Medium": 70,
    "Low": 40,
}


def calculate_moat_score(
    moat: Moat,
) -> int:

    score = 0

    score += LEVEL_SCORE.get(
        moat.switching_cost,
        0,
    )

    score += LEVEL_SCORE.get(
        moat.network_effect,
        0,
    )

    score += LEVEL_SCORE.get(
        moat.brand,
        0,
    )

    score += LEVEL_SCORE.get(
        moat.cost_advantage,
        0,
    )

    score += LEVEL_SCORE.get(
        moat.intangible_assets,
        0,
    )

    return round(score / 5)