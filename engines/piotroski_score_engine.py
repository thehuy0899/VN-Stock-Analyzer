def classify(score: int):

    if score >= 8:
        return "Excellent"

    if score >= 6:
        return "Good"

    if score >= 4:
        return "Average"

    return "Weak"