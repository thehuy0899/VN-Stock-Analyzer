from final_analysis import generate_final_analysis
from financial_health import calculate_financial_health
from data_loader import load_income_statement
from financial_cross_engine import analyze_financial_cross
from analysis_engine import (
    analyze_margin,
    analyze_growth,
)

from cross_analysis import analyze_cross_signals
from vnstock import Finance
from cashflow_engine import analyze_cashflow
from balance_sheet_engine import analyze_balance_sheet
from growth_quality_engine import analyze_growth_quality
from earnings_driver_engine import (
    analyze_earnings_drivers,
)
from cashflow_trend_engine import (
    analyze_cashflow_trend,
)
from capital_efficiency_engine import (
    analyze_capital_efficiency,
)
from capital_allocation_engine import (
    analyze_capital_allocation,
)
from debt_service_engine import (
    analyze_debt_service,
)

symbol = "VNM"


# ==============================
# LOAD INCOME STATEMENT
# ==============================

income = load_income_statement(
    symbol
)


# ==============================
# TEST MARGIN ANALYSIS
# ==============================

result = analyze_margin(
    income
)

print(
    "\nKET QUA ANALYSIS ENGINE"
)

print(
    "=" * 60
)

print(
    "Trang thai:",
    result["status"]
)

if result["status"] == "success":
    print(
        "Giai doan:",
        result["first_year"],
        "-",
        result["latest_year"],
    )

    print(
        "Gross Margin:",
        f'{result["gross_margin"]:.2f}%'
    )

    print(
        "Operating Margin:",
        f'{result["operating_margin"]:.2f}%'
    )

    print(
        "Gross Margin Change:",
        f'{result["gross_margin_change"]:+.2f} diem %'
    )

    print(
        "Operating Margin Change:",
        f'{result["operating_margin_change"]:+.2f} diem %'
    )

    print(
        "Selling Ratio Change:",
        f'{result["selling_ratio_change"]:+.2f} diem %'
    )

    print(
        "Admin Ratio Change:",
        f'{result["admin_ratio_change"]:+.2f} diem %'
    )

    print(
        "\nSIGNALS:"
    )

    for signal in result["signals"]:
        print(
            "-",
            signal,
        )


# ==============================
# TEST GROWTH
# ==============================


print(
    "\n" + "=" * 60
)

print(
    "TEST GROWTH"
)

growth_result = analyze_growth(
    income
)

print(
    "Revenue Growth:",
    growth_result["revenue_growth"]
)

print(
    "Revenue Growth Class:",
    growth_result["revenue_growth_class"]
)

print(
    "Profit Growth:",
    growth_result["profit_growth"]
)

print(
    "Profit Growth Class:",
    growth_result["profit_growth_class"]
)

print(
    "Revenue CAGR:",
    growth_result["revenue_cagr"]
)

print(
    "Revenue CAGR Class:",
    growth_result["revenue_cagr_class"]
)

print(
    "Profit CAGR:",
    growth_result["profit_cagr"]
)

print(
    "Profit CAGR Class:",
    growth_result["profit_cagr_class"]
)

print(
    "\nGROWTH SIGNALS:"
)

for signal in growth_result["signals"]:
    print(
        "-",
        signal,
    )
print(
    "\n" + "=" * 60
)

print(
    "TEST GROWTH QUALITY"
)

growth_quality_result = (
    analyze_growth_quality(
        growth_result,
        result,
    )
)

print(
    "Trang thai:",
    growth_quality_result["status"],
)

if (
    growth_quality_result["status"]
    == "success"
):
    print(
        "Growth Quality:",
        growth_quality_result[
            "growth_quality"
        ],
    )

    print(
        "\nGROWTH QUALITY SIGNALS:"
    )

    for signal in growth_quality_result.get(
        "signals",
        [],
    ):
        print(
            "-",
            signal,
        )

    print(
        "\nPROFIT HISTORY:"
    )

    for item in growth_quality_result.get(
        "profit_history",
        [],
    ):
        print(
            "-",
            item["year"],
            ":",
            item["profit"],
        )

    print(
        "\nGROWTH QUALITY DIAGNOSTICS:"
    )

    for key, value in (
        growth_quality_result.get(
            "diagnostics",
            {},
        ).items()
    ):
        print(
            "-",
            key,
            ":",
            value,
        )

else:
    print(
        "Message:",
        growth_quality_result.get(
            "message"
        ),
    )

# ==============================
# TEST EARNINGS DRIVERS
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST EARNINGS DRIVERS"
)

