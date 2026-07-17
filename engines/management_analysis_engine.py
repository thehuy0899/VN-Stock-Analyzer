from core.engine_result import EngineResult
from core.management import Management

from engines.management_score_engine import (
    calculate_management_score,
)


def analyze_management(
    management: Management,
) -> EngineResult:

    score = calculate_management_score(
        management
    )

    strengths = []
    weaknesses = []

    if management.founder_led:
        strengths.append(
            "Founder-led"
        )

    if management.capital_allocation == "High":
        strengths.append(
            "Phân bổ vốn hiệu quả"
        )

    if management.execution == "High":
        strengths.append(
            "Khả năng thực thi tốt"
        )

    if management.transparency == "Low":
        weaknesses.append(
            "Minh bạch thấp"
        )

    return EngineResult(
        score=score,
        confidence=1.0,
        summary=f"Management Score: {score}/100",
        strengths=strengths,
        weaknesses=weaknesses,
        evidence=[],
        recommendation="",
        metadata={
            "founder_led": management.founder_led,
        },
    )