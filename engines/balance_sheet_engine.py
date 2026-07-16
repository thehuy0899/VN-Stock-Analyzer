import pandas as pd


def analyze_balance_sheet(balance_sheet):
    if (
        balance_sheet is None
        or balance_sheet.empty
    ):
        return {
            "status": "error",
            "message": (
                "Không có dữ liệu "
                "bảng cân đối kế toán."
            ),
        }

    # ==============================
    # VALIDATE STRUCTURE
    # ==============================

    if "item_id" not in balance_sheet.columns:
        return {
            "status": "error",
            "message": (
                "Dữ liệu bảng cân đối kế toán "
                "không có cấu trúc phù hợp."
            ),
            "missing_columns": [
                "item_id",
            ],
        }

    # ==============================
    # FIND YEAR COLUMNS
    # ==============================

    year_columns = []

    for column in balance_sheet.columns:
        try:
            int(column)

            year_columns.append(
                column
            )

        except (
            ValueError,
            TypeError,
        ):
            continue

    if not year_columns:
        return {
            "status": "error",
            "message": (
                "Không tìm thấy cột năm."
            ),
        }

    year_columns = sorted(
        year_columns,
        key=lambda value: int(value),
    )

    latest_column = year_columns[-1]

    latest_year = int(
        latest_column
    )

    previous_column = None
    previous_year = None

    if len(year_columns) >= 2:
        previous_column = year_columns[-2]

        previous_year = int(
            previous_column
        )

    # ==============================
    # GET ITEM VALUE
    # ==============================

    def get_item_value(
        item_id,
        year_column,
    ):
        rows = balance_sheet[
            balance_sheet["item_id"]
            == item_id
        ]

        if rows.empty:
            return None

        value = rows.iloc[0][
            year_column
        ]

        if pd.isna(value):
            return None

        try:
            return float(value)

        except (
            ValueError,
            TypeError,
        ):
            return None

    # ==============================
    # CURRENT VALUES
    # ==============================

    cash = get_item_value(
        "cash_and_cash_equivalents",
        latest_column,
    )

    short_term_debt = get_item_value(
        "short_term_borrowings",
        latest_column,
    )

    long_term_debt = get_item_value(
        "long_term_borrowings",
        latest_column,
    )

    total_assets = get_item_value(
        "total_assets",
        latest_column,
    )

    equity = get_item_value(
        "owners_equity",
        latest_column,
    )

    # ==============================
    # VALIDATE ITEMS
    # ==============================

    required_items = {
        "cash": cash,
        "short_term_debt": short_term_debt,
        "long_term_debt": long_term_debt,
        "total_assets": total_assets,
        "equity": equity,
    }

    missing_items = []

    for (
        item_name,
        value,
    ) in required_items.items():
        if value is None:
            missing_items.append(
                item_name
            )

    if missing_items:
        return {
            "status": "error",
            "message": (
                "Không tìm thấy đủ chỉ tiêu "
                "cần thiết trong bảng cân đối kế toán."
            ),
            "missing_items": missing_items,
        }

    # ==============================
    # CURRENT CALCULATIONS
    # ==============================

    total_debt = (
        short_term_debt
        + long_term_debt
    )

    net_debt = (
        total_debt
        - cash
    )

    debt_to_equity = None

    if equity != 0:
        debt_to_equity = (
            total_debt
            / equity
        )

    net_debt_to_equity = None

    if equity != 0:
        net_debt_to_equity = (
            net_debt
            / equity
        )

    debt_to_assets = None

    if total_assets != 0:
        debt_to_assets = (
            total_debt
            / total_assets
        )

    equity_to_assets = None

    if total_assets != 0:
        equity_to_assets = (
            equity
            / total_assets
        )

    # ==============================
    # PREVIOUS DEBT
    # ==============================

    previous_total_debt = None
    debt_change = None

    if previous_column is not None:
        previous_short_term_debt = get_item_value(
            "short_term_borrowings",
            previous_column,
        )

        previous_long_term_debt = get_item_value(
            "long_term_borrowings",
            previous_column,
        )

        if (
            previous_short_term_debt is not None
            and previous_long_term_debt is not None
        ):
            previous_total_debt = (
                previous_short_term_debt
                + previous_long_term_debt
            )

            if previous_total_debt != 0:
                debt_change = (
                    (
                        total_debt
                        - previous_total_debt
                    )
                    / abs(
                        previous_total_debt
                    )
                    * 100
                )

    # ==============================
    # SIGNALS
    # ==============================

    signals = []

    # NET DEBT POSITION

    if net_debt <= 0:
        signals.append(
            "net_cash_position"
        )

    else:
        signals.append(
            "net_debt_position"
        )

    # FINANCIAL LEVERAGE

    if debt_to_equity is not None:
        if debt_to_equity < 0.5:
            signals.append(
                "low_financial_leverage"
            )

        elif debt_to_equity <= 1.0:
            signals.append(
                "moderate_financial_leverage"
            )

        else:
            signals.append(
                "high_financial_leverage"
            )

    # DEBT / ASSETS

    if debt_to_assets is not None:
        if debt_to_assets >= 0.5:
            signals.append(
                "debt_heavy_balance_sheet"
            )

    # EQUITY BUFFER

    if equity_to_assets is not None:
        if equity_to_assets >= 0.5:
            signals.append(
                "strong_equity_buffer"
            )

        elif equity_to_assets < 0.3:
            signals.append(
                "weak_equity_buffer"
            )

    # DEBT TREND

    if debt_change is not None:
        if debt_change > 10:
            signals.append(
                "debt_increasing"
            )

        elif debt_change < -10:
            signals.append(
                "debt_decreasing"
            )

        else:
            signals.append(
                "debt_stable"
            )

    # ==============================
    # RESULT
    # ==============================

    return {
        "status": "success",
        "latest_year": latest_year,
        "previous_year": previous_year,
        "cash": cash,
        "short_term_debt": short_term_debt,
        "long_term_debt": long_term_debt,
        "total_debt": total_debt,
        "net_debt": net_debt,
        "total_assets": total_assets,
        "equity": equity,
        "debt_to_equity": debt_to_equity,
        "net_debt_to_equity": (
            net_debt_to_equity
        ),
        "debt_to_assets": debt_to_assets,
        "equity_to_assets": equity_to_assets,
        "previous_total_debt": (
            previous_total_debt
        ),
        "debt_change": debt_change,
        "signals": signals,
    }