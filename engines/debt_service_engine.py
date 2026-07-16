import pandas as pd


# ============================================================
# HELPERS
# ============================================================


def _normalize_text(
    value,
):
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .lower()
    )


def _find_item_column(
    dataframe,
):
    candidate_columns = [
        "item",
        "ITEM",
        "Item",
    ]

    for column in candidate_columns:
        if column in dataframe.columns:
            return column

    return None


def _find_row(
    dataframe,
    item_column,
    keywords,
):
    if (
        dataframe is None
        or item_column is None
    ):
        return None

    normalized_keywords = [
        _normalize_text(
            keyword
        )
        for keyword in keywords
    ]

    for index, value in (
        dataframe[
            item_column
        ].items()
    ):
        normalized_value = (
            _normalize_text(
                value
            )
        )

        for keyword in (
            normalized_keywords
        ):
            if (
                keyword
                in normalized_value
            ):
                return index

    return None


def _get_year_columns(
    dataframe,
):
    year_columns = []

    for column in dataframe.columns:
        try:
            year = int(
                column
            )

            if (
                1900
                <= year
                <= 2200
            ):
                year_columns.append(
                    (
                        year,
                        column,
                    )
                )

        except (
            TypeError,
            ValueError,
        ):
            continue

    year_columns.sort(
        key=lambda item: item[0]
    )

    return year_columns


def _to_number(
    value,
):
    if pd.isna(
        value
    ):
        return None

    try:
        return float(
            value
        )

    except (
        TypeError,
        ValueError,
    ):
        return None


def _safe_growth(
    latest_value,
    previous_value,
):
    if (
        latest_value is None
        or previous_value is None
        or previous_value == 0
    ):
        return None

    return (
        (
            latest_value
            - previous_value
        )
        / abs(
            previous_value
        )
    )


# ============================================================
# CLASSIFICATION
# ============================================================


def _classify_interest_coverage(
    interest_coverage,
):
    if interest_coverage is None:
        return None

    if interest_coverage >= 6:
        return "very_strong"

    if interest_coverage >= 3:
        return "strong"

    if interest_coverage >= 1.5:
        return "moderate"

    if interest_coverage >= 1:
        return "weak"

    return "critical"


def _classify_interest_burden(
    interest_burden,
):
    if interest_burden is None:
        return None

    if interest_burden <= 0.10:
        return "very_low"

    if interest_burden <= 0.20:
        return "low"

    if interest_burden <= 0.40:
        return "moderate"

    if interest_burden <= 0.70:
        return "high"

    return "very_high"


def _classify_debt_service_regime(
    coverage_class,
    coverage_change,
    debt_growth,
    ebit_growth,
):
    if (
        coverage_class
        in [
            "very_strong",
            "strong",
        ]
        and coverage_change is not None
        and coverage_change > 0
    ):
        return (
            "strong_and_improving"
        )

    if (
        coverage_class
        in [
            "very_strong",
            "strong",
        ]
    ):
        return (
            "strong_debt_service_capacity"
        )

    if (
        coverage_class
        == "moderate"
        and coverage_change is not None
        and coverage_change > 0
    ):
        return (
            "moderate_but_improving"
        )

    if (
        coverage_class
        == "moderate"
    ):
        return (
            "moderate_debt_service_capacity"
        )

    if (
        coverage_class
        in [
            "weak",
            "critical",
        ]
        and coverage_change is not None
        and coverage_change < 0
    ):
        return (
            "debt_service_stress_worsening"
        )

    if (
        coverage_class
        in [
            "weak",
            "critical",
        ]
    ):
        return (
            "weak_debt_service_capacity"
        )

    if (
        debt_growth is not None
        and ebit_growth is not None
        and debt_growth
        > ebit_growth
    ):
        return (
            "debt_growth_outpacing_earnings"
        )

    return "neutral"

