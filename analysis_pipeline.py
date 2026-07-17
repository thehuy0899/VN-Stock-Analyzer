
print("Loaded:", __file__)
from financial_data_loader import (
    load_financial_data,
)

from analysis_engine import (
    analyze_margin,
    analyze_growth,
)

from engines.growth_quality_engine import (
    analyze_growth_quality,
)

from engines.earnings_driver_engine import (
    analyze_earnings_drivers,
)

from engines.balance_sheet_engine import (
    analyze_balance_sheet,
)

from engines.cashflow_engine import (
    analyze_cashflow,
)

from engines.cashflow_trend_engine import (
    analyze_cashflow_trend,
)

from engines.capital_efficiency_engine import (
    analyze_capital_efficiency,
)

from engines.capital_allocation_engine import (
    analyze_capital_allocation,
)

from engines.debt_service_engine import (
    analyze_debt_service,
)

from cross_analysis import (
    analyze_cross_signals,
)

from engines.financial_cross_engine import (
    analyze_financial_cross,
)

from financial_health import (
    calculate_financial_health,
)

from final_analysis import (
    generate_final_analysis,
)

from engines.decision_engine import (
    make_decision,
)

from engines.piotroski_engine import analyze as analyze_piotroski
from engines.altman_engine import analyze as analyze_altman
from engines.altman_score_engine import classify as classify_altman

# ============================================================
# ANALYSIS PIPELINE
# ============================================================

"""
Main Financial Analysis Pipeline

Flow:

1. Profitability
2. Growth
3. Cashflow
4. Balance Sheet
5. Capital
6. Debt
7. Cross Analysis
8. Financial Health
9. Final Analysis
"""

def run_analysis_pipeline(
    income,
    balance_sheet,
    cashflow,
):
    
    print("===== BALANCE ITEM IDs =====")
    print(balance_sheet["item_id"].tolist())

    print("\n===== INCOME ITEM IDs =====")
    print(income["item_id"].tolist())


    # ==============================
    # MARGIN
    # ==============================

    margin_result = analyze_margin(
        income
    )

    # ==============================
    # GROWTH
    # ==============================

    growth_result = analyze_growth(
        income
    )

    # ==============================
    # GROWTH QUALITY
    # ==============================

    growth_quality_result = (
        analyze_growth_quality(
            growth_result,
            margin_result,
        )
    )

    # ==============================
    # EARNINGS DRIVER
    # ==============================

    earnings_driver_result = (
        analyze_earnings_drivers(
            income,
            margin_result,
            growth_result,
        )
    )

    # ==============================
    # BALANCE SHEET
    # ==============================

    balance_result = (
        analyze_balance_sheet(
            balance_sheet
        )
    )


    piotroski_result = analyze_piotroski(
        income,
        balance_sheet,
        cashflow,
    )

    from engines.piotroski_score_engine import classify

    piotroski_result["level"] = classify(
        piotroski_result["score"]
    )

    print(piotroski_result)

    altman_result = analyze_altman(
        income,
        balance_sheet,
    )

    if altman_result["status"] == "success":
        altman_result["level"] = classify_altman(
            altman_result["score"]
        )

    print(altman_result)

    # ==============================
    # CASHFLOW
    # ==============================

    cashflow_result = analyze_cashflow(
        cashflow,
        growth_result,
    )

    # ==============================
    # CASHFLOW TREND
    # ==============================

    cashflow_trend_result = analyze_cashflow_trend(
        cashflow,
    )

    # ==============================
    # CAPITAL EFFICIENCY
    # ==============================

    capital_efficiency_result = analyze_capital_efficiency(
        income,
        balance_sheet,
    )

    # ==============================
    # CAPITAL ALLOCATION
    # ==============================

    capital_allocation_result = analyze_capital_allocation(
        capital_efficiency_result,
    )
    # ==============================
    # DEBT SERVICE
    # ==============================

    debt_service_result = analyze_debt_service(
        income,
        balance_sheet,
        cashflow_result,
    )


    # ==============================
    # CROSS ANALYSIS
    # ==============================

    cross_result = analyze_cross_signals(
        margin_result,
        growth_result,
    )

    # ==============================
    # FINANCIAL CROSS
    # ==============================

    financial_cross_result = analyze_financial_cross(
        cashflow_result,
        balance_result,
        cashflow_trend_result,
        capital_efficiency_result,
        capital_allocation_result,
        debt_service_result,
    )

    # ==============================
    # FINANCIAL HEALTH
    # ==============================

    health_result = calculate_financial_health(
        margin_result,
        growth_result,
        cross_result,
        cashflow_result,
        financial_cross_result,
        balance_result,
        piotroski_result,
        altman_result,
    )

    decision_result = make_decision(
        health_result["score"],
        health_result["score"],
        piotroski_result["score"],
    )

    # ==============================
    # FINAL ANALYSIS
    # ==============================

    final_analysis_result = generate_final_analysis(
        margin_result,
        growth_result,
        cross_result,
        health_result,
        cashflow_result,
        balance_result,
        financial_cross_result,
        growth_quality_result,
        earnings_driver_result,
        capital_efficiency_result,
        capital_allocation_result,
    )

    # ==============================
    # RETURN
    # ==============================

    return {
        "margin": margin_result,
        "growth": growth_result,
        "growth_quality": (
            growth_quality_result
        ),
        "earnings_driver": (
            earnings_driver_result
        ),
        "balance": balance_result,
        "cashflow": cashflow_result,
        "cashflow_trend": (
            cashflow_trend_result
        ),
        "capital_efficiency": (
            capital_efficiency_result
        ),
        "capital_allocation": (
            capital_allocation_result
        ),
        "debt_service": (
            debt_service_result
        ),
        "cross": cross_result,
        "financial_cross": (
            financial_cross_result
        ),
        "health": health_result,
        "final_analysis": (
            final_analysis_result
        ),
        "decision": decision_result,
        "piotroski": piotroski_result,
        "altman": altman_result,
    }


# ============================================================
# SYMBOL ANALYSIS WRAPPER
# ============================================================


def run_analysis_for_symbol(
    symbol,
):
    financial_data = (
        load_financial_data(
            symbol
        )
    )

    return run_analysis_pipeline(
        financial_data["income"],
        financial_data[
            "balance_sheet"
        ],
        financial_data["cashflow"],
    )