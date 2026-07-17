from analysis_pipeline import (
    run_analysis_for_symbol,
)

from services.business_service import (
    BusinessService,
)

from services.industry_service import (
    IndustryService,
)

from services.moat_service import (
    MoatService,
)

from services.management_service import (
    ManagementService,
)

from engines.valuation_engine import load_valuation
from report_engine import generate_report
from core.investment_data import InvestmentData


def run_investment_pipeline(
    ticker: str,
):
    financial = run_analysis_for_symbol(
        ticker
    )

    business = (
        BusinessService.get_business(
            ticker
        )
    )

    industry = (
        IndustryService.get_industry(
            ticker
        )
    )

    moat = (
        MoatService.get_moat(
            ticker
        )
    )

    management = (
        ManagementService.get_management(
            ticker
        )
    )

    valuation = load_valuation(
        price=120000,
        eps=6000,
        book_value=30000,
    )

    data = InvestmentData(
        financial=financial,
        business=business,
        industry=industry,
        moat=moat,
        management=management,
        valuation=valuation,
    )

    report = generate_report(
        data
    )
    return report