def _analyze_coverage_trend(
    history,
):
    valid_history = [
        item
        for item in history
        if item.get(
            "interest_coverage"
        )
        is not None
    ]

    if len(valid_history) < 3:
        return {
            "coverage_trend": None,
            "coverage_trend_signals": [],
            "coverage_trend_diagnostics": {
                "valid_periods": len(
                    valid_history
                ),
            },
        }

    coverage_values = [
        item[
            "interest_coverage"
        ]
        for item in valid_history
    ]

    latest_coverage = (
        coverage_values[-1]
    )

    previous_coverage = (
        coverage_values[-2]
    )

    historical_values = (
        coverage_values[:-1]
    )

    historical_average = (
        sum(
            historical_values
        )
        / len(
            historical_values
        )
    )

    trough_coverage = min(
        coverage_values
    )

    trough_index = (
        coverage_values.index(
            trough_coverage
        )
    )

    latest_change = (
        latest_coverage
        - previous_coverage
    )

    recovery_from_trough = (
        trough_index
        < len(
            coverage_values
        )
        - 1
        and latest_coverage
        > trough_coverage
    )

    maintained_high_coverage = (
        latest_coverage >= 6
        and previous_coverage >= 6
        and abs(
            latest_change
        )
        <= 0.5
    )

    persistent_improvement = all(
        coverage_values[index]
        >= coverage_values[
            index - 1
        ]
        for index in range(
            1,
            len(
                coverage_values
            ),
        )
    )

    persistent_deterioration = all(
        coverage_values[index]
        <= coverage_values[
            index - 1
        ]
        for index in range(
            1,
            len(
                coverage_values
            ),
        )
    )

    signals = []

    if recovery_from_trough:
        signals.append(
            "interest_coverage_recovered_from_trough"
        )

    if maintained_high_coverage:
        signals.append(
            "high_interest_coverage_sustained"
        )

    if persistent_improvement:
        signals.append(
            "persistent_interest_coverage_improvement"
        )

    if persistent_deterioration:
        signals.append(
            "persistent_interest_coverage_deterioration"
        )

    if (
        recovery_from_trough
        and maintained_high_coverage
    ):
        coverage_trend = (
            "recovered_and_sustained_high"
        )

    elif persistent_improvement:
        coverage_trend = (
            "persistent_improvement"
        )

    elif persistent_deterioration:
        coverage_trend = (
            "persistent_deterioration"
        )

    elif maintained_high_coverage:
        coverage_trend = (
            "stable_high"
        )

    elif recovery_from_trough:
        coverage_trend = (
            "recovering"
        )

    else:
        coverage_trend = (
            "mixed"
        )

    return {
        "coverage_trend": (
            coverage_trend
        ),
        "coverage_trend_signals": (
            signals
        ),
        "coverage_trend_diagnostics": {
            "valid_periods": len(
                valid_history
            ),
            "coverage_values": (
                coverage_values
            ),
            "latest_coverage": (
                latest_coverage
            ),
            "previous_coverage": (
                previous_coverage
            ),
            "latest_change": (
                latest_change
            ),
            "historical_average": (
                historical_average
            ),
            "trough_coverage": (
                trough_coverage
            ),
            "trough_year": (
                valid_history[
                    trough_index
                ].get(
                    "year"
                )
            ),
            "recovery_from_trough": (
                recovery_from_trough
            ),
            "maintained_high_coverage": (
                maintained_high_coverage
            ),
        },
    }

# ============================================================
# MAIN ENGINE
# ============================================================


