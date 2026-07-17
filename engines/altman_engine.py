import pandas as pd


def _value(df: pd.DataFrame, item_id: str, year=None):

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
            c for c in balance.columns
            if str(c).isdigit()
        ]
    )

    if len(years) == 0:
        return {
            "status": "error",
            "message": "No year found."
        }

    year = years[-1]

    current_assets = _value(
        balance,
        "current_assets",
        year,
    )

    current_liabilities = _value(
        balance,
        "current_liabilities",
        year,
    )

    total_assets = _value(
        balance,
        "total_assets",
        year,
    )

    retained_earnings = _value(
        balance,
        "undistributed_earnings",
        year,
    )

    ebit = _value(
        income,
        "operating_profit_loss",
        year,
    )

    revenue = _value(
        income,
        "net_sales",
        year,
    )

    total_liabilities = _value(
        balance,
        "liabilities",
        year,
    )

    equity = _value(
        balance,
        "owners_equity",
        year,
    )

    values = [
        current_assets,
        current_liabilities,
        total_assets,
        retained_earnings,
        ebit,
        revenue,
        total_liabilities,
        equity,
    ]

    if any(v is None for v in values):
        return {
            "status": "error",
            "message": "Missing financial data."
        }

    if (
        total_assets == 0
        or total_liabilities == 0
    ):
        return {
            "status": "error",
            "message": "Division by zero."
        }

    working_capital = (
    current_assets
    - current_liabilities
    )

    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = equity / total_liabilities
    x5 = revenue / total_assets

    score = (
        1.2 * x1
        + 1.4 * x2
        + 3.3 * x3
        + 0.6 * x4
        + 1.0 * x5
    )

    return {
        "status": "success",
        "score": round(score, 2),
        "components": {
            "x1": round(x1, 4),
            "x2": round(x2, 4),
            "x3": round(x3, 4),
            "x4": round(x4, 4),
            "x5": round(x5, 4),
        },
    }