import pandas as pd


# ==============================
# NORMALIZE TEXT
# ==============================


def _normalize_text(
    value,
):
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


# ==============================
# CONVERT NUMBER
# ==============================


def _to_number(
    value,
):
    if value is None:
        return None

    try:
        value = pd.to_numeric(
            value,
            errors="coerce",
        )
    except Exception:
        return None

    if pd.isna(value):
        return None

    return float(value)


# ==============================
# FIND YEAR COLUMNS
# ==============================


def _find_year_columns(
    cashflow,
):
    year_columns = []

    for column in cashflow.columns:
        column_text = str(
            column
        ).strip()

        if (
            len(column_text) == 4
            and column_text.isdigit()
        ):
            year = int(
                column_text
            )

            if (
                1900
                <= year
                <= 2100
            ):
                year_columns.append(
                    (
                        year,
                        column,
                    )
                )

    year_columns.sort(
        key=lambda item: item[0]
    )

    return year_columns


# ==============================
# FIND ITEM ROW
# ==============================


def _find_item_row(
    cashflow,
    item_ids=None,
    item_en_keywords=None,
    item_keywords=None,
):
    item_ids = {
        _normalize_text(item)
        for item in (
            item_ids or []
        )
    }

    item_en_keywords = [
        str(keyword).lower()
        for keyword in (
            item_en_keywords or []
        )
    ]

    item_keywords = [
        str(keyword).lower()
        for keyword in (
            item_keywords or []
        )
    ]

    # ==============================
    # ITEM ID
    # ==============================

    if "item_id" in cashflow.columns:
        for index, value in (
            cashflow["item_id"].items()
        ):
            normalized_value = (
                _normalize_text(
                    value
                )
            )

            if (
                normalized_value
                in item_ids
            ):
                return index

    # ==============================
    # ITEM EN
    # ==============================

    if "item_en" in cashflow.columns:
        for index, value in (
            cashflow["item_en"].items()
        ):
            value_text = (
                str(value).lower()
            )

            for keyword in (
                item_en_keywords
            ):
                if (
                    keyword
                    in value_text
                ):
                    return index

    # ==============================
    # ITEM VI
    # ==============================

    if "item" in cashflow.columns:
        for index, value in (
            cashflow["item"].items()
        ):
            value_text = (
                str(value).lower()
            )

            for keyword in (
                item_keywords
            ):
                if (
                    keyword
                    in value_text
                ):
                    return index

    return None


# ==============================
# BUILD HISTORY
# ==============================


def _build_history(
    cashflow,
    row_index,
    year_columns,
):
    history = []

    if row_index is None:
        return history

    for year, column in year_columns:
        value = _to_number(
            cashflow.at[
                row_index,
                column,
            ]
        )

        history.append(
            {
                "year": year,
                "value": value,
            }
        )

    return history


# ==============================
# CALCULATE GROWTH
# ==============================


def _calculate_growth(
    current,
    previous,
):
    if (
        current is None
        or previous is None
        or previous == 0
    ):
        return None

    return (
        (
            current
            - previous
        )
        / abs(previous)
        * 100
    )


# ==============================
# CLASSIFY CASHFLOW REGIME
# ==============================


