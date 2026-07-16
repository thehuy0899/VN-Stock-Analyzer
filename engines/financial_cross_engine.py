def analyze_financial_cross(
    cashflow_result,
    balance_result,
    cashflow_trend_result=None,
    capital_efficiency_result=None,
    capital_allocation_result=None,
    debt_service_result=None,
):
    # ==============================
    # VALIDATE INPUT
    # ==============================

    if cashflow_result is None:
        return {
            "status": "error",
            "message": (
                "Cashflow result is None."
            ),
        }

    if balance_result is None:
        return {
            "status": "error",
            "message": (
                "Balance result is None."
            ),
        }

    if (
        cashflow_result.get("status")
        != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Cashflow analysis "
                "was not successful."
            ),
        }

    if (
        balance_result.get("status")
        != "success"
    ):
        return {
            "status": "error",
            "message": (
                "Balance sheet analysis "
                "was not successful."
            ),
        }

    # ==============================
    # NORMALIZE OPTIONAL INPUTS
    # ==============================

    debt_service_result = (
        debt_service_result or {}
    )

    # ==============================
    # CASHFLOW DATA
    # ==============================

    operating_cashflow = (
        cashflow_result.get(
            "operating_cashflow"
        )
    )

    free_cashflow = (
        cashflow_result.get(
            "free_cashflow"
        )
    )

    cash_conversion = (
        cashflow_result.get(
            "cash_conversion"
        )
    )

    cashflow_signals = set(
        cashflow_result.get(
            "signals",
            [],
        )
    )

    # ==============================
    # BALANCE SHEET DATA
    # ==============================

    total_debt = balance_result.get(
        "total_debt"
    )

    net_debt = balance_result.get(
        "net_debt"
    )

    debt_change = balance_result.get(
        "debt_change"
    )

    debt_to_equity = balance_result.get(
        "debt_to_equity"
    )

    equity_to_assets = (
        balance_result.get(
            "equity_to_assets"
        )
    )

    balance_signals = set(
        balance_result.get(
            "signals",
            [],
        )
    )

    # ==============================
    # CASHFLOW TREND DATA
    # ==============================

    cashflow_regime = None
    cashflow_trend_signals = set()
    cashflow_history = []

    if (
        cashflow_trend_result is not None
        and cashflow_trend_result.get(
            "status"
        )
        == "success"
    ):
        cashflow_regime = (
            cashflow_trend_result.get(
                "cashflow_regime"
            )
        )

        cashflow_trend_signals = set(
            cashflow_trend_result.get(
                "signals",
                [],
            )
        )

        cashflow_history = (
            cashflow_trend_result.get(
                "cashflow_history",
                [],
            )
        )

    # ==============================
    # CAPITAL EFFICIENCY DATA
    # ==============================

    capital_efficiency_signals = set()

    capital_efficiency_regime = None
    latest_roic = None
    incremental_roic = None

    if (
        capital_efficiency_result is not None
        and capital_efficiency_result.get(
            "status"
        )
        == "success"
    ):
        capital_efficiency_signals = set(
            capital_efficiency_result.get(
                "signals",
                [],
            )
        )

        capital_efficiency_regime = (
            capital_efficiency_result.get(
                "capital_efficiency_regime"
            )
        )

        latest_roic = (
            capital_efficiency_result.get(
                "latest_roic"
            )
        )

        incremental_roic = (
            capital_efficiency_result.get(
                "incremental_roic"
            )
        )

    # ==============================
    # CAPITAL ALLOCATION DATA
    # ==============================

    capital_allocation_signals = set()

    if (
        capital_allocation_result is not None
        and capital_allocation_result.get(
            "status"
        )
        == "success"
    ):
        capital_allocation_signals = set(
            capital_allocation_result.get(
                "signals",
                [],
            )
        )

    # ==============================
    # DEBT SERVICE DATA
    # ==============================

    debt_service_signals = set(
        debt_service_result.get(
            "signals",
            [],
        )
    )

    debt_service_regime = (
        debt_service_result.get(
            "debt_service_regime"
        )
    )

    coverage_trend = (
        debt_service_result.get(
            "coverage_trend"
        )
    )

    interest_coverage_class = (
        debt_service_result.get(
            "interest_coverage_class"
        )
    )

    interest_burden_class = (
        debt_service_result.get(
            "interest_burden_class"
        )
    )

    # ==============================
    # SIGNAL CONTAINERS
    # ==============================

    signals = []

    diagnostics = {
        "cashflow_regime": (
            cashflow_regime
        ),
        "operating_cashflow": (
            operating_cashflow
        ),
        "free_cashflow": (
            free_cashflow
        ),
        "cash_conversion": (
            cash_conversion
        ),
        "total_debt": (
            total_debt
        ),
        "net_debt": (
            net_debt
        ),
        "debt_change": (
            debt_change
        ),
        "debt_to_equity": (
            debt_to_equity
        ),
        "equity_to_assets": (
            equity_to_assets
        ),
        "cashflow_history": (
            cashflow_history
        ),
        "capital_efficiency_regime": (
            capital_efficiency_regime
        ),
        "latest_roic": (
            latest_roic
        ),
        "incremental_roic": (
            incremental_roic
        ),
        "debt_service_regime": (
            debt_service_regime
        ),
        "coverage_trend": (
            coverage_trend
        ),
        "interest_coverage_class": (
            interest_coverage_class
        ),
        "interest_burden_class": (
            interest_burden_class
        ),
    }

    # ==============================
    # CURRENT INVESTMENT PRESSURE
    # ==============================

    if (
        "free_cashflow_negative"
        in cashflow_signals
        and "net_debt_position"
        in balance_signals
    ):
        signals.append(
            "investment_pressure_with_net_debt"
        )

    # ==============================
    # NEGATIVE FCF + RISING DEBT
    # ==============================

    if (
        "free_cashflow_negative"
        in cashflow_signals
        and "debt_increasing"
        in balance_signals
    ):
        signals.append(
            "negative_fcf_with_rising_debt"
        )

    # ==============================
    # PERSISTENT INVESTMENT PRESSURE
    # ==============================

    if (
        cashflow_regime
        == "persistent_negative_fcf"
        or (
            "multi_year_negative_free_cashflow"
            in cashflow_trend_signals
        )
    ):
        signals.append(
            "persistent_investment_pressure"
        )

    # ==============================
    # PERSISTENT FCF DEFICIT
    # WITH NET DEBT
    # ==============================

    if (
        (
            cashflow_regime
            == "persistent_negative_fcf"
            or (
                "multi_year_negative_free_cashflow"
                in cashflow_trend_signals
            )
        )
        and "net_debt_position"
        in balance_signals
    ):
        signals.append(
            "persistent_fcf_deficit_with_net_debt"
        )

    # ==============================
    # PERSISTENT FCF DEFICIT
    # WITH RISING DEBT
    # ==============================

    if (
        (
            cashflow_regime
            == "persistent_negative_fcf"
            or (
                "multi_year_negative_free_cashflow"
                in cashflow_trend_signals
            )
        )
        and "debt_increasing"
        in balance_signals
    ):
        signals.append(
            "persistent_fcf_deficit_with_rising_debt"
        )

    # ==============================
    # WEAK CAPEX SELF-FUNDING
    # ==============================

    if (
        "weak_capex_self_funding"
        in cashflow_trend_signals
    ):
        signals.append(
            "weak_investment_self_funding"
        )

    # ==============================
    # POSITIVE OCF QUALITY
    # ==============================

    if (
        "operating_cashflow_positive"
        in cashflow_signals
        or (
            "consistent_positive_operating_cashflow"
            in cashflow_trend_signals
        )
    ):
        signals.append(
            "operating_cashflow_quality_positive"
        )

    # ==============================
    # CASHFLOW IMPROVEMENT
    # ==============================

    if (
        "operating_cashflow_improving"
        in cashflow_trend_signals
    ):
        signals.append(
            "operating_cashflow_momentum_improving"
        )

    # ==============================
    # CAPEX MODERATION
    # ==============================

    if (
        "capex_moderating"
        in cashflow_trend_signals
    ):
        signals.append(
            "investment_intensity_moderating"
        )

    # ==============================
    # BALANCE SHEET BUFFER
    # ==============================

    if (
        "strong_equity_buffer"
        in balance_signals
    ):
        signals.append(
            "balance_sheet_buffer_present"
        )

    # ==============================
    # PARTIAL BUFFER
    # ==============================

    investment_pressure = (
        "investment_pressure_with_net_debt"
        in signals
        or "persistent_investment_pressure"
        in signals
    )

    if (
        investment_pressure
        and "balance_sheet_buffer_present"
        in signals
    ):
        signals.append(
            "investment_pressure_partially_buffered"
        )

    # ==============================
    # FUNDING PRESSURE ESCALATION
    # ==============================

    if (
        "persistent_fcf_deficit_with_rising_debt"
        in signals
        and "weak_investment_self_funding"
        in signals
    ):
        signals.append(
            "external_funding_dependence_rising"
        )

    # ==============================
    # PRESSURE MODERATION SIGNAL
    # ==============================

    if (
        "persistent_investment_pressure"
        in signals
        and (
            "operating_cashflow_momentum_improving"
            in signals
        )
        and (
            "investment_intensity_moderating"
            in signals
        )
    ):
        signals.append(
            "investment_pressure_showing_moderation"
        )

    # ==============================
    # INVESTMENT FUNDING
    # VS CAPITAL DEPLOYMENT QUALITY
    # ==============================

    if (
        "persistent_fcf_deficit_with_rising_debt"
        in signals
        and "strong_incremental_roic"
        in capital_efficiency_signals
    ):
        signals.append(
            "investment_funded_growth_with_productive_capital"
        )

    if (
        "external_funding_dependence_rising"
        in signals
        and "strong_incremental_roic"
        in capital_efficiency_signals
    ):
        signals.append(
            "external_funding_supports_productive_investment"
        )

    if (
        "persistent_investment_pressure"
        in signals
        and "capital_deployment_quality_improving"
        in capital_efficiency_signals
    ):
        signals.append(
            "investment_pressure_with_improving_capital_productivity"
        )

    if (
        (
            "persistent_fcf_deficit_with_net_debt"
            in signals
            or (
                "persistent_fcf_deficit_with_rising_debt"
                in signals
            )
        )
        and "negative_incremental_roic"
        in capital_efficiency_signals
    ):
        signals.append(
            "investment_pressure_with_weak_capital_deployment"
        )

    if (
        "persistent_fcf_deficit_with_rising_debt"
        in signals
        and "negative_incremental_roic"
        in capital_efficiency_signals
    ):
        signals.append(
            "debt_funded_investment_with_negative_incremental_returns"
        )

    # ==============================
    # CAPITAL RETURN GAP
    # ==============================

    if (
        latest_roic is not None
        and incremental_roic is not None
    ):
        if (
            incremental_roic
            > latest_roic
        ):
            signals.append(
                "new_capital_outperforming_existing_capital_base"
            )

        elif (
            incremental_roic
            < latest_roic
            and incremental_roic >= 0
        ):
            signals.append(
                "new_capital_returns_below_existing_capital_base"
            )

    # ==============================
    # CAPITAL DEPLOYMENT REGIME
    # ==============================

    if (
        capital_efficiency_regime
        == (
            "improving_with_strong_incremental_returns"
        )
        and "persistent_investment_pressure"
        in signals
    ):
        signals.append(
            "productive_investment_cycle"
        )

    # ==============================
    # CAPITAL ALLOCATION CROSS
    # ==============================

    if (
        "productive_capital_allocation"
        in capital_allocation_signals
    ):
        signals.append(
            "productive_reinvestment_confirmed"
        )

    if (
        "new_capital_more_productive"
        in capital_allocation_signals
    ):
        signals.append(
            "incremental_capital_productivity_confirmed"
        )

    if (
        "profit_growth_outpaces_capital_growth"
        in capital_allocation_signals
    ):
        signals.append(
            "capital_scaling_efficiency_positive"
        )

    if (
        "strong_incremental_returns"
        in capital_allocation_signals
        and "persistent_negative_free_cashflow"
        in cashflow_trend_signals
    ):
        signals.append(
            "negative_fcf_associated_with_productive_reinvestment"
        )

    if (
        "productive_capital_allocation"
        in capital_allocation_signals
        and "external_funding_dependence_rising"
        in signals
    ):
        signals.append(
            "external_funding_supports_productive_capital_allocation"
        )

    if (
        "profit_growth_outpaces_capital_growth"
        in capital_allocation_signals
        and "operating_cashflow_improving"
        in cashflow_trend_signals
    ):
        signals.append(
            "capital_productivity_translating_to_cashflow"
        )

    # ==============================
    # DEBT SERVICE CROSS FLAGS
    # ==============================

    strong_interest_coverage = (
        (
            "very_strong_interest_coverage"
            in debt_service_signals
        )
        or (
            "strong_interest_coverage"
            in debt_service_signals
        )
    )

    coverage_recovered = (
        (
            "interest_coverage_recovered_from_trough"
            in debt_service_signals
        )
    )

    coverage_sustained_high = (
        (
            "high_interest_coverage_sustained"
            in debt_service_signals
        )
    )

    low_interest_burden = (
        "low_interest_burden"
        in debt_service_signals
    )

    earnings_outpace_debt = (
        (
            "earnings_capacity_outpaces_debt_growth"
            in debt_service_signals
        )
    )

    cash_debt_support_present = (
        (
            "strong_cash_debt_support"
            in debt_service_signals
        )
        or (
            "moderate_cash_debt_support"
            in debt_service_signals
        )
    )

    debt_service_capacity_strong = (
        strong_interest_coverage
        and low_interest_burden
    )

    debt_absorption_capacity_improving = (
        earnings_outpace_debt
        and (
            coverage_recovered
            or coverage_sustained_high
        )
    )

    debt_service_resilience = (
        debt_service_capacity_strong
        and coverage_sustained_high
    )

    productive_debt_supported_investment = (
        (
            "productive_investment_cycle"
            in signals
        )
        and debt_service_capacity_strong
        and earnings_outpace_debt
    )

    external_funding_absorption_positive = (
        (
            "external_funding_dependence_rising"
            in signals
        )
        and debt_service_capacity_strong
        and earnings_outpace_debt
    )

    productive_reinvestment_with_debt_capacity = (
        (
            "productive_reinvestment_confirmed"
            in signals
        )
        and debt_service_resilience
    )

    cashflow_and_debt_service_support = (
        (
            "operating_cashflow_quality_positive"
            in signals
        )
        and cash_debt_support_present
        and debt_service_capacity_strong
    )

    # ==============================
    # DEBT SERVICE CROSS ANALYSIS
    # ==============================

    if debt_service_capacity_strong:
        signals.append(
            "strong_debt_service_capacity"
        )

    if debt_absorption_capacity_improving:
        signals.append(
            "debt_absorption_capacity_improving"
        )

    if debt_service_resilience:
        signals.append(
            "debt_service_resilience_confirmed"
        )

    if productive_debt_supported_investment:
        signals.append(
            "productive_investment_supported_by_debt_capacity"
        )

    if external_funding_absorption_positive:
        signals.append(
            "external_funding_absorbed_by_earnings_growth"
        )

    if productive_reinvestment_with_debt_capacity:
        signals.append(
            "productive_reinvestment_with_strong_debt_service"
        )

    if cashflow_and_debt_service_support:
        signals.append(
            "cashflow_supports_debt_service_capacity"
        )

    # ==============================
    # DEDUPLICATE SIGNALS
    # ==============================

    signals = list(
        dict.fromkeys(
            signals
        )
    )

    # =========================================================
    # DEBT SERVICE STRESS CROSS SIGNALS
    # =========================================================

    debt_service_signals = set()

    if (
        debt_service_result is not None
        and debt_service_result.get(
            "status"
        )
        == "success"
    ):
        debt_service_signals = set(
            debt_service_result.get(
                "signals",
                [],
            )
        )

    # =========================================================
    # CRITICAL DEBT SERVICE STRESS
    # =========================================================

    if (
        "critical_interest_coverage"
        in debt_service_signals
    ):
        signals.append(
            "critical_debt_service_stress"
        )

    # =========================================================
    # DEBT SERVICE DETERIORATING
    # =========================================================

    if (
        "latest_interest_coverage_deteriorating"
        in debt_service_signals
    ):
        signals.append(
            "latest_debt_service_momentum_deteriorating"
        )

    # =========================================================
    # DEBT GROWTH VS EARNINGS CAPACITY
    # =========================================================

    if (
        "latest_debt_growth_outpaces_ebit_growth"
        in debt_service_signals
    ):
        signals.append(
            "latest_debt_growth_outpaces_ebit_growth"
        )

    # =========================================================
    # WEAK CASH SUPPORT FOR DEBT
    # =========================================================

    if (
        "weak_cash_debt_support"
        in debt_service_signals
    ):
        signals.append(
            "weak_cash_support_for_debt"
        )

    # =========================================================
    # COMBINED DEBT SERVICE STRESS
    # =========================================================

    if (
        "critical_interest_coverage"
        in debt_service_signals
        and "latest_interest_coverage_deteriorating"
        in debt_service_signals
    ):
        signals.append(
            "debt_service_stress_confirmed"
        )

    if (
        "latest_debt_growth_outpaces_ebit_growth"
        in debt_service_signals
        and "weak_cash_debt_support"
        in debt_service_signals
    ):
        signals.append(
            "debt_absorption_capacity_weakening"
        )

    # =========================================================
    # FUNDING PRESSURE + DEBT SERVICE STRESS
    # =========================================================

    if (
        "negative_fcf_with_rising_debt"
        in signals
        and "critical_interest_coverage"
        in debt_service_signals
    ):
        signals.append(
            "funding_pressure_with_debt_service_stress"
        )

    if (
        "investment_pressure_with_net_debt"
        in signals
        and "latest_debt_growth_outpaces_ebit_growth"
        in debt_service_signals
        and "weak_cash_debt_support"
        in debt_service_signals
    ):
        signals.append(
            "investment_pressure_exceeds_debt_absorption"
        )

    # ==============================
    # RETURN
    # ==============================

    return {
        "status": "success",
        "signals": signals,
        "diagnostics": diagnostics,
    }