earnings_driver_result = (
    analyze_earnings_drivers(
        growth_result,
        result,
        growth_quality_result,
    )
)

print(
    "Trang thai:",
    earnings_driver_result["status"],
)

if (
    earnings_driver_result["status"]
    == "success"
):
    print(
        "Growth Regime:",
        earnings_driver_result.get(
            "growth_regime"
        ),
    )

    print(
        "Driver Profile:",
        earnings_driver_result.get(
            "driver_profile"
        ),
    )

    print(
        "\nPRIMARY DRIVERS:"
    )

    for driver in (
        earnings_driver_result.get(
            "primary_drivers",
            [],
        )
    ):
        print(
            "-",
            driver,
        )

    print(
        "\nSECONDARY DRIVERS:"
    )

    for driver in (
        earnings_driver_result.get(
            "secondary_drivers",
            [],
        )
    ):
        print(
            "-",
            driver,
        )

    print(
        "\nEARNINGS MECHANISM:"
    )

    for mechanism in (
        earnings_driver_result.get(
            "earnings_mechanism",
            [],
        )
    ):
        print(
            "-",
            mechanism,
        )

    print(
        "\nOFFSET FACTORS:"
    )

    for factor in (
        earnings_driver_result.get(
            "offset_factors",
            [],
        )
    ):
        print(
            "-",
            factor,
        )

    print(
        "\nDRIVER SCORES:"
    )

    for driver, score in (
        earnings_driver_result.get(
            "driver_scores",
            {},
        ).items()
    ):
        print(
            "-",
            driver,
            ":",
            score,
        )

    print(
        "\nOFFSET SCORES:"
    )

    for factor, score in (
        earnings_driver_result.get(
            "offset_scores",
            {},
        ).items()
    ):
        print(
            "-",
            factor,
            ":",
            score,
        )

    print(
        "\nEARNINGS DRIVER SIGNALS:"
    )

    for signal in (
        earnings_driver_result.get(
            "signals",
            [],
        )
    ):
        print(
            "-",
            signal,
        )

    print(
        "\nEARNINGS DRIVER DIAGNOSTICS:"
    )

    for key, value in (
        earnings_driver_result.get(
            "diagnostics",
            {},
        ).items()
    ):
        print(
            "-",
            key,
            ":",
            value,
        )

else:
    print(
        "Message:",
        earnings_driver_result.get(
            "message"
        ),
    )

# ==============================
# TEST CROSS ANALYSIS
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST CROSS ANALYSIS"
)

cross_result = analyze_cross_signals(
    result,
    growth_result,
)

print(
    "Trang thai:",
    cross_result["status"]
)

print(
    "\nCROSS SIGNALS:"
)

for signal in cross_result["signals"]:
    print(
        "-",
        signal,
    )


# ==============================
# TEST BALANCE SHEET
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST BALANCE SHEET"
)

finance_balance = Finance(
    symbol=symbol,
    source="VCI",
)

balance_sheet = finance_balance.balance_sheet(
    period="year",
)

balance_result = analyze_balance_sheet(
    balance_sheet
)

print(
    "Trang thai:",
    balance_result["status"],
)

if balance_result["status"] == "success":
    print(
        "Latest Year:",
        balance_result["latest_year"],
    )

    print(
        "Cash:",
        balance_result["cash"],
    )

    print(
        "Short-term Debt:",
        balance_result["short_term_debt"],
    )

    print(
        "Long-term Debt:",
        balance_result["long_term_debt"],
    )

    print(
        "Total Debt:",
        balance_result["total_debt"],
    )

    print(
        "Net Debt:",
        balance_result["net_debt"],
    )

    print(
        "Total Assets:",
        balance_result["total_assets"],
    )

    print(
        "Equity:",
        balance_result["equity"],
    )

    print(
        "Debt / Equity:",
        balance_result["debt_to_equity"],
    )
    print(
        "Net Debt / Equity:",
        balance_result["net_debt_to_equity"],
    )

    print(
        "Previous Total Debt:",
        balance_result["previous_total_debt"],
    )

    print(
        "Debt Change:",
        balance_result["debt_change"],
    )
    print(
        "Debt / Assets:",
        balance_result["debt_to_assets"],
    )

    print(
        "Equity / Assets:",
        balance_result["equity_to_assets"],
    )

    print(
        "\nBALANCE SHEET SIGNALS:"
    )

    for signal in balance_result["signals"]:
        print(
            "-",
            signal,
        )

else:
    print(
        "Message:",
        balance_result.get(
            "message"
        ),
    )

    print(
        "Missing Items:",
        balance_result.get(
            "missing_items"
        ),
    )




