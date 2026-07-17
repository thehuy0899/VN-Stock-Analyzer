import pandas as pd


def _value(
    df: pd.DataFrame,
    item_id: str,
    year=None,
):
    row = df[df["item_id"] == item_id]

    if row.empty:
        return None

    numeric_cols = [
        c for c in row.columns
        if str(c).isdigit()
    ]

    if not numeric_cols:
        return None

    numeric_cols = sorted(numeric_cols)

    if year is None:
        year = numeric_cols[-1]

    if year not in row.columns:
        return None

    value = row.iloc[0][year]

    if pd.isna(value):
        return None

    return float(value)


def analyze(
    income: pd.DataFrame,
    balance: pd.DataFrame,
):
    years = sorted(
        [
            c
            for c in balance.columns
            if str(c).isdigit()
        ]
    )

    if len(years) < 2:
        return {
            "status": "error",
            "message": "Need at least two years."
        }

    current = years[-1]
    previous = years[-2]

    sales = _value(
        income,
        "net_sales",
        current,
    )

    sales_prev = _value(
        income,
        "net_sales",
        previous,
    )

    receivable = _value(
        balance,
        "trade_accounts_receivable",
        current,
    )

    receivable_prev = _value(
        balance,
        "trade_accounts_receivable",
        previous,
    )

    gross_profit = _value(
        income,
        "gross_profit",
        current,
    )

    gross_profit_prev = _value(
        income,
        "gross_profit",
        previous,
    )

    total_assets = _value(
        balance,
        "total_assets",
        current,
    )

    total_assets_prev = _value(
        balance,
        "total_assets",
        previous,
    )

    depreciation = _value(
        balance,
        "accumulated_depreciation",
        current,
    )

    depreciation_prev = _value(
        balance,
        "accumulated_depreciation",
        previous,
    )

    values = [
        sales,
        sales_prev,
        receivable,
        receivable_prev,
        gross_profit,
        gross_profit_prev,
        total_assets,
        total_assets_prev,
    ]

    if any(v is None for v in values):
        return {
            "status": "error",
            "message": "Missing financial data."
        }

    if (
        sales == 0
        or sales_prev == 0
        or gross_profit == 0
        or gross_profit_prev == 0
        or total_assets == 0
        or total_assets_prev == 0
    ):
        return {
            "status": "error",
            "message": "Division by zero."
        }

    dsri = (
        (receivable / sales)
        /
        (receivable_prev / sales_prev)
    )

    gmi = (
        (gross_profit_prev / sales_prev)
        /
        (gross_profit / sales)
    )

    asset_quality = (
        1
        - (
            (receivable + gross_profit)
            / total_assets
        )
    )

    asset_quality_prev = (
        1
        - (
            (receivable_prev + gross_profit_prev)
            / total_assets_prev
        )
    )

    if asset_quality_prev == 0:
        return {
            "status": "error",
            "message": "Division by zero."
        }

    aqi = (
        asset_quality
        /
        asset_quality_prev
    )

    sgi = (
        sales
        /
        sales_prev
    )

    depi = 1.0

    if (
        depreciation is not None
        and depreciation_prev is not None
        and depreciation != 0
        and depreciation_prev != 0
    ):
        depi = (
            depreciation_prev
            /
            depreciation
        )

    score = (
        -4.84
        + 0.92 * dsri
        + 0.528 * gmi
        + 0.404 * aqi
        + 0.892 * sgi
        + 0.115 * depi
    )

    return {
        "status": "success",
        "score": round(score, 2),
        "components": {
            "DSRI": round(dsri, 4),
            "GMI": round(gmi, 4),
            "AQI": round(aqi, 4),
            "SGI": round(sgi, 4),
            "DEPI": round(depi, 4),
        },
    }