def _classify_cashflow_regime(
    valid_history,
    signals,
    capex_coverage,
):
    signals = set(
        signals or []
    )

    latest = valid_history[-1]

    operating_cashflow = latest.get(
        "operating_cashflow"
    )

    free_cashflow = latest.get(
        "free_cashflow"
    )

    # ==============================
    # OCF NEGATIVE
    # ==============================

    if (
        operating_cashflow is not None
        and operating_cashflow <= 0
    ):
        return (
            "operating_cashflow_stress"
        )

    # ==============================
    # MULTI-YEAR NEGATIVE FCF
    # ==============================

    if (
        "multi_year_negative_free_cashflow"
        in signals
    ):
        if (
            "capex_accelerating"
            in signals
        ):
            return (
                "persistent_investment_pressure"
            )

        return (
            "persistent_negative_fcf"
        )

    # ==============================
    # FCF TURNED NEGATIVE
    # ==============================

    if (
        "free_cashflow_turned_negative"
        in signals
    ):
        if (
            "capex_accelerating"
            in signals
        ):
            return (
                "investment_acceleration"
            )

        return (
            "emerging_fcf_pressure"
        )

    # ==============================
    # NEGATIVE FCF
    # ==============================

    if (
        free_cashflow is not None
        and free_cashflow < 0
    ):
        if (
            capex_coverage is not None
            and capex_coverage >= 0.7
        ):
            return (
                "investment_pressure"
            )

        return (
            "funding_pressure"
        )

    # ==============================
    # FCF RECOVERY
    # ==============================

    if (
        "free_cashflow_recovered"
        in signals
    ):
        return (
            "cashflow_recovery"
        )

    # ==============================
    # POSITIVE AND IMPROVING
    # ==============================

    if (
        free_cashflow is not None
        and free_cashflow > 0
        and (
            "free_cashflow_improving"
            in signals
        )
    ):
        return (
            "cashflow_expansion"
        )

    # ==============================
    # POSITIVE STABLE
    # ==============================

    if (
        free_cashflow is not None
        and free_cashflow > 0
    ):
        return (
            "healthy_cash_generation"
        )

    return "neutral"


# ==============================
# ANALYZE CASHFLOW TREND
# ==============================


