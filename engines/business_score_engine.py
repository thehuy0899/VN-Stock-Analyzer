from core.business import Business


def calculate_business_score(
    business: Business,
):
    score = 0

    details = []

    if business.business_model:
        score += 15
        details.append(
            "✔ Business Model (+15)"
        )

    if business.core_product:
        score += 10
        details.append(
            "✔ Core Product (+10)"
        )

    if business.customer:
        score += 10
        details.append(
            "✔ Customer (+10)"
        )

    if business.growth_driver:
        score += 15
        details.append(
            "✔ Growth Driver (+15)"
        )

    if business.pricing_power:
        score += 15
        details.append(
            "✔ Pricing Power (+15)"
        )

    if business.economies_of_scale:
        score += 15
        details.append(
            "✔ Economies of Scale (+15)"
        )

    if business.brand_strength:
        score += 10
        details.append(
            "✔ Brand Strength (+10)"
        )

    if business.switching_cost:
        score += 5
        details.append(
            "✔ Switching Cost (+5)"
        )

    if business.network_effect:
        score += 5
        details.append(
            "✔ Network Effect (+5)"
        )

    if business.threat:
        score += 10
        details.append(
            "✔ Threat Analysis (+10)"
        )

    return {
        "score": score,
        "details": details,
    }