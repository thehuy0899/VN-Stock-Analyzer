from core.industry import Industry


LEVEL_SCORE = {
    "High": 100,
    "Medium": 70,
    "Low": 40,
}


def calculate_industry_score(
    industry: Industry,
) -> int:

    score = 0

    score += LEVEL_SCORE.get(
        industry.growth,
        0,
    )

    score += LEVEL_SCORE.get(
        industry.entry_barrier,
        0,
    )

    score += (
        100
        - LEVEL_SCORE.get(
            industry.cyclical,
            0,
        )
    )

    return round(score / 3)