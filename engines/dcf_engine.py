import pandas as pd

from engines.dcf_assumption_engine import (
    get_default_assumptions,
)
from engines.discount_rate_engine import calculate_wacc
from engines.terminal_value_engine import calculate_terminal_value


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


def _net_debt(balance_sheet):
    cash = _value(
        balance_sheet,
        "cash_and_cash_equivalents",
    )

    if cash is None:
        cash = 0

    st_debt = _value(
        balance_sheet,
        "short_term_borrowings",
    )

    if st_debt is None:
        st_debt = 0

    lt_debt = _value(
        balance_sheet,
        "long_term_borrowings",
    )

    if lt_debt is None:
        lt_debt = 0

    return (
        st_debt
        + lt_debt
        - cash
    )


def analyze(
    cashflow: pd.DataFrame,
    balance_sheet: pd.DataFrame,
    current_price=None,
    outstanding_shares=None,
):
    assumptions = (
        get_default_assumptions()
    )
    wacc_result = calculate_wacc()
    discount_rate = wacc_result["wacc"]

    years = sorted(
        [
            c
            for c in cashflow.columns
            if str(c).isdigit()
        ]
    )

    if len(years) == 0:
        return {
            "status": "error",
            "message": "No financial year."
        }

    year = years[-1]

    operating_cf = _value(
        cashflow,
        "net_cash_inflows_outflows_from_operating_activities",
        year,
    )

    capex = _value(
        cashflow,
        "purchases_of_fixed_assets_and_other_long_term_assets",
        year,
    )
    if (
        operating_cf is None
        or capex is None
    ):
        return {
            "status": "error",
            "message": "Missing cashflow data."
        }

    fcf = operating_cf - abs(capex)

    growth = 0.10

    projection = []

    current_fcf = fcf

    for i in range(
        assumptions["projection_years"]
    ):
        current_fcf *= (
            1 + growth
        )
        projection.append(
            current_fcf
        )

    present_values = []

    for i, value in enumerate(projection, start=1):
        pv = value / ((1 + discount_rate) ** i)
        present_values.append(pv)

    terminal = calculate_terminal_value(
        last_fcf=projection[-1],
        wacc=discount_rate,
    )

    terminal_pv = (
        terminal["terminal_value"]
        / (
            (1 + discount_rate)
            ** assumptions["projection_years"]
        )
    )

    enterprise_value = (
        sum(present_values)
        + terminal_pv
    )

    net_debt = _net_debt(
        balance_sheet
    )

    equity_value = (
        enterprise_value
        - net_debt
    )

    intrinsic_value = None

    margin_of_safety = None

    if (
        outstanding_shares
        and current_price
    ):
        intrinsic_value = (
            equity_value
            / outstanding_shares
        )

        margin_of_safety = (
            (
                intrinsic_value
                - current_price
            )
            / current_price
            * 100
        )

    return {
        "status": "success",
        "fcf": round(fcf, 2),
        "projection": projection,
        "assumptions": assumptions,
        "wacc": wacc_result,
        "present_values": present_values,
        "terminal": terminal,
        "terminal_pv": terminal_pv,
        "enterprise_value": enterprise_value,
        "net_debt": net_debt,
        "equity_value": equity_value,
        "intrinsic_value": intrinsic_value,
        "current_price": current_price,
        "margin_of_safety": margin_of_safety,
    }