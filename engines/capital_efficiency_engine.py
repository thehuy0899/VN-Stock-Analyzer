import re
import unicodedata

import pandas as pd


# ============================================================
# TEXT HELPERS
# ============================================================


def _normalize_text(value):
    if value is None:
        return ""

    text = str(value).strip().lower()

    text = unicodedata.normalize(
        "NFD",
        text,
    )

    text = "".join(
        char
        for char in text
        if unicodedata.category(char)
        != "Mn"
    )

    text = text.replace(
        "đ",
        "d",
    )

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def _detect_item_column(df):
    candidates = [
        "item",
        "name",
        "indicator",
        "metric",
    ]

    normalized_columns = {
        _normalize_text(column): column
        for column in df.columns
    }

    for candidate in candidates:
        normalized_candidate = (
            _normalize_text(candidate)
        )

        if (
            normalized_candidate
            in normalized_columns
        ):
            return normalized_columns[
                normalized_candidate
            ]

    return None


def _extract_year_columns(df):
    year_columns = []

    for column in df.columns:
        try:
            year = int(column)

            if 1900 <= year <= 2100:
                year_columns.append(
                    (
                        year,
                        column,
                    )
                )

        except (
            ValueError,
            TypeError,
        ):
            continue

    year_columns.sort(
        key=lambda item: item[0]
    )

    return year_columns


def _safe_float(value):
    try:
        if pd.isna(value):
            return None

        return float(value)

    except (
        ValueError,
        TypeError,
    ):
        return None


# ============================================================
# ITEM MATCHING
# ============================================================


def _find_item_row(
    df,
    item_column,
    keywords,
):
    if (
        df is None
        or df.empty
        or item_column not in df.columns
    ):
        return None

    normalized_items = (
        df[item_column]
        .astype(str)
        .map(_normalize_text)
    )

    normalized_keywords = [
        _normalize_text(keyword)
        for keyword in keywords
    ]

    # --------------------------------------------------------
    # EXACT MATCH
    # --------------------------------------------------------

    for keyword in normalized_keywords:
        matched = df[
            normalized_items == keyword
        ]

        if not matched.empty:
            return matched.iloc[0]

    # --------------------------------------------------------
    # CONTAINS MATCH
    # --------------------------------------------------------

    for keyword in normalized_keywords:
        matched = df[
            normalized_items.str.contains(
                keyword,
                regex=False,
                na=False,
            )
        ]

        if not matched.empty:
            return matched.iloc[0]

    return None


def _find_debt_row(
    df,
    item_column,
    debt_type,
):
    if (
        df is None
        or df.empty
        or item_column not in df.columns
    ):
        return None

    normalized_items = (
        df[item_column]
        .astype(str)
        .map(_normalize_text)
    )

    # ========================================================
    # SHORT-TERM DEBT
    # ========================================================

    if debt_type == "short_term":
        exact_keywords = [
            "vay va no thue tai chinh ngan han",
            "vay ngan han",
            "no vay ngan han",
            "no ngan han co lai",
            "short term borrowings",
            "short term debt",
            "current borrowings",
        ]

        required_period_tokens = [
            "ngan han",
            "short term",
            "current",
        ]

    # ========================================================
    # LONG-TERM DEBT
    # ========================================================

    elif debt_type == "long_term":
        exact_keywords = [
            "vay va no thue tai chinh dai han",
            "vay dai han",
            "no vay dai han",
            "no dai han co lai",
            "long term borrowings",
            "long term debt",
            "non current borrowings",
        ]

        required_period_tokens = [
            "dai han",
            "long term",
            "non current",
        ]

    else:
        return None

    # --------------------------------------------------------
    # EXACT / CONTAINS ALIAS MATCH
    # --------------------------------------------------------

    for keyword in exact_keywords:
        normalized_keyword = (
            _normalize_text(keyword)
        )

        matched = df[
            normalized_items
            == normalized_keyword
        ]

        if not matched.empty:
            return matched.iloc[0]

    for keyword in exact_keywords:
        normalized_keyword = (
            _normalize_text(keyword)
        )

        matched = df[
            normalized_items.str.contains(
                normalized_keyword,
                regex=False,
                na=False,
            )
        ]

        if not matched.empty:
            return matched.iloc[0]

    # --------------------------------------------------------
    # TOKEN FALLBACK
    # --------------------------------------------------------

    debt_tokens = [
        "vay",
        "no vay",
        "no thue tai chinh",
        "borrowings",
        "debt",
    ]

    for index, item in normalized_items.items():
        has_debt_token = any(
            token in item
            for token in debt_tokens
        )

        has_period_token = any(
            token in item
            for token in required_period_tokens
        )

        if (
            has_debt_token
            and has_period_token
        ):
            return df.loc[index]

    return None


