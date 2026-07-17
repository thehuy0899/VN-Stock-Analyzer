from core.management import Management


LEVEL_SCORE = {
    "High": 100,
    "Medium": 70,
    "Low": 40,
}


def calculate_management_score(
    management: Management,
) -> int:

    score = 0

    score += 100 if management.founder_led else 50

    score += LEVEL_SCORE.get(
        management.capital_allocation,
        0,
    )

    score += LEVEL_SCORE.get(
        management.execution,
        0,
    )

    score += LEVEL_SCORE.get(
        management.transparency,
        0,
    )

    score += LEVEL_SCORE.get(
        management.insider_ownership,
        0,
    )

    return round(score / 5)