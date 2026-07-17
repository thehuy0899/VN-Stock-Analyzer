from core.decision import Decision


def make_decision(
    business_score: int,
    financial_score: int,
    piotroski_score: int = None,
):
    score = (
        business_score +
        financial_score
    ) // 2

    if piotroski_score is not None:

        if piotroski_score >= 8:
            score += 3

        elif piotroski_score >= 6:
            score += 2

        elif piotroski_score <= 2:
            score -= 3

            score = max(
                0,
                min(score, 100),
            )

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