def analyze_cashflow_trend(
    cashflow,
):
    if cashflow is None:
        return {
            "status": "error",
            "message": (
                "Cashflow data is None."
            ),
        }

    if not isinstance(
        cashflow,
        pd.DataFrame,
    ):
        return {
            "status": "error",
            "message": (
                "Cashflow data must be "
                "a pandas DataFrame."
            ),
        }

    if cashflow.empty:
        return {
            "status": "error",
            "message": (
                "Cashflow data is empty."
            ),
        }

    # ==============================
    # YEAR COLUMNS
    # ==============================

    year_columns = (
        _find_year_columns(
            cashflow
        )
    )

    if len(year_columns) < 2:
        return {
            "status": "error",
            "message": (
                "Not enough annual "
                "cashflow periods."
            ),
            "year_columns": [
                str(column)
                for _, column
                in year_columns
            ],
        }

    # ==============================
    # FIND OPERATING CASHFLOW
    # ==============================

    operating_cashflow_row = (
        _find_item_row(
            cashflow,
            item_ids=[
                (
                    "net_cash_flows_"
                    "from_operating_"
                    "activities"
                ),
                (
                    "net_cash_flow_"
                    "from_operating_"
                    "activities"
                ),
                (
                    "net_cash_inflows_"
                    "outflows_from_"
                    "operating_activities"
                ),
                (
                    "cash_flows_from_"
                    "operating_activities"
                ),
                "operating_cash_flow",
                "operating_cashflow",
            ],
            item_en_keywords=[
                (
                    "net cash flows "
                    "from operating "
                    "activities"
                ),
                (
                    "net cash flow "
                    "from operating "
                    "activities"
                ),
                (
                    "net cash inflows/"
                    "outflows from "
                    "operating activities"
                ),
                (
                    "cash flows from "
                    "operating activities"
                ),
            ],
            item_keywords=[
                (
                    "lưu chuyển tiền thuần "
                    "từ hoạt động kinh doanh"
                ),
                (
                    "lưu chuyển tiền thuần "
                    "trong kỳ từ hoạt động "
                    "kinh doanh"
                ),
                (
                    "tiền thuần từ hoạt động "
                    "kinh doanh"
                ),
            ],
        )
    )

    # ==============================
    # FIND CAPEX
    # ==============================

    capex_row = _find_item_row(
        cashflow,
        item_ids=[
            "purchase_of_fixed_assets",
            (
                "purchase_of_property_"
                "plant_and_equipment"
            ),
            "purchases_of_fixed_assets",
            "acquisition_of_fixed_assets",
            (
                "cash_paid_for_purchase_"
                "construction_of_fixed_assets"
            ),
            (
                "purchase_and_construction_"
                "of_fixed_assets"
            ),
        ],
        item_en_keywords=[
            "purchase of fixed assets",
            "purchases of fixed assets",
            (
                "purchase of property, "
                "plant and equipment"
            ),
            (
                "cash paid for purchase "
                "and construction of "
                "fixed assets"
            ),
            (
                "purchase and construction "
                "of fixed assets"
            ),
        ],
        item_keywords=[
            (
                "tiền chi để mua sắm, "
                "xây dựng tscđ"
            ),
            (
                "tiền chi mua sắm, "
                "xây dựng tscđ"
            ),
            (
                "mua sắm, xây dựng "
                "tài sản cố định"
            ),
            (
                "chi mua sắm tài sản "
                "cố định"
            ),
        ],
    )

    # ==============================
    # VALIDATE ITEMS
    # ==============================

    missing_items = []

    if (
        operating_cashflow_row
        is None
    ):
        missing_items.append(
            "operating_cashflow"
        )

    if capex_row is None:
        missing_items.append(
            "capex"
        )

    if missing_items:
        return {
            "status": "error",
            "message": (
                "Required cashflow "
                "items were not found."
            ),
            "missing_items": (
                missing_items
            ),
            "available_item_ids": (
                cashflow.get(
                    "item_id",
                    pd.Series(
                        dtype=object
                    ),
                )
                .dropna()
                .astype(str)
                .tolist()
            ),
        }

    # ==============================
    # BUILD HISTORY
    # ==============================

    operating_cashflow_history = (
        _build_history(
            cashflow,
            operating_cashflow_row,
            year_columns,
        )
    )

    capex_history = _build_history(
        cashflow,
        capex_row,
        year_columns,
    )

    cashflow_history = []

    for (
        operating_item,
        capex_item,
    ) in zip(
        operating_cashflow_history,
        capex_history,
    ):
        year = operating_item[
            "year"
        ]

        operating_cashflow = (
            operating_item["value"]
        )

        capex = capex_item[
            "value"
        ]

        free_cashflow = None

        if (
            operating_cashflow
            is not None
            and capex is not None
        ):
            free_cashflow = (
                operating_cashflow
                + capex
            )

        cashflow_history.append(
            {
                "year": year,
                "operating_cashflow": (
                    operating_cashflow
                ),
                "capex": capex,
                "free_cashflow": (
                    free_cashflow
                ),
            }
        )

    # ==============================
    # VALID HISTORY
    # ==============================

    valid_history = [
        item
        for item in cashflow_history
        if (
            item[
                "operating_cashflow"
            ]
            is not None
            and item["capex"]
            is not None
            and item[
                "free_cashflow"
            ]
            is not None
        )
    ]

    if len(valid_history) < 2:
        return {
            "status": "error",
            "message": (
                "Not enough valid "
                "cashflow periods."
            ),
            "cashflow_history": (
                cashflow_history
            ),
        }

    latest = valid_history[-1]
    previous = valid_history[-2]

    # ==============================
    # CURRENT VALUES
    # ==============================

    latest_year = latest["year"]

    operating_cashflow = latest[
        "operating_cashflow"
    ]

    capex = latest["capex"]

    free_cashflow = latest[
        "free_cashflow"
    ]

    previous_operating_cashflow = (
        previous[
            "operating_cashflow"
        ]
    )

    previous_capex = previous[
        "capex"
    ]

    previous_free_cashflow = (
        previous[
            "free_cashflow"
        ]
    )

    # ==============================
    # CHANGES
    # ==============================

    operating_cashflow_change = (
        _calculate_growth(
            operating_cashflow,
            previous_operating_cashflow,
        )
    )

    capex_change = _calculate_growth(
        abs(capex),
        abs(previous_capex),
    )

    free_cashflow_change = (
        _calculate_growth(
            free_cashflow,
            previous_free_cashflow,
        )
    )

    # ==============================
    # SIGNALS
    # ==============================

    signals = []

    # ==============================
    # OCF TREND
    # ==============================

    if (
        operating_cashflow > 0
        and previous_operating_cashflow > 0
    ):
        if (
            operating_cashflow_change
            is not None
            and operating_cashflow_change
            >= 15
        ):
            signals.append(
                "operating_cashflow_improving"
            )

        elif (
            operating_cashflow_change
            is not None
            and operating_cashflow_change
            <= -15
        ):
            signals.append(
                "operating_cashflow_weakening"
            )

        else:
            signals.append(
                "operating_cashflow_stable"
            )

    elif (
        operating_cashflow > 0
        and previous_operating_cashflow <= 0
    ):
        signals.append(
            "operating_cashflow_recovered"
        )

    elif operating_cashflow <= 0:
        signals.append(
            "operating_cashflow_negative"
        )

    # ==============================
    # CAPEX TREND
    # ==============================

    if (
        capex_change is not None
        and capex_change >= 20
    ):
        signals.append(
            "capex_accelerating"
        )

    elif (
        capex_change is not None
        and capex_change <= -20
    ):
        signals.append(
            "capex_moderating"
        )

    else:
        signals.append(
            "capex_stable"
        )

    # ==============================
    # FCF TREND
    # ==============================

    if (
        free_cashflow > 0
        and previous_free_cashflow > 0
    ):
        if (
            free_cashflow_change
            is not None
            and free_cashflow_change
            >= 15
        ):
            signals.append(
                "free_cashflow_improving"
            )

        elif (
            free_cashflow_change
            is not None
            and free_cashflow_change
            <= -15
        ):
            signals.append(
                "free_cashflow_weakening"
            )

        else:
            signals.append(
                "free_cashflow_stable"
            )

    elif (
        free_cashflow < 0
        and previous_free_cashflow >= 0
    ):
        signals.append(
            "free_cashflow_turned_negative"
        )

    elif (
        free_cashflow > 0
        and previous_free_cashflow <= 0
    ):
        signals.append(
            "free_cashflow_recovered"
        )

    elif (
        free_cashflow < 0
        and previous_free_cashflow < 0
    ):
        signals.append(
            "persistent_negative_free_cashflow"
        )

    # ==============================
    # MULTI-YEAR PATTERNS
    # ==============================

    recent_history = (
        valid_history[-3:]
    )

    recent_fcf = [
        item["free_cashflow"]
        for item in recent_history
    ]

    if (
        len(recent_fcf) >= 3
        and all(
            value < 0
            for value in recent_fcf
        )
    ):
        signals.append(
            "multi_year_negative_free_cashflow"
        )

    recent_ocf = [
        item["operating_cashflow"]
        for item in recent_history
    ]

    if (
        len(recent_ocf) >= 3
        and all(
            value > 0
            for value in recent_ocf
        )
    ):
        signals.append(
            "consistent_positive_operating_cashflow"
        )

    # ==============================
    # CAPEX COVERAGE
    # ==============================

    capex_coverage = None

    if (
        capex is not None
        and capex != 0
    ):
        capex_coverage = (
            operating_cashflow
            / abs(capex)
        )

        if capex_coverage >= 1:
            signals.append(
                "operating_cashflow_covers_capex"
            )

        elif capex_coverage >= 0.7:
            signals.append(
                "partial_capex_self_funding"
            )

        else:
            signals.append(
                "weak_capex_self_funding"
            )

    # ==============================
    # CASHFLOW REGIME
    # ==============================

    cashflow_regime = (
        _classify_cashflow_regime(
            valid_history,
            signals,
            capex_coverage,
        )
    )

    # ==============================
    # RETURN
    # ==============================

    return {
        "status": "success",
        "cashflow_regime": (
            cashflow_regime
        ),
        "latest_year": latest_year,
        "operating_cashflow": (
            operating_cashflow
        ),
        "previous_operating_cashflow": (
            previous_operating_cashflow
        ),
        "operating_cashflow_change": (
            operating_cashflow_change
        ),
        "capex": capex,
        "previous_capex": previous_capex,
        "capex_change": capex_change,
        "free_cashflow": free_cashflow,
        "previous_free_cashflow": (
            previous_free_cashflow
        ),
        "free_cashflow_change": (
            free_cashflow_change
        ),
        "capex_coverage": capex_coverage,
        "cashflow_history": (
            cashflow_history
        ),
        "signals": signals,
        "diagnostics": {
            "operating_cashflow_row": (
                operating_cashflow_row
            ),
            "capex_row": capex_row,
            "year_columns": [
                year
                for year, _
                in year_columns
            ],
            "valid_periods": len(
                valid_history
            ),
        },
    }