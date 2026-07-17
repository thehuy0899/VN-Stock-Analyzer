from engines.business_engine import analyze_business
from engines.industry_analysis_engine import analyze_industry
from engines.moat_analysis_engine import analyze_moat
from engines.management_analysis_engine import analyze_management
from engines.valuation_analysis_engine import analyze_valuation

from config.scoring import SCORING_WEIGHTS
from core.investment_data import InvestmentData


def generate_report(data: InvestmentData):

    business_result = analyze_business(data.business)
    industry_result = analyze_industry(data.industry)
    moat_result = analyze_moat(data.moat)
    management_result = analyze_management(data.management)
    valuation_result = analyze_valuation(data.valuation)

    investment_score = round(
        data.financial["health"]["score"] * SCORING_WEIGHTS["financial"]
        + business_result.score * SCORING_WEIGHTS["business"]
        + industry_result.score * SCORING_WEIGHTS["industry"]
        + moat_result.score * SCORING_WEIGHTS["moat"]
        + management_result.score * SCORING_WEIGHTS["management"]
        + valuation_result.score * SCORING_WEIGHTS["valuation"]
    )

    if investment_score >= 85:
        recommendation = "STRONG BUY"
    elif investment_score >= 70:
        recommendation = "BUY"
    elif investment_score >= 55:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    return {
        "financial_score": data.financial["health"]["score"],
        "business_score": business_result.score,
        "industry_score": industry_result.score,
        "moat_score": moat_result.score,
        "management_score": management_result.score,
        "valuation_score": valuation_result.score,
        "investment_score": investment_score,
        "recommendation": recommendation,
    }