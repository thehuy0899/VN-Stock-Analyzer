def classify(score: float) -> str:
    if score is None:
        return "Unknown"

    if score > -1.78:
        return "High Risk"

    if score > -2.22:
        return "Watch"

    return "Low Risk"