from core.engine_result import EngineResult
from core.moat import Moat

from engines.moat_score_engine import (
    calculate_moat_score,
)


def analyze_moat(
    moat: Moat,
) -> EngineResult:

    score = calculate_moat_score(
        moat
    )

    strengths = []
    weaknesses = []

    if moat.brand == "High":
        strengths.append(
            "Thương hiệu mạnh"
        )

    if moat.switching_cost == "High":
        strengths.append(
            "Chi phí chuyển đổi cao"
        )

    if moat.cost_advantage == "High":
        strengths.append(
            "Lợi thế chi phí"
        )

    if moat.network_effect == "Low":
        weaknesses.append(
            "Network Effect yếu"
        )

    return EngineResult(
        score=score,
        confidence=1.0,
        summary=f"Moat Score: {score}/100",
        strengths=strengths,
        weaknesses=weaknesses,
        evidence=[],
        recommendation="",
        metadata={},
    )