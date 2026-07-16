from analysis_pipeline import (
    run_analysis_for_symbol,
)


# ============================================================
# REGRESSION CASE SYMBOLS
# ============================================================

CASE_1_SYMBOL = "HPG"
CASE_2_SYMBOL = "MCO"
CASE_3_SYMBOL = "PC1"
CASE_4_SYMBOL = "VNM"


# ============================================================
# REGRESSION TEST HELPERS
# ============================================================


def assert_signal(
    signals,
    signal,
    case_name,
):
    assert signal in signals, (
        f"[{case_name}] "
        f"Missing signal: {signal}"
    )


def assert_no_signal(
    signals,
    signal,
    case_name,
):
    assert signal not in signals, (
        f"[{case_name}] "
        f"Unexpected signal: {signal}"
    )


def assert_status_success(
    result,
    case_name,
):
    assert result is not None, (
        f"[{case_name}] Result is None"
    )

    assert result.get("status") == "success", (
        f"[{case_name}] "
        f"Status is not success: "
        f"{result.get('status')}"
    )


def print_case_passed(
    case_name,
):
    print(
        f"[PASS] {case_name}"
    )


def get_final_analysis_text(
    final_analysis_result,
    key,
):
    return (
        final_analysis_result.get(
            key
        )
        or ""
    ).lower()


def assert_text_contains(
    text,
    phrase,
    case_name,
    field_name,
):
    assert phrase.lower() in text, (
        f"[{case_name}] "
        f"{field_name} missing phrase: "
        f"{phrase!r}. "
        f"Actual text: {text}"
    )


def assert_text_not_contains(
    text,
    phrase,
    case_name,
    field_name,
):
    assert phrase.lower() not in text, (
        f"[{case_name}] "
        f"{field_name} contains forbidden phrase: "
        f"{phrase!r}. "
        f"Actual text: {text}"
    )


# ============================================================
# CASE 1
# PRODUCTIVE REINVESTMENT
# NEGATIVE FCF + PRODUCTIVE CAPITAL
# ============================================================


def test_productive_reinvestment_case(
    health_result,
    financial_cross_result,
    debt_service_result,
    final_analysis_result,
):
    case_name = (
        "PRODUCTIVE REINVESTMENT "
        "WITH STRONG DEBT CAPACITY"
    )

    assert_status_success(
        health_result,
        case_name,
    )

    assert_status_success(
        financial_cross_result,
        case_name,
    )

    assert_status_success(
        debt_service_result,
        case_name,
    )

    # ==============================
    # HEALTH PROFILE
    # ==============================

    strengths = set(
        health_result.get(
            "strengths",
            [],
        )
    )

    warnings = set(
        health_result.get(
            "warnings",
            [],
        )
    )

    assert_signal(
        strengths,
        "strong_capital_allocation_quality",
        case_name,
    )

    assert_signal(
        strengths,
        (
            "productive_reinvestment_"
            "explains_fcf_deficit"
        ),
        case_name,
    )

    assert_signal(
        strengths,
        (
            "external_funding_"
            "deployed_productively"
        ),
        case_name,
    )

    assert_signal(
        strengths,
        "productive_investment_cycle",
        case_name,
    )

    assert_signal(
        strengths,
        (
            "new_capital_outperforming_"
            "existing_capital_base"
        ),
        case_name,
    )

    assert_signal(
        strengths,
        "strong_debt_service_capacity",
        case_name,
    )

    assert_signal(
        warnings,
        "persistent_investment_pressure",
        case_name,
    )

    assert_signal(
        warnings,
        "weak_investment_self_funding",
        case_name,
    )

    assert_signal(
        warnings,
        (
            "external_funding_"
            "dependence_rising"
        ),
        case_name,
    )

    # ==============================
    # FINANCIAL CROSS
    # ==============================

    cross_signals = set(
        financial_cross_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        cross_signals,
        (
            "negative_fcf_associated_with_"
            "productive_reinvestment"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "external_funding_supports_"
            "productive_capital_allocation"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "incremental_capital_"
            "productivity_confirmed"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "productive_investment_"
            "supported_by_debt_capacity"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "external_funding_absorbed_"
            "by_earnings_growth"
        ),
        case_name,
    )

    assert_no_signal(
        cross_signals,
        "debt_service_stress_confirmed",
        case_name,
    )

    assert_no_signal(
        cross_signals,
        (
            "debt_absorption_capacity_"
            "weakening"
        ),
        case_name,
    )

    # ==============================
    # DEBT SERVICE
    # ==============================

    debt_signals = set(
        debt_service_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        debt_signals,
        "very_strong_interest_coverage",
        case_name,
    )

    assert_signal(
        debt_signals,
        (
            "earnings_capacity_outpaces_"
            "debt_growth"
        ),
        case_name,
    )

    assert_signal(
        debt_signals,
        "moderate_cash_debt_support",
        case_name,
    )

    # ==============================
    # FINAL ANALYSIS
    # ==============================

    assert_status_success(
        final_analysis_result,
        case_name,
    )

    capital_quality = (
        get_final_analysis_text(
            final_analysis_result,
            "capital_quality",
        )
    )

    key_watch = (
        get_final_analysis_text(
            final_analysis_result,
            "key_watch",
        )
    )

    thesis = (
        get_final_analysis_text(
            final_analysis_result,
            "thesis",
        )
    )

    assert_text_contains(
        capital_quality,
        "tái đầu tư",
        case_name,
        "capital_quality",
    )

    assert_text_contains(
        thesis,
        "hiệu quả",
        case_name,
        "thesis",
    )

    assert_text_not_contains(
        key_watch,
        "áp lực nghiêm trọng",
        case_name,
        "key_watch",
    )

    print_case_passed(
        case_name
    )


