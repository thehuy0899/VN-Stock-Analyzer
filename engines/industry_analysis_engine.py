from core.industry import Industry
from core.engine_result import EngineResult

from engines.industry_score_engine import (
    calculate_industry_score,
)


def analyze_industry(
    industry: Industry,
) -> EngineResult:

    score = calculate_industry_score(
        industry
    )

    strengths = []
    weaknesses = []

    if industry.growth == "High":
        strengths.append(
            "Ngành có tăng trưởng cao"
        )

    if industry.entry_barrier == "High":
        strengths.append(
            "Rào cản gia nhập cao"
        )

    if industry.cyclical == "High":
        weaknesses.append(
            "Ngành có tính chu kỳ cao"
        )

    return EngineResult(
        score=score,
        confidence=1.0,
        summary=f"Industry Score: {score}/100",
        strengths=strengths,
        weaknesses=weaknesses,
        evidence=[],
        recommendation="",
        metadata={
            "industry": industry.industry,
        },
    )