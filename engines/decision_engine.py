from core.decision import Decision


def make_decision(
    business_score: int,
    financial_score: int,
):
    score = (
        business_score +
        financial_score
    ) // 2

    if score >= 90:
        recommendation = "Strong Buy"

    elif score >= 80:
        recommendation = "Buy"

    elif score >= 65:
        recommendation = "Watchlist"

    elif score >= 50:
        recommendation = "Avoid"

    else:
        recommendation = "Reject"

    return Decision(
        score=score,
        recommendation=recommendation,
        confidence=1.0,
        risks=[],
        opportunities=[],
    )