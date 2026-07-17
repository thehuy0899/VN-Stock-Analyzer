from core.business import Business


LEVEL_SCORE = {
    "High": 100,
    "Medium": 70,
    "Low": 40,
}


def calculate_business_score(
    business: Business,
) -> int:

    score = 0

    if business.business_model:
        score += 100

    if business.customer:
        score += 100

    if business.core_product:
        score += 100

    if business.growth_driver:
        score += 100

    score += LEVEL_SCORE.get(
        business.pricing_power,
        0,
    )

    score += LEVEL_SCORE.get(
        business.switching_cost,
        0,
    )

    score += LEVEL_SCORE.get(
        business.network_effect,
        0,
    )

    score += LEVEL_SCORE.get(
        business.economies_of_scale,
        0,
    )

    score += LEVEL_SCORE.get(
        business.brand_strength,
        0,
    )

    return round(score / 9)