# ============================================================
# CASE 2
# DEBT SERVICE STRESS
# WEAK DEBT ABSORPTION
# ============================================================


def test_debt_service_stress_case(
    health_result,
    financial_cross_result,
    debt_service_result,
    final_analysis_result,
):
    case_name = (
        "DEBT SERVICE STRESS "
        "WITH WEAK DEBT ABSORPTION"
    )

    assert_status_success(
        health_result,
        case_name,
    )

    assert_status_success(
        financial_cross_result,
        case_name,
    )

    assert_status_success(
        debt_service_result,
        case_name,
    )

    # ==============================
    # HEALTH PROFILE
    # ==============================

    strengths = set(
        health_result.get(
            "strengths",
            [],
        )
    )

    warnings = set(
        health_result.get(
            "warnings",
            [],
        )
    )

    assert_signal(
        strengths,
        "operating_cashflow_positive",
        case_name,
    )

    assert_signal(
        strengths,
        "operating_cashflow_quality_positive",
        case_name,
    )

    assert_signal(
        strengths,
        "balance_sheet_buffer_present",
        case_name,
    )

    assert_signal(
        warnings,
        "weak_growth_momentum",
        case_name,
    )

    assert_signal(
        warnings,
        "gross_margin_down",
        case_name,
    )

    assert_signal(
        warnings,
        "investment_pressure_with_net_debt",
        case_name,
    )

    assert_signal(
        warnings,
        "negative_fcf_with_rising_debt",
        case_name,
    )

    assert_signal(
        warnings,
        "weak_investment_self_funding",
        case_name,
    )

    # ==============================
    # FINANCIAL CROSS
    # ==============================

    cross_signals = set(
        financial_cross_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        cross_signals,
        "critical_debt_service_stress",
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "latest_debt_service_"
            "momentum_deteriorating"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "latest_debt_growth_"
            "outpaces_ebit_growth"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        "weak_cash_support_for_debt",
        case_name,
    )

    assert_signal(
        cross_signals,
        "debt_service_stress_confirmed",
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "debt_absorption_capacity_"
            "weakening"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "funding_pressure_with_"
            "debt_service_stress"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "investment_pressure_"
            "exceeds_debt_absorption"
        ),
        case_name,
    )

    assert_no_signal(
        cross_signals,
        "strong_debt_service_capacity",
        case_name,
    )

    assert_no_signal(
        cross_signals,
        (
            "debt_absorption_capacity_"
            "improving"
        ),
        case_name,
    )

    # ==============================
    # DEBT SERVICE
    # ==============================

    debt_signals = set(
        debt_service_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        debt_signals,
        "critical_interest_coverage",
        case_name,
    )

    assert_signal(
        debt_signals,
        (
            "latest_interest_coverage_"
            "deteriorating"
        ),
        case_name,
    )

    assert_signal(
        debt_signals,
        (
            "latest_debt_growth_"
            "outpaces_ebit_growth"
        ),
        case_name,
    )

    assert_signal(
        debt_signals,
        "weak_cash_debt_support",
        case_name,
    )

    assert_no_signal(
        debt_signals,
        "very_strong_interest_coverage",
        case_name,
    )

    assert_no_signal(
        debt_signals,
        "strong_cash_debt_support",
        case_name,
    )

    # ==============================
    # FINAL ANALYSIS
    # ==============================

    assert_status_success(
        final_analysis_result,
        case_name,
    )

    key_watch = (
        get_final_analysis_text(
            final_analysis_result,
            "key_watch",
        )
    )

    assert_text_contains(
        key_watch,
        "năng lực trả lãi",
        case_name,
        "key_watch",
    )

    assert_text_contains(
        key_watch,
        "áp lực nghiêm trọng",
        case_name,
        "key_watch",
    )

    assert (
        (
            "năng lực hấp thụ"
            in key_watch
        )
        or (
            "dư địa tiếp tục sử dụng "
            "nguồn vốn bên ngoài"
            in key_watch
        )
        or (
            "tốc độ tăng nợ"
            in key_watch
        )
    ), (
        f"[{case_name}] "
        f"Key watch lost debt absorption "
        f"or debt growth risk: "
        f"{key_watch}"
    )

    assert_text_contains(
        key_watch,
        "kiểm soát tốc độ tăng nợ",
        case_name,
        "key_watch",
    )

    assert_text_not_contains(
        key_watch,
        (
            "nền tảng dòng tiền và cấu trúc "
            "tài chính hiện duy trì tương đối vững"
        ),
        case_name,
        "key_watch",
    )

    print_case_passed(
        case_name
    )