def analyze_debt_service(
    income,
    balance_sheet,
    cashflow_result=None,
):
    # ==============================
    # VALIDATE INPUT
    # ==============================

    if (
        income is None
        or balance_sheet is None
    ):
        return {
            "status": "error",
            "message": (
                "Income statement or "
                "balance sheet is missing."
            ),
            "missing_items": None,
        }

    # ==============================
    # ITEM COLUMNS
    # ==============================

    income_item_column = (
        _find_item_column(
            income
        )
    )

    balance_item_column = (
        _find_item_column(
            balance_sheet
        )
    )

    if (
        income_item_column is None
        or balance_item_column is None
    ):
        return {
            "status": "error",
            "message": (
                "Financial item column "
                "was not found."
            ),
            "missing_items": [
                "item_column",
            ],
        }

    # ==============================
    # FIND INCOME ROWS
    # ==============================

    operating_profit_row = (
        _find_row(
            income,
            income_item_column,
            [
                (
                    "lãi/(lỗ) từ hoạt động "
                    "kinh doanh"
                ),
                (
                    "lợi nhuận từ hoạt động "
                    "kinh doanh"
                ),
            ],
        )
    )

    interest_expense_row = (
        _find_row(
            income,
            income_item_column,
            [
                "chi phí lãi vay",
                "interest expense",
            ],
        )
    )

    # ==============================
    # FIND BALANCE ROWS
    # ==============================

    short_term_debt_row = (
        _find_row(
            balance_sheet,
            balance_item_column,
            [
                "vay ngắn hạn",
                "short-term borrowings",
                "short term borrowings",
            ],
        )
    )

    long_term_debt_row = (
        _find_row(
            balance_sheet,
            balance_item_column,
            [
                "vay dài hạn",
                "long-term borrowings",
                "long term borrowings",
            ],
        )
    )

    # ==============================
    # VALIDATE REQUIRED ITEMS
    # ==============================

    missing_items = []

    if operating_profit_row is None:
        missing_items.append(
            "operating_profit"
        )

    if interest_expense_row is None:
        missing_items.append(
            "interest_expense"
        )

    if (
        short_term_debt_row is None
        and long_term_debt_row is None
    ):
        missing_items.append(
            "debt"
        )

    if missing_items:
        return {
            "status": "error",
            "message": (
                "Required financial items "
                "were not found."
            ),
            "missing_items": (
                missing_items
            ),
            "diagnostics": {
                "income_item_column": (
                    income_item_column
                ),
                "balance_item_column": (
                    balance_item_column
                ),
                "operating_profit_row": (
                    operating_profit_row
                ),
                "interest_expense_row": (
                    interest_expense_row
                ),
                "short_term_debt_row": (
                    short_term_debt_row
                ),
                "long_term_debt_row": (
                    long_term_debt_row
                ),
            },
        }

    # ==============================
    # YEAR COLUMNS
    # ==============================

    income_year_columns = dict(
        _get_year_columns(
            income
        )
    )

    balance_year_columns = dict(
        _get_year_columns(
            balance_sheet
        )
    )

    common_years = sorted(
        set(
            income_year_columns.keys()
        )
        & set(
            balance_year_columns.keys()
        )
    )

    if len(
        common_years
    ) < 2:
        return {
            "status": "error",
            "message": (
                "Insufficient financial "
                "history."
            ),
            "missing_items": None,
        }

    # ==============================
    # BUILD HISTORY
    # ==============================

    history = []

    for year in common_years:
        income_column = (
            income_year_columns[
                year
            ]
        )

        balance_column = (
            balance_year_columns[
                year
            ]
        )

        operating_profit = (
            _to_number(
                income.loc[
                    operating_profit_row,
                    income_column,
                ]
            )
        )

        interest_expense = (
            _to_number(
                income.loc[
                    interest_expense_row,
                    income_column,
                ]
            )
        )

        short_term_debt = 0.0

        if (
            short_term_debt_row
            is not None
        ):
            short_term_debt = (
                _to_number(
                    balance_sheet.loc[
                        short_term_debt_row,
                        balance_column,
                    ]
                )
                or 0.0
            )

        long_term_debt = 0.0

        if (
            long_term_debt_row
            is not None
        ):
            long_term_debt = (
                _to_number(
                    balance_sheet.loc[
                        long_term_debt_row,
                        balance_column,
                    ]
                )
                or 0.0
            )

        total_debt = (
            short_term_debt
            + long_term_debt
        )

        if interest_expense is not None:
            interest_expense = abs(
                interest_expense
            )

        adjusted_ebit = None
        interest_coverage = None
        interest_burden = None

        if (
            operating_profit is not None
            and interest_expense is not None
        ):
            adjusted_ebit = (
                operating_profit
                + interest_expense
            )

        if (
            adjusted_ebit is not None
            and interest_expense is not None
            and interest_expense > 0
        ):
            interest_coverage = (
                adjusted_ebit
                / interest_expense
            )

        if (
            adjusted_ebit is not None
            and adjusted_ebit > 0
            and interest_expense is not None
        ):
            interest_burden = (
                interest_expense
                / adjusted_ebit
            )

        history.append(
            {
                "year": year,
                "operating_profit": (
                    operating_profit
                ),
                "adjusted_ebit": (
                    adjusted_ebit
                ),
                "interest_expense": (
                    interest_expense
                ),
                "short_term_debt": (
                    short_term_debt
                ),
                "long_term_debt": (
                    long_term_debt
                ),
                "total_debt": (
                    total_debt
                ),
                "interest_coverage": (
                    interest_coverage
                ),
                "interest_burden": (
                    interest_burden
                ),
            }
        )

    if len(
        history
    ) < 2:
        return {
            "status": "error",
            "message": (
                "Insufficient debt service "
                "history."
            ),
            "missing_items": None,
        }

    coverage_trend_result = (
        _analyze_coverage_trend(
            history
        )
    )

    coverage_trend = (
        coverage_trend_result.get(
            "coverage_trend"
        )
    )

    coverage_trend_signals = (
        coverage_trend_result.get(
            "coverage_trend_signals",
            [],
        )
    )

    coverage_trend_diagnostics = (
        coverage_trend_result.get(
            "coverage_trend_diagnostics",
            {},
        )
    )

    # ==============================
    # LATEST / PREVIOUS
    # ==============================

    latest = history[-1]
    previous = history[-2]

    latest_interest_coverage = (
        latest[
            "interest_coverage"
        ]
    )

    previous_interest_coverage = (
        previous[
            "interest_coverage"
        ]
    )

    latest_interest_burden = (
        latest[
            "interest_burden"
        ]
    )

    coverage_change = None

    if (
        latest_interest_coverage
        is not None
        and previous_interest_coverage
        is not None
    ):
        coverage_change = (
            latest_interest_coverage
            - previous_interest_coverage
        )

    debt_growth = _safe_growth(
        latest[
            "total_debt"
        ],
        previous[
            "total_debt"
        ],
    )

    ebit_growth = (
        _safe_growth(
            latest[
                "adjusted_ebit"
            ],
            previous[
                "adjusted_ebit"
            ],
        )
    )

    # ==============================
    # CLASSIFICATION
    # ==============================

    coverage_class = (
        _classify_interest_coverage(
            latest_interest_coverage
        )
    )

    burden_class = (
        _classify_interest_burden(
            latest_interest_burden
        )
    )

    debt_service_regime = (
        _classify_debt_service_regime(
            coverage_class,
            coverage_change,
            debt_growth,
            ebit_growth,
        )
    )

    # ==============================
    # CASH DEBT SUPPORT
    # ==============================

    operating_cashflow = None
    cash_debt_support = None

    if (
        cashflow_result is not None
        and cashflow_result.get(
            "status"
        )
        == "success"
    ):
        operating_cashflow = (
            cashflow_result.get(
                "operating_cashflow"
            )
        )

    if (
        operating_cashflow is not None
        and latest[
            "total_debt"
        ]
        > 0
    ):
        cash_debt_support = (
            operating_cashflow
            / latest[
                "total_debt"
            ]
        )

    # ==============================
    # SIGNALS
    # ==============================

    signals = []

    signals.extend(
    coverage_trend_signals
)

    if coverage_class == "very_strong":
        signals.append(
            "very_strong_interest_coverage"
        )

    elif coverage_class == "strong":
        signals.append(
            "strong_interest_coverage"
        )

    elif coverage_class == "moderate":
        signals.append(
            "moderate_interest_coverage"
        )

    elif coverage_class == "weak":
        signals.append(
            "weak_interest_coverage"
        )

    elif coverage_class == "critical":
        signals.append(
            "critical_interest_coverage"
        )

    if (
        coverage_change is not None
        and coverage_change > 0.5
    ):
        signals.append(
            "latest_interest_coverage_improving"
        )

    elif (
        coverage_change is not None
        and coverage_change < -0.5
    ):
        signals.append(
            "latest_interest_coverage_deteriorating"
        )

    if burden_class in [
        "very_low",
        "low",
    ]:
        signals.append(
            "low_interest_burden"
        )

    elif burden_class == "high":
        signals.append(
            "high_interest_burden"
        )

    elif burden_class == "very_high":
        signals.append(
            "very_high_interest_burden"
        )
    
    if (
    debt_growth is not None
    and ebit_growth is not None
):
        if (
            ebit_growth
            > debt_growth
        ):
            signals.append(
                (
                    "earnings_capacity_outpaces_"
                    "debt_growth"
                )
            )

        elif (
            debt_growth
            > ebit_growth
        ):
            signals.append(
                (
                    "latest_debt_growth_outpaces_"
                    "ebit_growth"
                )
            )


    if cash_debt_support is not None:
        if cash_debt_support >= 0.30:
            signals.append(
                "strong_cash_debt_support"
            )

        elif cash_debt_support >= 0.15:
            signals.append(
                "moderate_cash_debt_support"
            )

        else:
            signals.append(
                "weak_cash_debt_support"
            )

    # ==============================
    # RETURN
    # ==============================

    return {
        "status": "success",
        "latest_year": latest[
            "year"
        ],
        "debt_service_regime": (
            debt_service_regime
        ),
        "coverage_trend": (
            coverage_trend
        ),
        "latest_interest_coverage": (
            latest_interest_coverage
        ),
        "previous_interest_coverage": (
            previous_interest_coverage
        ),
        "interest_coverage_change": (
            coverage_change
        ),
        "interest_coverage_class": (
            coverage_class
        ),
        "latest_interest_burden": (
            latest_interest_burden
        ),
        "interest_burden_class": (
            burden_class
        ),
        "debt_growth": debt_growth,
        "ebit_growth": (
            ebit_growth
        ),
        "operating_cashflow": (
            operating_cashflow
        ),
        "cash_debt_support": (
            cash_debt_support
        ),
        "signals": signals,
        "history": history,
                "diagnostics": {
            "income_item_column": (
                income_item_column
            ),
            "balance_item_column": (
                balance_item_column
            ),
            "operating_profit_row": (
                operating_profit_row
            ),
            "interest_expense_row": (
                interest_expense_row
            ),
            "short_term_debt_row": (
                short_term_debt_row
            ),
            "long_term_debt_row": (
                long_term_debt_row
            ),
            "operating_profit_item": (
                income.loc[
                    operating_profit_row,
                    income_item_column,
                ]
            ),
            "interest_expense_item": (
                income.loc[
                    interest_expense_row,
                    income_item_column,
                ]
            ),
            "coverage_trend": (
                coverage_trend_diagnostics
            ),
        },
    }