# ============================================================
# TEST CAPITAL EFFICIENCY
# ============================================================

print()
print(
    "=" * 60
)
print(
    "TEST CAPITAL EFFICIENCY"
)

capital_efficiency_result = (
    analyze_capital_efficiency(
        income,
        balance_sheet,
    )
)

print(
    "Trang thai:",
    capital_efficiency_result.get(
        "status"
    ),
)

if (
    capital_efficiency_result.get(
        "status"
    )
    == "success"
):
    print(
        "Capital Efficiency Regime:",
        capital_efficiency_result.get(
            "capital_efficiency_regime"
        ),
    )

    print(
        "Capital Efficiency Profile:",
        capital_efficiency_result.get(
            "capital_efficiency_profile"
        ),
    )

    print(
        "Latest ROIC:",
        capital_efficiency_result.get(
            "latest_roic"
        ),
    )

    print(
        "Previous ROIC:",
        capital_efficiency_result.get(
            "previous_roic"
        ),
    )

    print(
        "ROIC Change:",
        capital_efficiency_result.get(
            "roic_change"
        ),
    )

    print(
        "ROIC Class:",
        capital_efficiency_result.get(
            "roic_class"
        ),
    )

    print(
        "Incremental ROIC:",
        capital_efficiency_result.get(
            "incremental_roic"
        ),
    )

    print(
        "Incremental ROIC Class:",
        capital_efficiency_result.get(
            "incremental_roic_class"
        ),
    )

    print()
    print(
        "CAPITAL HISTORY:"
    )

    for item in (
        capital_efficiency_result.get(
            "history",
            [],
        )
    ):
        print(
            "-",
            item.get(
                "year"
            ),
            ":",
            "ROIC =",
            item.get(
                "roic"
            ),
            "| Incremental ROIC =",
            item.get(
                "incremental_roic"
            ),
            "| NOPAT =",
            item.get(
                "nopat"
            ),
            "| Invested Capital =",
            item.get(
                "invested_capital"
            ),
        )

    print()
    print(
        "CAPITAL EFFICIENCY SIGNALS:"
    )

    for signal in (
        capital_efficiency_result.get(
            "signals",
            [],
        )
    ):
        print(
            "-",
            signal,
        )

    print()
    print(
        "CAPITAL EFFICIENCY DIAGNOSTICS:"
    )

    for key, value in (
        capital_efficiency_result.get(
            "diagnostics",
            {},
        ).items()
    ):
        print(
            "-",
            key,
            ":",
            value,
        )

else:
    print(
        "Message:",
        capital_efficiency_result.get(
            "message"
        ),
    )

    print(
        "Missing Items:",
        capital_efficiency_result.get(
            "missing_items"
        ),
    )

    print(
        "Diagnostics:",
        capital_efficiency_result.get(
            "diagnostics"
        ),
    )


# ==============================
# TEST CAPITAL ALLOCATION
# ==============================


print()

capital_allocation_result = (
    analyze_capital_allocation(
        capital_efficiency_result,
    )
)

print(
    "Trang thai:",
    capital_allocation_result.get("status"),
)

if (
    capital_allocation_result.get("status")
    == "success"
):
    print(
        "Allocation Regime:",
        capital_allocation_result.get(
            "allocation_regime"
        ),
    )

    print(
        "Reinvestment Intensity:",
        capital_allocation_result.get(
            "reinvestment_intensity"
        ),
    )

    print(
        "Invested Capital Growth:",
        capital_allocation_result.get(
            "invested_capital_growth"
        ),
    )

    print(
        "NOPAT Growth:",
        capital_allocation_result.get(
            "nopat_growth"
        ),
    )

    print(
        "Latest ROIC:",
        capital_allocation_result.get(
            "latest_roic"
        ),
    )

    print(
        "Incremental ROIC:",
        capital_allocation_result.get(
            "incremental_roic"
        ),
    )

    print()
    print("CAPITAL ALLOCATION SIGNALS:")

    for signal in (
        capital_allocation_result.get(
            "signals",
            [],
        )
    ):
        print("-", signal)

    print()
    print(
        "CAPITAL ALLOCATION DIAGNOSTICS:"
    )

    for key, value in (
        capital_allocation_result.get(
            "diagnostics",
            {},
        ).items()
    ):
        print("-", key, ":", value)

else:
    print(
        "Message:",
        capital_allocation_result.get(
            "message"
        ),
    )

    print(
        "Missing Items:",
        capital_allocation_result.get(
            "missing_items"
        ),
    )