# ============================================================
# CASE 3
# STRONG GROWTH
# IMPROVING DEBT ABSORPTION
# ============================================================


def test_growth_with_improving_debt_absorption_case(
    health_result,
    financial_cross_result,
    debt_service_result,
    final_analysis_result,
):
    case_name = (
        "STRONG GROWTH WITH "
        "IMPROVING DEBT ABSORPTION"
    )

    assert_status_success(
        health_result,
        case_name,
    )

    assert_status_success(
        financial_cross_result,
        case_name,
    )

    assert_status_success(
        debt_service_result,
        case_name,
    )

    # ==============================
    # HEALTH PROFILE
    # ==============================

    strengths = set(
        health_result.get(
            "strengths",
            [],
        )
    )

    warnings = set(
        health_result.get(
            "warnings",
            [],
        )
    )

    assert_signal(
        strengths,
        "strong_growth_quality",
        case_name,
    )

    assert_signal(
        strengths,
        "strong_profitability_profile",
        case_name,
    )

    assert_signal(
        strengths,
        "strong_cash_quality",
        case_name,
    )

    assert_signal(
        strengths,
        "free_cashflow_positive",
        case_name,
    )

    assert_signal(
        strengths,
        "strong_capital_allocation_quality",
        case_name,
    )

    assert_signal(
        strengths,
        (
            "capital_productivity_"
            "supporting_cashflow"
        ),
        case_name,
    )

    assert_signal(
        strengths,
        (
            "debt_absorption_capacity_"
            "improving"
        ),
        case_name,
    )

    assert_signal(
        strengths,
        (
            "new_capital_outperforming_"
            "existing_capital_base"
        ),
        case_name,
    )

    assert len(warnings) == 0, (
        f"[{case_name}] "
        f"Unexpected warnings: "
        f"{sorted(warnings)}"
    )

    # ==============================
    # FINANCIAL CROSS
    # ==============================

    cross_signals = set(
        financial_cross_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        cross_signals,
        (
            "operating_cashflow_"
            "momentum_improving"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "new_capital_outperforming_"
            "existing_capital_base"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "incremental_capital_"
            "productivity_confirmed"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "capital_productivity_"
            "translating_to_cashflow"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "debt_absorption_capacity_"
            "improving"
        ),
        case_name,
    )

    assert_no_signal(
        cross_signals,
        "debt_service_stress_confirmed",
        case_name,
    )

    assert_no_signal(
        cross_signals,
        (
            "debt_absorption_capacity_"
            "weakening"
        ),
        case_name,
    )

    assert_no_signal(
        cross_signals,
        (
            "funding_pressure_with_"
            "debt_service_stress"
        ),
        case_name,
    )

    # ==============================
    # DEBT SERVICE
    # ==============================

    debt_signals = set(
        debt_service_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        debt_signals,
        (
            "interest_coverage_"
            "recovered_from_trough"
        ),
        case_name,
    )

    assert_signal(
        debt_signals,
        "strong_interest_coverage",
        case_name,
    )

    assert_signal(
        debt_signals,
        (
            "latest_interest_coverage_"
            "improving"
        ),
        case_name,
    )

    assert_signal(
        debt_signals,
        (
            "earnings_capacity_outpaces_"
            "debt_growth"
        ),
        case_name,
    )

    assert_signal(
        debt_signals,
        "moderate_cash_debt_support",
        case_name,
    )

    assert_no_signal(
        debt_signals,
        "critical_interest_coverage",
        case_name,
    )

    assert_no_signal(
        debt_signals,
        (
            "latest_interest_coverage_"
            "deteriorating"
        ),
        case_name,
    )

    # ==============================
    # FINAL ANALYSIS
    # ==============================

    assert_status_success(
        final_analysis_result,
        case_name,
    )

    growth_driver = (
        get_final_analysis_text(
            final_analysis_result,
            "growth_driver",
        )
    )

    capital_quality = (
        get_final_analysis_text(
            final_analysis_result,
            "capital_quality",
        )
    )

    key_watch = (
        get_final_analysis_text(
            final_analysis_result,
            "key_watch",
        )
    )

    thesis = (
        get_final_analysis_text(
            final_analysis_result,
            "thesis",
        )
    )

    assert_text_contains(
        thesis,
        "tăng trưởng",
        case_name,
        "thesis",
    )

    assert (
        "tăng trưởng"
        in growth_driver
        or "tăng trưởng"
        in capital_quality
    ), (
        f"[{case_name}] "
        f"Growth profile lost from narrative. "
        f"Growth driver: {growth_driver}. "
        f"Capital quality: {capital_quality}"
    )

    assert_text_not_contains(
        key_watch,
        "áp lực nghiêm trọng",
        case_name,
        "key_watch",
    )

    assert_text_not_contains(
        key_watch,
        (
            "năng lực trả lãi đang chịu "
            "áp lực nghiêm trọng"
        ),
        case_name,
        "key_watch",
    )

    print_case_passed(
        case_name
    )


