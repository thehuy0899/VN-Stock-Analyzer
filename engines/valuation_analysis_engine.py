from core.engine_result import EngineResult
from core.valuation import Valuation

from engines.valuation_score_engine import (
    calculate_valuation_score,
)


def analyze_valuation(
    valuation: Valuation,
) -> EngineResult:

    score = calculate_valuation_score(
        valuation
    )

    strengths = []
    weaknesses = []

    if valuation.pe <= 15:
        strengths.append(
            "P/E hấp dẫn"
        )

    if valuation.pb <= 2:
        strengths.append(
            "P/B hấp dẫn"
        )

    if valuation.pe > 25:
        weaknesses.append(
            "P/E cao"
        )

    if valuation.pb > 5:
        weaknesses.append(
            "P/B cao"
        )

    return EngineResult(
        score=score,
        confidence=1.0,
        summary=f"Valuation Score: {score}/100",
        strengths=strengths,
        weaknesses=weaknesses,
        evidence=[],
        recommendation="",
        metadata={
            "pe": valuation.pe,
            "pb": valuation.pb,
        },
    )