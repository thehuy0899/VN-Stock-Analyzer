LEVEL_SCORE = {
    "Excellent": 100,
    "High": 80,
    "Medium": 60,
    "Low": 40,
    "None": 0,
}


def score_level(level: str) -> int:
    return LEVEL_SCORE.get(level, 0)