# ============================================================
# CASE 4
# MATURE BUSINESS
# WEAK GROWTH + STRONG FINANCIAL BASE
# ============================================================


def test_mature_low_growth_case(
    health_result,
    financial_cross_result,
    debt_service_result,
    final_analysis_result,
):
    case_name = (
        "MATURE LOW GROWTH "
        "STRONG FINANCIAL BASE"
    )

    assert_status_success(
        health_result,
        case_name,
    )

    assert_status_success(
        financial_cross_result,
        case_name,
    )

    assert_status_success(
        debt_service_result,
        case_name,
    )

    # ==============================
    # HEALTH PROFILE
    # ==============================

    strengths = set(
        health_result.get(
            "strengths",
            [],
        )
    )

    warnings = set(
        health_result.get(
            "warnings",
            [],
        )
    )

    assert_signal(
        strengths,
        "strong_cash_quality",
        case_name,
    )

    assert_signal(
        strengths,
        "strong_debt_service_capacity",
        case_name,
    )

    assert_signal(
        strengths,
        "strong_financial_structure",
        case_name,
    )

    assert_signal(
        warnings,
        "weak_growth_momentum",
        case_name,
    )

    # ==============================
    # DEBT SERVICE
    # ==============================

    debt_signals = set(
        debt_service_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        debt_signals,
        "very_strong_interest_coverage",
        case_name,
    )

    assert_signal(
        debt_signals,
        "strong_cash_debt_support",
        case_name,
    )

    assert_signal(
        debt_signals,
        (
            "latest_interest_coverage_"
            "deteriorating"
        ),
        case_name,
    )

    assert_signal(
        debt_signals,
        (
            "latest_debt_growth_"
            "outpaces_ebit_growth"
        ),
        case_name,
    )

    # ==============================
    # FINANCIAL CROSS
    # ==============================

    cross_signals = set(
        financial_cross_result.get(
            "signals",
            [],
        )
    )

    assert_signal(
        cross_signals,
        "strong_debt_service_capacity",
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "cashflow_supports_"
            "debt_service_capacity"
        ),
        case_name,
    )

    assert_signal(
        cross_signals,
        (
            "latest_debt_service_"
            "momentum_deteriorating"
        ),
        case_name,
    )

    assert_no_signal(
        cross_signals,
        "debt_absorption_capacity_weakening",
        case_name,
    )

    assert_no_signal(
        cross_signals,
        "debt_service_stress_confirmed",
        case_name,
    )

    assert_no_signal(
        cross_signals,
        (
            "investment_pressure_"
            "exceeds_debt_absorption"
        ),
        case_name,
    )

    # ==============================
    # FINAL ANALYSIS
    # ==============================

    assert_status_success(
        final_analysis_result,
        case_name,
    )

    key_watch = (
        get_final_analysis_text(
            final_analysis_result,
            "key_watch",
        )
    )

    capital_quality = (
        get_final_analysis_text(
            final_analysis_result,
            "capital_quality",
        )
    )

    assert_text_contains(
        key_watch,
        "động lực tăng trưởng",
        case_name,
        "key_watch",
    )

    assert_text_contains(
        key_watch,
        "tái tạo động lực tăng trưởng",
        case_name,
        "key_watch",
    )

    assert_text_contains(
        capital_quality,
        "doanh nghiệp trưởng thành",
        case_name,
        "capital_quality",
    )

    assert_text_not_contains(
        key_watch,
        "áp lực nghiêm trọng",
        case_name,
        "key_watch",
    )

    print_case_passed(
        case_name
    )


