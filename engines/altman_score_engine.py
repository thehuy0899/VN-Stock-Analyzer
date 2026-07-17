def classify(score: float) -> str:
    if score is None:
        return "Unknown"

    if score >= 2.99:
        return "Safe"

    if score >= 1.81:
        return "Grey"

    return "Distress"