# ==============================
# TEST CASHFLOW
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST CASHFLOW"
)

finance = Finance(
    symbol=symbol,
    source="VCI",
)

cashflow = finance.cash_flow(
    period="year",
)

cashflow_result = analyze_cashflow(
    cashflow,
    growth_result,
)

print(
    "Trang thai:",
    cashflow_result["status"],
)

if cashflow_result["status"] == "success":
    print(
        "Operating Cash Flow:",
        cashflow_result["operating_cashflow"],
    )

    print(
        "CAPEX:",
        cashflow_result["capex"],
    )

    print(
        "Free Cash Flow:",
        cashflow_result["free_cashflow"],
    )

    print(
        "Cash Conversion:",
        cashflow_result["cash_conversion"],
    )

    print(
        "\nCASHFLOW SIGNALS:"
    )

    for signal in cashflow_result["signals"]:
        print(
            "-",
            signal,
        )

# ============================================================
# TEST DEBT SERVICE
# ============================================================

print()
print(
    "=" * 60
)

print(
    "TEST DEBT SERVICE"
)

debt_service_result = (
    analyze_debt_service(
        income,
        balance_sheet,
        cashflow_result,
    )
)

print(
    "Trang thai:",
    debt_service_result.get(
        "status"
    ),
)

if (
    debt_service_result.get(
        "status"
    )
    == "success"
):
    print(
        "Debt Service Regime:",
        debt_service_result.get(
            "debt_service_regime"
        ),
    )

    print(
        "Coverage Trend:",
        debt_service_result.get(
            "coverage_trend"
        ),
    )

    print(
        "Latest Interest Coverage:",
        debt_service_result.get(
            "latest_interest_coverage"
        ),
    )

    print(
        "Previous Interest Coverage:",
        debt_service_result.get(
            "previous_interest_coverage"
        ),
    )

    print(
        "Interest Coverage Change:",
        debt_service_result.get(
            "interest_coverage_change"
        ),
    )

    print(
        "Interest Coverage Class:",
        debt_service_result.get(
            "interest_coverage_class"
        ),
    )

    print(
        "Latest Interest Burden:",
        debt_service_result.get(
            "latest_interest_burden"
        ),
    )

    print(
        "Interest Burden Class:",
        debt_service_result.get(
            "interest_burden_class"
        ),
    )

    print(
        "Debt Growth:",
        debt_service_result.get(
            "debt_growth"
        ),
    )

    print(
        "EBIT Growth:",
        debt_service_result.get(
            "ebit_growth"
        ),
    )

    print(
        "Cash Debt Support:",
        debt_service_result.get(
            "cash_debt_support"
        ),
    )

    print()
    print(
        "DEBT SERVICE HISTORY:"
    )

    for item in (
        debt_service_result.get(
            "history",
            [],
        )
    ):
        print(
            "-",
            item.get(
                "year"
            ),
            "| Operating Profit:",
            item.get(
                "operating_profit"
            ),
            "| Adjusted EBIT:",
            item.get(
                "adjusted_ebit"
            ),
            "| Interest Expense:",
            item.get(
                "interest_expense"
            ),
            "| Total Debt:",
            item.get(
                "total_debt"
            ),
            "| Interest Coverage:",
            item.get(
                "interest_coverage"
            ),
            "| Interest Burden:",
            item.get(
                "interest_burden"
            ),
        )

    print()
    print(
        "DEBT SERVICE SIGNALS:"
    )

    for signal in (
        debt_service_result.get(
            "signals",
            [],
        )
    ):
        print(
            "-",
            signal,
        )

    print()
    print(
        "DEBT SERVICE DIAGNOSTICS:"
    )

    for key, value in (
        debt_service_result.get(
            "diagnostics",
            {},
        ).items()
    ):
        print(
            "-",
            key,
            ":",
            value,
        )

else:
    print(
        "Message:",
        debt_service_result.get(
            "message"
        ),
    )

    print(
        "Missing Items:",
        debt_service_result.get(
            "missing_items"
        ),
    )

    print(
        "Diagnostics:",
        debt_service_result.get(
            "diagnostics"
        ),
    )

# ==============================
# TEST CASHFLOW TREND
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST CASHFLOW TREND"
)

cashflow_trend_result = (
    analyze_cashflow_trend(
        cashflow
    )
)

print(
    "Trang thai:",
    cashflow_trend_result[
        "status"
    ],
)