# ============================================================
# RUN REGRESSION TESTS
# ============================================================


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("REGRESSION TESTS")

    case_1_result = (
        run_analysis_for_symbol(
            CASE_1_SYMBOL
        )
    )

    test_productive_reinvestment_case(
        case_1_result["health"],
        case_1_result[
            "financial_cross"
        ],
        case_1_result[
            "debt_service"
        ],
        case_1_result[
            "final_analysis"
        ],
    )

    case_2_result = (
        run_analysis_for_symbol(
            CASE_2_SYMBOL
        )
    )

    test_debt_service_stress_case(
        case_2_result["health"],
        case_2_result[
            "financial_cross"
        ],
        case_2_result[
            "debt_service"
        ],
        case_2_result[
            "final_analysis"
        ],
    )

    case_3_result = (
        run_analysis_for_symbol(
            CASE_3_SYMBOL
        )
    )

    test_growth_with_improving_debt_absorption_case(
        case_3_result["health"],
        case_3_result[
            "financial_cross"
        ],
        case_3_result[
            "debt_service"
        ],
        case_3_result[
            "final_analysis"
        ],
    )

    case_4_result = (
        run_analysis_for_symbol(
            CASE_4_SYMBOL
        )
    )

    test_mature_low_growth_case(
        case_4_result["health"],
        case_4_result[
            "financial_cross"
        ],
        case_4_result[
            "debt_service"
        ],
        case_4_result[
            "final_analysis"
        ],
    )