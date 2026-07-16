from core.business import Business
from business_score_engine import (
    calculate_business_score,
)
from core.engine_result import EngineResult


def analyze_business(
    business: Business,
) -> EngineResult:

    strengths = []
    weaknesses = []

    if business.business_model:
        strengths.append(
            "Có mô hình kinh doanh rõ ràng"
        )

    else:
        weaknesses.append(
            "Chưa xác định mô hình kinh doanh"
        )

    if business.customer:
        strengths.append(
            "Đã xác định khách hàng mục tiêu"
        )

    else:
        weaknesses.append(
            "Chưa xác định khách hàng"
        )
    
    score_result = calculate_business_score(
        business
    )

    return EngineResult(
        score=score_result["score"],
        confidence=1.0,
        summary=f"Business Score: {score_result['score']}/100",
        strengths=strengths,
        weaknesses=weaknesses,
        evidence=score_result["details"],
        recommendation="",
        metadata={
            "business_model": business.business_model,
            "customer": business.customer,
        },
    )