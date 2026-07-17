def calculate_financial_health(
    margin_result,
    growth_result,
    cross_result,
    cashflow_result,
    financial_cross_result,
    balance_result=None,
    piotroski_result=None,
    altman_result=None,
):
    
    # ==============================
    # COLLECT SIGNALS
    # ==============================

    margin_signals = set(
        margin_result.get(
            "signals",
            [],
        )
    )

    growth_signals = set(
        growth_result.get(
            "signals",
            [],
        )
    )

    cross_signals = set(
        cross_result.get(
            "signals",
            [],
        )
    )

    cashflow_signals = set()
    financial_cross_signals = set()
    balance_signals = set()

    if (
        cashflow_result is not None
        and cashflow_result.get("status")
        == "success"
    ):
        cashflow_signals = set(
            cashflow_result.get(
                "signals",
                [],
            )
        )

    if (
        financial_cross_result is not None
        and financial_cross_result.get("status")
        == "success"
    ):
        financial_cross_signals = set(
            financial_cross_result.get(
                "signals",
                [],
            )
        )

    if (
        balance_result is not None
        and balance_result.get("status")
        == "success"
    ):
        balance_signals = set(
            balance_result.get(
                "signals",
                [],
            )
        )

    # ==============================
    # DEBT SERVICE MITIGATION FLAGS
    # ==============================

    strong_debt_service_capacity = (
        "strong_debt_service_capacity"
        in financial_cross_signals
    )

    debt_absorption_improving = (
        "debt_absorption_capacity_improving"
        in financial_cross_signals
    )

    debt_service_resilience = (
        "debt_service_resilience_confirmed"
        in financial_cross_signals
    )

    # ==============================
    # FACTOR SCORES
    # ==============================

    growth_score = 0
    profitability_score = 0
    cash_quality_score = 0
    financial_structure_score = 0

    strengths = []
    warnings = []

    # ==============================
    # 1. GROWTH QUALITY
    # MAX 25
    # ==============================

    revenue_cagr = growth_result.get(
        "revenue_cagr"
    )

    profit_cagr = growth_result.get(
        "profit_cagr"
    )

    revenue_growth = growth_result.get(
        "revenue_growth"
    )

    profit_growth = growth_result.get(
        "profit_growth"
    )

    # ==============================
    # LONG-TERM REVENUE GROWTH
    # ==============================

    if revenue_cagr is not None:
        if revenue_cagr >= 15:
            growth_score += 8

        elif revenue_cagr >= 8:
            growth_score += 6

        elif revenue_cagr >= 3:
            growth_score += 4

        elif revenue_cagr > 0:
            growth_score += 2

    # ==============================
    # LONG-TERM PROFIT GROWTH
    # ==============================

    if profit_cagr is not None:
        if profit_cagr >= 20:
            growth_score += 9

        elif profit_cagr >= 12:
            growth_score += 7

        elif profit_cagr >= 5:
            growth_score += 5

        elif profit_cagr > 0:
            growth_score += 2

    # ==============================
    # RECENT GROWTH MOMENTUM
    # ==============================

    if (
        revenue_growth is not None
        and profit_growth is not None
    ):
        if (
            revenue_growth > 0
            and profit_growth > revenue_growth
        ):
            growth_score += 5

        elif (
            revenue_growth > 0
            and profit_growth > 0
        ):
            growth_score += 3

        elif (
            revenue_growth < 0
            and profit_growth < 0
        ):
            growth_score -= 3

    # ==============================
    # STRONG COMBINED GROWTH
    # ==============================

    if (
        "strong_long_term_growth"
        in cross_signals
    ):
        growth_score += 3

    growth_score = max(
        0,
        min(
            growth_score,
            25,
        ),
    )

    if growth_score >= 20:
        strengths.append(
            "strong_growth_quality"
        )

    elif growth_score >= 14:
        strengths.append(
            "positive_growth_quality"
        )

    elif growth_score < 8:
        warnings.append(
            "weak_growth_momentum"
        )

    # ==============================
    # 2. PROFITABILITY
    # MAX 25
    # ==============================

    gross_margin_change = margin_result.get(
        "gross_margin_change"
    )

    operating_margin_change = margin_result.get(
        "operating_margin_change"
    )

    # ==============================
    # GROSS MARGIN DIRECTION
    # ==============================

    if gross_margin_change is not None:
        if gross_margin_change >= 2:
            profitability_score += 8

        elif gross_margin_change > 0:
            profitability_score += 6

        elif gross_margin_change > -2:
            profitability_score += 3

    # ==============================
    # OPERATING MARGIN DIRECTION
    # ==============================

    if operating_margin_change is not None:
        if operating_margin_change >= 2:
            profitability_score += 9

        elif operating_margin_change > 0:
            profitability_score += 7

        elif operating_margin_change > -1:
            profitability_score += 3

    # ==============================
    # OPERATING LEVERAGE
    # ==============================

    if (
        "operating_leverage_positive"
        in cross_signals
    ):
        profitability_score += 5

    # ==============================
    # COST EFFICIENCY SUPPORT
    # ==============================

    if (
        "cost_efficiency_offset_gross_pressure"
        in cross_signals
        or
        "admin_efficiency_supports_profit_growth"
        in cross_signals
    ):
        profitability_score += 3

    profitability_score = max(
        0,
        min(
            profitability_score,
            25,
        ),
    )

    if profitability_score >= 20:
        strengths.append(
            "strong_profitability_profile"
        )

    elif profitability_score >= 14:
        strengths.append(
            "improving_profitability"
        )

    if (
        "gross_margin_down"
        in margin_signals
    ):
        warnings.append(
            "gross_margin_down"
        )

    # ==============================
    # 3. CASH QUALITY
    # MAX 25
    # ==============================

    cash_conversion = None

    if (
        cashflow_result is not None
        and cashflow_result.get("status")
        == "success"
    ):
        cash_conversion = (
            cashflow_result.get(
                "cash_conversion"
            )
        )

    # ==============================
    # OPERATING CASHFLOW
    # ==============================

    if (
        "operating_cashflow_positive"
        in cashflow_signals
    ):
        cash_quality_score += 8

    # ==============================
    # FREE CASHFLOW
    # ==============================

    if (
        "free_cashflow_positive"
        in cashflow_signals
    ):
        cash_quality_score += 8

    elif (
        "free_cashflow_negative"
        in cashflow_signals
    ):
        cash_quality_score += 2

    # ==============================
    # CASH CONVERSION
    # ==============================

    if cash_conversion is not None:
        if cash_conversion >= 1:
            cash_quality_score += 9

        elif cash_conversion >= 0.8:
            cash_quality_score += 7

        elif cash_conversion >= 0.5:
            cash_quality_score += 4

        elif cash_conversion > 0:
            cash_quality_score += 1

    cash_quality_score = max(
        0,
        min(
            cash_quality_score,
            25,
        ),
    )

    if cash_quality_score >= 20:
        strengths.append(
            "strong_cash_quality"
        )

    elif cash_quality_score >= 14:
        strengths.append(
            "positive_cash_quality"
        )

    elif cash_quality_score < 8:
        warnings.append(
            "weak_cash_quality"
        )

    # ==============================
    # PRESERVE CASHFLOW SIGNALS
    # ==============================

    if (
        "operating_cashflow_positive"
        in cashflow_signals
    ):
        strengths.append(
            "operating_cashflow_positive"
        )

    if (
        "free_cashflow_positive"
        in cashflow_signals
    ):
        strengths.append(
            "free_cashflow_positive"
        )

    if (
        "strong_cash_conversion"
        in cashflow_signals
    ):
        strengths.append(
            "strong_cash_conversion"
        )

    if (
        "operating_cashflow_quality_positive"
        in financial_cross_signals
    ):
        strengths.append(
            "operating_cashflow_quality_positive"
        )

        # ==============================
    # 4. FINANCIAL STRUCTURE
    # MAX 25
    # ==============================

    debt_to_equity = None
    equity_to_assets = None
    debt_change = None

    if (
        balance_result is not None
        and balance_result.get("status")
        == "success"
    ):
        debt_to_equity = (
            balance_result.get(
                "debt_to_equity"
            )
        )

        equity_to_assets = (
            balance_result.get(
                "equity_to_assets"
            )
        )

        debt_change = (
            balance_result.get(
                "debt_change"
            )
        )

    # ==============================
    # LEVERAGE
    # ==============================

    if debt_to_equity is not None:
        if debt_to_equity < 0.5:
            financial_structure_score += 9

        elif debt_to_equity < 1:
            financial_structure_score += 7

        elif debt_to_equity < 1.5:
            financial_structure_score += 4

        else:
            financial_structure_score += 1

    # ==============================
    # EQUITY BUFFER
    # ==============================

    if equity_to_assets is not None:
        if equity_to_assets >= 0.6:
            financial_structure_score += 9

        elif equity_to_assets >= 0.45:
            financial_structure_score += 7

        elif equity_to_assets >= 0.3:
            financial_structure_score += 4

        else:
            financial_structure_score += 1

        # ==============================
    # DEBT TREND
    #
    # balance_result debt_change
    # is percentage:
    # 5 = 5%
    # 15 = 15%
    # 30 = 30%
    # ==============================

    if debt_change is not None:
        if debt_change <= 5:
            financial_structure_score += 7

        elif debt_change <= 15:
            financial_structure_score += 5

        elif debt_change <= 30:
            financial_structure_score += 3

    # ==============================
    # CAPITAL DEPLOYMENT CONTEXT
    # ==============================

    productive_investment_cycle = (
        "productive_investment_cycle"
        in financial_cross_signals
    )

    improving_capital_productivity = (
        "investment_pressure_with_improving_capital_productivity"
        in financial_cross_signals
    )

    new_capital_outperforming = (
        "new_capital_outperforming_existing_capital_base"
        in financial_cross_signals
    )

    productive_external_funding = (
        "external_funding_supports_productive_investment"
        in financial_cross_signals
    )

    weak_capital_deployment = (
        "investment_pressure_with_weak_capital_deployment"
        in financial_cross_signals
    )

    negative_incremental_returns = (
        "debt_funded_investment_with_negative_incremental_returns"
        in financial_cross_signals
    )

    # ==============================
    # CAPITAL ALLOCATION QUALITY
    # ==============================

    capital_allocation_quality_signals = {
        "productive_reinvestment_confirmed",
        "incremental_capital_productivity_confirmed",
        "capital_scaling_efficiency_positive",
    }

    capital_allocation_quality_count = sum(
        1
        for signal
        in capital_allocation_quality_signals
        if signal
        in financial_cross_signals
    )

    if (
        capital_allocation_quality_count
        >= 2
    ):
        strengths.append(
            "strong_capital_allocation_quality"
        )

        financial_structure_score += 2

    # ==============================
    # PRODUCTIVE FCF DEFICIT
    # ==============================

    if (
        "negative_fcf_associated_with_productive_reinvestment"
        in financial_cross_signals
    ):
        strengths.append(
            "productive_reinvestment_explains_fcf_deficit"
        )

    # ==============================
    # EXTERNAL FUNDING QUALITY
    # ==============================

    if (
        "external_funding_supports_productive_capital_allocation"
        in financial_cross_signals
    ):
        strengths.append(
            "external_funding_deployed_productively"
        )

    # ==============================
    # CAPITAL PRODUCTIVITY TO CASH
    # ==============================

    if (
        "capital_productivity_translating_to_cashflow"
        in financial_cross_signals
    ):
        strengths.append(
            "capital_productivity_supporting_cashflow"
        )

        cash_quality_score += 1

    # ==============================
    # NEGATIVE FCF + RISING DEBT
    # BASE FUNDING PRESSURE
    # ==============================

    if (
        "negative_fcf_with_rising_debt"
        in financial_cross_signals
    ):
        if (
            productive_investment_cycle
            or productive_external_funding
        ):
            financial_structure_score -= 2

        else:
            financial_structure_score -= 5

    # ==============================
    # PRODUCTIVE CAPITAL DEPLOYMENT
    # ==============================

    if new_capital_outperforming:
        financial_structure_score += 2

    if improving_capital_productivity:
        financial_structure_score += 1

    # ==============================
    # DEBT SERVICE MITIGATION
    #
    # Debt service does not erase
    # funding pressure.
    #
    # It mitigates the risk that
    # funding pressure becomes
    # debt service stress.
    # ==============================

    if strong_debt_service_capacity:
        financial_structure_score += 1

        strengths.append(
            "strong_debt_service_capacity"
        )

    if debt_absorption_improving:
        financial_structure_score += 1

        strengths.append(
            "debt_absorption_capacity_improving"
        )

    if debt_service_resilience:
        strengths.append(
            "debt_service_resilience_confirmed"
        )

    # ==============================
    # PRODUCTIVE INVESTMENT
    # WITH DEBT CAPACITY
    # ==============================

    if (
        "productive_investment_supported_by_debt_capacity"
        in financial_cross_signals
    ):
        strengths.append(
            "productive_investment_supported_by_debt_capacity"
        )

    if (
        "external_funding_absorbed_by_earnings_growth"
        in financial_cross_signals
    ):
        strengths.append(
            "external_funding_absorbed_by_earnings_growth"
        )

    if (
        "productive_reinvestment_with_strong_debt_service"
        in financial_cross_signals
    ):
        strengths.append(
            "productive_reinvestment_with_strong_debt_service"
        )

    if (
        "cashflow_supports_debt_service_capacity"
        in financial_cross_signals
    ):
        strengths.append(
            "cashflow_supports_debt_service_capacity"
        )

    # ==============================
    # WEAK CAPITAL DEPLOYMENT
    # ==============================

    if weak_capital_deployment:
        financial_structure_score -= 5

    if negative_incremental_returns:
        financial_structure_score -= 8

    # ==============================
    # CAPITAL STRUCTURE PRESSURE
    # ==============================

    if (
        "capital_structure_pressure"
        in financial_cross_signals
    ):
        financial_structure_score -= 7

    # ==============================
    # FINAL FACTOR CAPS
    # ==============================

    cash_quality_score = max(
        0,
        min(
            cash_quality_score,
            25,
        ),
    )

    financial_structure_score = max(
        0,
        min(
            financial_structure_score,
            25,
        ),
    )

    # ==============================
    # FINANCIAL STRUCTURE CLASS
    # ==============================

    if financial_structure_score >= 20:
        strengths.append(
            "strong_financial_structure"
        )

    elif financial_structure_score >= 14:
        strengths.append(
            "adequate_financial_structure"
        )

    elif financial_structure_score < 8:
        warnings.append(
            "weak_financial_structure"
        )

    # ==============================
    # PRESERVE FINANCIAL CONTEXT
    # ==============================

    if (
        "balance_sheet_buffer_present"
        in financial_cross_signals
    ):
        strengths.append(
            "balance_sheet_buffer_present"
        )

    if (
        "investment_pressure_partially_buffered"
        in financial_cross_signals
    ):
        strengths.append(
            "investment_pressure_partially_buffered"
        )

    if productive_investment_cycle:
        strengths.append(
            "productive_investment_cycle"
        )

    if productive_external_funding:
        strengths.append(
            "external_funding_supports_productive_investment"
        )

    if improving_capital_productivity:
        strengths.append(
            "investment_pressure_with_improving_capital_productivity"
        )

    if new_capital_outperforming:
        strengths.append(
            "new_capital_outperforming_existing_capital_base"
        )

    if (
        "investment_pressure_showing_moderation"
        in financial_cross_signals
    ):
        strengths.append(
            "investment_pressure_showing_moderation"
        )

    if (
        "operating_cashflow_momentum_improving"
        in financial_cross_signals
    ):
        strengths.append(
            "operating_cashflow_momentum_improving"
        )

    # ==============================
    # PRESERVE FINANCIAL WARNINGS
    # ==============================

    if (
        "investment_pressure_with_net_debt"
        in financial_cross_signals
    ):
        warnings.append(
            "investment_pressure_with_net_debt"
        )

    if (
        "negative_fcf_with_rising_debt"
        in financial_cross_signals
    ):
        warnings.append(
            "negative_fcf_with_rising_debt"
        )

    if (
        "persistent_investment_pressure"
        in financial_cross_signals
    ):
        warnings.append(
            "persistent_investment_pressure"
        )

    if (
        "persistent_fcf_deficit_with_net_debt"
        in financial_cross_signals
    ):
        warnings.append(
            "persistent_fcf_deficit_with_net_debt"
        )

    if (
        "persistent_fcf_deficit_with_rising_debt"
        in financial_cross_signals
    ):
        warnings.append(
            "persistent_fcf_deficit_with_rising_debt"
        )

    if (
        "weak_investment_self_funding"
        in financial_cross_signals
    ):
        warnings.append(
            "weak_investment_self_funding"
        )

    if (
        "external_funding_dependence_rising"
        in financial_cross_signals
    ):
        warnings.append(
            "external_funding_dependence_rising"
        )

    if weak_capital_deployment:
        warnings.append(
            "investment_pressure_with_weak_capital_deployment"
        )

    if negative_incremental_returns:
        warnings.append(
            "debt_funded_investment_with_negative_incremental_returns"
        )

    if (
        "capital_structure_pressure"
        in financial_cross_signals
    ):
        warnings.append(
            "capital_structure_pressure"
        )

    # ==============================
    # REMOVE DUPLICATES
    # PRESERVE ORDER
    # ==============================

    strengths = list(
        dict.fromkeys(
            strengths
        )
    )

    warnings = list(
        dict.fromkeys(
            warnings
        )
    )


    # ==============================
    # PIOTROSKI SCORE
    # ==============================

    piotroski_bonus = 0

    if piotroski_result is not None:

        f_score = piotroski_result.get("score", 0)

        if f_score >= 8:
            piotroski_bonus = 10

        elif f_score >= 6:
            piotroski_bonus = 8

        elif f_score >= 4:
            piotroski_bonus = 5

        elif f_score >= 2:
            piotroski_bonus = 2

    altman_bonus = 0

    if (
        altman_result is not None
        and altman_result.get("status") == "success"
    ):

        level = altman_result.get("level")

        if level == "Safe":
            altman_bonus = 8

        elif level == "Grey":
            altman_bonus = 4

        else:
            altman_bonus = 0


        # ==============================
        # TOTAL SCORE
        # ==============================

        score = (
            growth_score
            + profitability_score
            + cash_quality_score
            + financial_structure_score
        )

        score = (
            score * 0.85
            + piotroski_bonus
            + altman_bonus
        )

        score = max(
            0,
            min(
                score,
                100,
            ),
        )

    # ==============================
    # HEALTH CLASS
    # ==============================

    if score >= 85:
        health_class = "excellent"

    elif score >= 70:
        health_class = "strong"

    elif score >= 50:
        health_class = "moderate"

    else:
        health_class = "weak"

    # ==============================
    # RETURN
    # ==============================

    return {
        "status": "success",
        "score": score,
        "health_class": health_class,
        "factor_scores": {
            "growth": growth_score,
            "profitability": (
                profitability_score
            ),
            "cash_quality": (
                cash_quality_score
            ),
            "financial_structure": (
                financial_structure_score
            ),
            "piotroski": piotroski_bonus,
            "altman": altman_bonus,
        },
        "strengths": strengths,
        "warnings": warnings,
    }