# ============================================================
# CLASSIFICATION
# ============================================================


def _classify_roic(roic):
    if roic is None:
        return None

    if roic >= 0.15:
        return "excellent"

    if roic >= 0.10:
        return "strong"

    if roic >= 0.07:
        return "moderate"

    return "weak"


def _classify_incremental_roic(
    incremental_roic,
):
    if incremental_roic is None:
        return None

    if incremental_roic >= 0.20:
        return "excellent"

    if incremental_roic >= 0.12:
        return "strong"

    if incremental_roic >= 0.07:
        return "moderate"

    if incremental_roic >= 0:
        return "weak"

    return "negative"


# ============================================================
# MAIN ENGINE
# ============================================================


def analyze_capital_efficiency(
    income,
    balance_sheet,
):
    # ========================================================
    # VALIDATION
    # ========================================================

    if (
        income is None
        or balance_sheet is None
        or income.empty
        or balance_sheet.empty
    ):
        return {
            "status": "error",
            "message": (
                "Income statement or balance sheet "
                "is empty."
            ),
        }

    income_item_column = (
        _detect_item_column(
            income
        )
    )

    balance_item_column = (
        _detect_item_column(
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
                "could not be detected."
            ),
        }

    # ========================================================
    # FIND INCOME ROWS
    # ========================================================

    operating_profit_row = (
        _find_item_row(
            income,
            income_item_column,
            [
                "lãi/(lỗ) từ hoạt động kinh doanh",
                "lợi nhuận từ hoạt động kinh doanh",
                "operating profit",
            ],
        )
    )

    profit_before_tax_row = (
        _find_item_row(
            income,
            income_item_column,
            [
                "lãi/(lỗ) trước thuế",
                "lợi nhuận trước thuế",
                "profit before tax",
            ],
        )
    )

    tax_expense_row = (
        _find_item_row(
            income,
            income_item_column,
            [
                "chi phí thuế thu nhập doanh nghiệp",
                "income tax expense",
            ],
        )
    )

    # ========================================================
    # FIND BALANCE SHEET ROWS
    # ========================================================

    cash_row = (
        _find_item_row(
            balance_sheet,
            balance_item_column,
            [
                "tiền và tương đương tiền",
                "tiền và các khoản tương đương tiền",
                "cash and cash equivalents",
            ],
        )
    )

    short_term_debt_row = (
        _find_debt_row(
            balance_sheet,
            balance_item_column,
            "short_term",
        )
    )

    long_term_debt_row = (
        _find_debt_row(
            balance_sheet,
            balance_item_column,
            "long_term",
        )
    )

    equity_row = (
        _find_item_row(
            balance_sheet,
            balance_item_column,
            [
                "vốn chủ sở hữu",
                "owners equity",
                "total equity",
                "equity",
            ],
        )
    )

    # ========================================================
    # DIAGNOSTICS
    # ========================================================

    diagnostics = {
        "income_item_column": (
            income_item_column
        ),
        "balance_item_column": (
            balance_item_column
        ),
        "operating_profit_row": (
            None
            if operating_profit_row is None
            else operating_profit_row.name
        ),
        "profit_before_tax_row": (
            None
            if profit_before_tax_row is None
            else profit_before_tax_row.name
        ),
        "tax_expense_row": (
            None
            if tax_expense_row is None
            else tax_expense_row.name
        ),
        "cash_row": (
            None
            if cash_row is None
            else cash_row.name
        ),
        "short_term_debt_row": (
            None
            if short_term_debt_row is None
            else short_term_debt_row.name
        ),
        "long_term_debt_row": (
            None
            if long_term_debt_row is None
            else long_term_debt_row.name
        ),
        "equity_row": (
            None
            if equity_row is None
            else equity_row.name
        ),
        "short_term_debt_item": (
            None
            if short_term_debt_row is None
            else short_term_debt_row[
                balance_item_column
            ]
        ),
        "long_term_debt_item": (
            None
            if long_term_debt_row is None
            else long_term_debt_row[
                balance_item_column
            ]
        ),
    }

    # ========================================================
    # REQUIRED ITEMS
    # ========================================================

    missing_items = []

    if operating_profit_row is None:
        missing_items.append(
            "operating_profit"
        )

    if equity_row is None:
        missing_items.append(
            "equity"
        )

    if cash_row is None:
        missing_items.append(
            "cash"
        )

    if (
        short_term_debt_row is None
        and long_term_debt_row is None
    ):
        missing_items.append(
            "interest_bearing_debt"
        )

    if missing_items:
        return {
            "status": "error",
            "message": (
                "Required financial items "
                "were not found."
            ),
            "missing_items": missing_items,
            "diagnostics": diagnostics,
        }

    # ========================================================
    # YEAR COLUMNS
    # ========================================================

    income_years = dict(
        _extract_year_columns(
            income
        )
    )

    balance_years = dict(
        _extract_year_columns(
            balance_sheet
        )
    )

    common_years = sorted(
        set(
            income_years.keys()
        )
        & set(
            balance_years.keys()
        )
    )

    if len(common_years) < 2:
        return {
            "status": "error",
            "message": (
                "At least two common financial "
                "periods are required."
            ),
            "diagnostics": diagnostics,
        }

    # ========================================================
    # BUILD CAPITAL HISTORY
    # ========================================================

    history = []

    for year in common_years:
        income_column = (
            income_years[year]
        )

        balance_column = (
            balance_years[year]
        )

        operating_profit = (
            _safe_float(
                operating_profit_row[
                    income_column
                ]
            )
        )

        profit_before_tax = (
            None
            if profit_before_tax_row is None
            else _safe_float(
                profit_before_tax_row[
                    income_column
                ]
            )
        )

        tax_expense = (
            None
            if tax_expense_row is None
            else _safe_float(
                tax_expense_row[
                    income_column
                ]
            )
        )

        cash = _safe_float(
            cash_row[
                balance_column
            ]
        )

        short_term_debt = (
            0.0
            if short_term_debt_row is None
            else (
                _safe_float(
                    short_term_debt_row[
                        balance_column
                    ]
                )
                or 0.0
            )
        )

        long_term_debt = (
            0.0
            if long_term_debt_row is None
            else (
                _safe_float(
                    long_term_debt_row[
                        balance_column
                    ]
                )
                or 0.0
            )
        )

        equity = _safe_float(
            equity_row[
                balance_column
            ]
        )

        if (
            operating_profit is None
            or cash is None
            or equity is None
        ):
            continue

        # ====================================================
        # EFFECTIVE TAX RATE
        # ====================================================

        tax_rate = 0.20

        if (
            profit_before_tax is not None
            and tax_expense is not None
            and profit_before_tax > 0
        ):
            calculated_tax_rate = (
                tax_expense
                / profit_before_tax
            )

            if (
                0
                <= calculated_tax_rate
                <= 0.50
            ):
                tax_rate = (
                    calculated_tax_rate
                )

        # ====================================================
        # NOPAT
        # ====================================================

        nopat = (
            operating_profit
            * (
                1
                - tax_rate
            )
        )

        # ====================================================
        # INVESTED CAPITAL
        # ====================================================

        total_debt = (
            short_term_debt
            + long_term_debt
        )

        invested_capital = (
            equity
            + total_debt
            - cash
        )

        if invested_capital <= 0:
            continue

        # ====================================================
        # ROIC
        # ====================================================

        roic = (
            nopat
            / invested_capital
        )

        history.append(
            {
                "year": year,
                "operating_profit": (
                    operating_profit
                ),
                "tax_rate": tax_rate,
                "nopat": nopat,
                "cash": cash,
                "short_term_debt": (
                    short_term_debt
                ),
                "long_term_debt": (
                    long_term_debt
                ),
                "total_debt": total_debt,
                "equity": equity,
                "invested_capital": (
                    invested_capital
                ),
                "roic": roic,
            }
        )

    # ========================================================
    # VALIDATE HISTORY
    # ========================================================

    if len(history) < 2:
        return {
            "status": "error",
            "message": (
                "Insufficient capital efficiency "
                "history."
            ),
            "diagnostics": diagnostics,
        }

    # ========================================================
    # INCREMENTAL ROIC HISTORY
    # ========================================================

    for index in range(
        len(history)
    ):
        history[index][
            "incremental_roic"
        ] = None

        if index == 0:
            continue

        current = history[index]
        previous = history[
            index - 1
        ]

        delta_nopat = (
            current["nopat"]
            - previous["nopat"]
        )

        delta_invested_capital = (
            current["invested_capital"]
            - previous["invested_capital"]
        )

        current[
            "delta_nopat"
        ] = delta_nopat

        current[
            "delta_invested_capital"
        ] = delta_invested_capital

        if (
            delta_invested_capital
            > 0
        ):
            current[
                "incremental_roic"
            ] = (
                delta_nopat
                / delta_invested_capital
            )

    # ========================================================
    # LATEST METRICS
    # ========================================================

    latest = history[-1]
    previous = history[-2]

    latest_roic = latest[
        "roic"
    ]

    previous_roic = previous[
        "roic"
    ]

    roic_change = (
        latest_roic
        - previous_roic
    )

    incremental_roic = latest.get(
        "incremental_roic"
    )

    roic_class = _classify_roic(
        latest_roic
    )

    incremental_roic_class = (
        _classify_incremental_roic(
            incremental_roic
        )
    )

    # ========================================================
    # CAPITAL EFFICIENCY REGIME
    # ========================================================

    recent_roic_history = [
        item["roic"]
        for item in history[-3:]
    ]

    roic_improving = False

    if len(recent_roic_history) >= 3:
        roic_improving = (
            recent_roic_history[-1]
            > recent_roic_history[-2]
            > recent_roic_history[-3]
        )

    if (
        incremental_roic is not None
        and incremental_roic >= 0.12
        and roic_improving
    ):
        capital_efficiency_regime = (
            "improving_with_strong_incremental_returns"
        )

    elif (
        incremental_roic is not None
        and incremental_roic >= 0.12
    ):
        capital_efficiency_regime = (
            "strong_incremental_returns"
        )

    elif roic_improving:
        capital_efficiency_regime = (
            "improving_capital_efficiency"
        )

    elif roic_change < -0.01:
        capital_efficiency_regime = (
            "deteriorating_capital_efficiency"
        )

    else:
        capital_efficiency_regime = (
            "stable_capital_efficiency"
        )

    # ========================================================
    # CAPITAL EFFICIENCY PROFILE
    # ========================================================

    capital_efficiency_profile = None

    # --------------------------------------------------------
    # LOW BASE + PRODUCTIVE NEW CAPITAL
    # --------------------------------------------------------

    if (
        latest_roic < 0.07
        and roic_improving
        and incremental_roic is not None
        and incremental_roic >= 0.12
        and incremental_roic > latest_roic
    ):
        capital_efficiency_profile = (
            "low_base_with_improving_capital_productivity"
        )

    # --------------------------------------------------------
    # STRONG BASE + PRODUCTIVE NEW CAPITAL
    # --------------------------------------------------------

    elif (
        latest_roic >= 0.10
        and incremental_roic is not None
        and incremental_roic >= 0.12
        and incremental_roic > latest_roic
    ):
        capital_efficiency_profile = (
            "strong_base_with_productive_incremental_capital"
        )

    # --------------------------------------------------------
    # MODERATE BASE + PRODUCTIVE NEW CAPITAL
    # --------------------------------------------------------

    elif (
        latest_roic >= 0.07
        and incremental_roic is not None
        and incremental_roic >= 0.12
        and incremental_roic > latest_roic
    ):
        capital_efficiency_profile = (
            "moderate_base_with_productive_incremental_capital"
        )

    # --------------------------------------------------------
    # IMPROVING EXISTING CAPITAL BASE
    # --------------------------------------------------------

    elif roic_improving:
        capital_efficiency_profile = (
            "improving_existing_capital_productivity"
        )

    # --------------------------------------------------------
    # NEW CAPITAL UNDERPERFORMS EXISTING BASE
    # --------------------------------------------------------

    elif (
        incremental_roic is not None
        and incremental_roic >= 0
        and incremental_roic < latest_roic
    ):
        capital_efficiency_profile = (
            "incremental_capital_underperforming_existing_base"
        )

    # --------------------------------------------------------
    # DESTRUCTIVE INCREMENTAL CAPITAL
    # --------------------------------------------------------

    elif (
        incremental_roic is not None
        and incremental_roic < 0
    ):
        capital_efficiency_profile = (
            "destructive_incremental_capital"
        )

    # --------------------------------------------------------
    # STABLE PROFILE
    # --------------------------------------------------------

    else:
        capital_efficiency_profile = (
            "stable_capital_productivity"
        )

    # ========================================================
    # SIGNALS
    # ========================================================

    signals = []

    if latest_roic >= 0.10:
        signals.append(
            "strong_roic"
        )

    elif latest_roic < 0.07:
        signals.append(
            "weak_roic"
        )

    if roic_change >= 0.01:
        signals.append(
            "roic_improving"
        )

    elif roic_change <= -0.01:
        signals.append(
            "roic_deteriorating"
        )

    if roic_improving:
        signals.append(
            "persistent_roic_improvement"
        )

    if incremental_roic is not None:
        if incremental_roic >= 0.12:
            signals.append(
                "strong_incremental_roic"
            )

        elif incremental_roic < 0:
            signals.append(
                "negative_incremental_roic"
            )

        if (
            incremental_roic
            > latest_roic
        ):
            signals.append(
                "incremental_returns_above_existing_base"
            )

    if (
        roic_improving
        and incremental_roic is not None
        and incremental_roic >= 0.12
    ):
        signals.append(
            "capital_deployment_quality_improving"
        )

    # ========================================================
    # CAPITAL EFFICIENCY PROFILE SIGNALS
    # ========================================================

    if (
        capital_efficiency_profile
        == "low_base_with_improving_capital_productivity"
    ):
        signals.append(
            "low_existing_capital_efficiency"
        )

        signals.append(
            "incremental_capital_materially_more_productive"
        )

        signals.append(
            "capital_productivity_recovery"
        )

    elif (
        capital_efficiency_profile
        == "strong_base_with_productive_incremental_capital"
    ):
        signals.append(
            "strong_existing_capital_efficiency"
        )

        signals.append(
            "incremental_capital_materially_more_productive"
        )

        signals.append(
            "capital_productivity_compounding"
        )

    elif (
        capital_efficiency_profile
        == "moderate_base_with_productive_incremental_capital"
    ):
        signals.append(
            "moderate_existing_capital_efficiency"
        )

        signals.append(
            "incremental_capital_materially_more_productive"
        )

        signals.append(
            "capital_productivity_improving"
        )

    elif (
        capital_efficiency_profile
        == "improving_existing_capital_productivity"
    ):
        signals.append(
            "existing_capital_productivity_improving"
        )

    elif (
        capital_efficiency_profile
        == "incremental_capital_underperforming_existing_base"
    ):
        signals.append(
            "incremental_capital_underperforming"
        )

    elif (
        capital_efficiency_profile
        == "destructive_incremental_capital"
    ):
        signals.append(
            "incremental_capital_value_destructive"
        )

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "status": "success",
        "latest_year": latest.get(
            "year"
        ),
        "capital_efficiency_regime": (
            capital_efficiency_regime
        ),
        "capital_efficiency_profile": (
            capital_efficiency_profile
        ),
        "latest_roic": latest_roic,
        "previous_roic": previous_roic,
        "roic_change": roic_change,
        "roic_class": roic_class,
        "incremental_roic": (
            incremental_roic
        ),
        "incremental_roic_class": (
            incremental_roic_class
        ),
        "signals": signals,
        "history": history,
        "diagnostics": diagnostics,
    }