if (
    cashflow_trend_result[
        "status"
    ]
    == "success"
):
    print(
        "Cashflow Regime:",
        cashflow_trend_result[
            "cashflow_regime"
        ],
    )

    print(
        "\nCASHFLOW HISTORY:"
    )

    for item in (
        cashflow_trend_result.get(
            "cashflow_history",
            [],
        )
    ):
        print(
            "-",
            item["year"],
            "| CFO:",
            item[
                "operating_cashflow"
            ],
            "| CAPEX:",
            item["capex"],
            "| FCF:",
            item["free_cashflow"],
        )

    print(
        "\nCASHFLOW TREND SIGNALS:"
    )

    for signal in (
        cashflow_trend_result.get(
            "signals",
            [],
        )
    ):
        print(
            "-",
            signal,
        )

    print(
        "\nCASHFLOW TREND DIAGNOSTICS:"
    )

    for key, value in (
        cashflow_trend_result.get(
            "diagnostics",
            {},
        ).items()
    ):
        print(
            "-",
            key,
            ":",
            value,
        )

else:
    print(
        "Message:",
        cashflow_trend_result.get(
            "message"
        ),
    )

    print(
        "Missing Items:",
        cashflow_trend_result.get(
            "missing_items"
        ),
    )

    print(
        "\nAVAILABLE CASHFLOW COLUMNS:"
    )

    for column in (
        cashflow_trend_result.get(
            "available_columns",
            [],
        )
    ):
        print(
            "-",
            repr(column),
        )

    print(
        "\nCASHFLOW COLUMN TYPE:"
    )

    print(
        type(
            cashflow.columns
        )
    )

    print(
        "\nRAW CASHFLOW COLUMNS:"
    )

    for column in cashflow.columns:
        print(
            "-",
            repr(column),
        )

# ==============================
# TEST FINANCIAL CROSS
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST FINANCIAL CROSS"
)

financial_cross_result = (
    analyze_financial_cross(
        cashflow_result,
        balance_result,
        cashflow_trend_result,
        capital_efficiency_result,
        capital_allocation_result,
        debt_service_result,
    )
)

print(
    "Trang thai:",
    financial_cross_result["status"],
)

if financial_cross_result["status"] == "success":
    print(
        "\nFINANCIAL CROSS SIGNALS:"
    )

    for signal in financial_cross_result["signals"]:
        print(
            "-",
            signal,
        )

else:
    print(
        "Message:",
        financial_cross_result.get(
            "message"
        ),
    )

# ==============================
# TEST FINANCIAL HEALTH
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST FINANCIAL HEALTH"
)

health_result = calculate_financial_health(
    result,
    growth_result,
    cross_result,
    cashflow_result,
    financial_cross_result,
    balance_result,
)

print(
    "Trang thai:",
    health_result["status"]
)

print(
    "Score:",
    health_result["score"]
)

print(
    "Health Class:",
    health_result["health_class"]
)

print(
    "\nSTRENGTHS:"
)

for strength in health_result["strengths"]:
    print(
        "-",
        strength,
    )

print(
    "\nWARNINGS:"
)

for warning in health_result["warnings"]:
    print(
        "-",
        warning,
    )


# ==============================
# TEST FINAL ANALYSIS
# ==============================

print(
    "\n" + "=" * 60
)

print(
    "TEST FINAL ANALYSIS"
)

final_result = generate_final_analysis(
    result,
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



print(
    "Trang thai:",
    final_result["status"]
)

print(
    "Score:",
    final_result["score"]
)

print(
    "Health Class:",
    final_result["health_class"]
)

print(
    "\nFACTOR SCORES:"
)

for factor, factor_score in (
    health_result["factor_scores"].items()
):
    print(
        "-",
        factor,
        ":",
        factor_score,
        "/ 25",
    )

print(
    "\nPHAN TICH:"
)

for text in final_result["analysis"]:
    print(
        "-",
        text,
    )

print(
    "\nKET LUAN:"
)

print(
    final_result.get(
        "conclusion"
    )
)


# ============================================================
# INVESTMENT THESIS
# ============================================================

print()
print(
    "=" * 60
)

print(
    "INVESTMENT THESIS"
)

print()
print(
    "GROWTH DRIVER:"
)

print(
    final_result.get(
        "growth_driver"
    )
)

print()
print(
    "GROWTH QUALITY:"
)

print(
    final_result.get(
        "growth_quality"
    )
)

print()
print(
    "CAPITAL QUALITY:"
)

print(
    final_result.get(
        "capital_quality"
    )
)

print()
print(
    "KEY WATCH:"
)

print(
    final_result.get(
        "key_watch"
    )
)

print()
print(
    "FULL THESIS:"
)

print(
    final_result.get(
        "thesis"
    )
)
