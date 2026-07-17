from core.valuation import Valuation


def calculate_valuation_score(
    valuation: Valuation,
) -> int:

    score = 100

    if valuation.pe > 25:
        score -= 25
    elif valuation.pe > 20:
        score -= 15
    elif valuation.pe > 15:
        score -= 5

    if valuation.pb > 5:
        score -= 25
    elif valuation.pb > 3:
        score -= 15
    elif valuation.pb > 2:
        score -= 5

    return max(score, 0)