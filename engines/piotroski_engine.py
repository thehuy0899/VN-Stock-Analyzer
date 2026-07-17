print("Loaded Piotroski:", __file__)
import pandas as pd


def _value(df: pd.DataFrame, item_id: str, year: str):
    row = df[df["item_id"] == item_id]

    if row.empty:
        return 0

    return float(row.iloc[0][year])


def analyze(income, balance_sheet, cashflow):
    print(">>> Piotroski analyze() called")

    current = "2025"
    previous = "2024"

    net_income = _value(
        income,
        "net_profit_loss_after_tax",
        current,
    )

    prev_net_income = _value(
        income,
        "net_profit_loss_after_tax",
        previous,
    )

    total_assets = _value(
        balance_sheet,
        "total_assets",
        current,
    )

    prev_total_assets = _value(
        balance_sheet,
        "total_assets",
        previous,
    )

    operating_cashflow = _value(
        cashflow,
        "net_cash_inflows_outflows_from_operating_activities",
        current,
    )

    long_term_debt = _value(
        balance_sheet,
        "long_term_borrowings",
        current,
    )

    prev_long_term_debt = _value(
        balance_sheet,
        "long_term_borrowings",
        previous,
    )

    current_assets = _value(
        balance_sheet,
        "current_assets",
        current,
    )

    prev_current_assets = _value(
        balance_sheet,
        "current_assets",
        previous,
    )

    current_liabilities = _value(
        balance_sheet,
        "current_liabilities",
        current,
    )

    prev_current_liabilities = _value(
        balance_sheet,
        "current_liabilities",
        previous,
    )

    current_ratio = (
        current_assets / current_liabilities
    )

    prev_current_ratio = (
        prev_current_assets / prev_current_liabilities
    )

    shares = _value(
        balance_sheet,
        "paid_in_capital",
        current,
    )

    prev_shares = _value(
        balance_sheet,
        "paid_in_capital",
        previous,
    )

    gross_profit = _value(
        income,
        "gross_profit",
        current,
    )

    prev_gross_profit = _value(
        income,
        "gross_profit",
        previous,
    )

    net_sales = _value(
        income,
        "net_sales",
        current,
    )

    prev_net_sales = _value(
        income,
        "net_sales",
        previous,
    )

    gross_margin = gross_profit / net_sales
    prev_gross_margin = (
        prev_gross_profit / prev_net_sales
    )

    asset_turnover = (
        net_sales / total_assets
    )

    prev_asset_turnover = (
        prev_net_sales / prev_total_assets
    )

    roa = net_income / total_assets
    prev_roa = prev_net_income / prev_total_assets

    score = 0
    passed = []
    failed = []

    # F1: Positive Net Income
    if net_income > 0:
        score += 1
        passed.append("positive_net_income")
    else:
        failed.append("positive_net_income")

    # F2: Positive Operating Cash Flow
    if operating_cashflow > 0:
        score += 1
        passed.append("positive_operating_cashflow")
    else:
        failed.append("positive_operating_cashflow")

    # F3: ROA Improvement
    if roa > prev_roa:
        score += 1
        passed.append("improving_roa")
    else:
        failed.append("improving_roa")

    # F4: Operating Cash Flow > Net Income
    if operating_cashflow > net_income:
        score += 1
        passed.append("cashflow_exceeds_net_income")
    else:
        failed.append("cashflow_exceeds_net_income")

    # F5: Lower Long-term Debt
    if long_term_debt < prev_long_term_debt:
        score += 1
        passed.append("lower_long_term_debt")
    else:
        failed.append("lower_long_term_debt")

    # F6: Higher Current Ratio
    if current_ratio > prev_current_ratio:
        score += 1
        passed.append("higher_current_ratio")
    else:
        failed.append("higher_current_ratio")

    # F7: No New Shares Issued
    if shares <= prev_shares:
        score += 1
        passed.append("no_new_shares_issued")
    else:
        failed.append("no_new_shares_issued")

    # F8: Higher Gross Margin
    if gross_margin > prev_gross_margin:
        score += 1
        passed.append("higher_gross_margin")
    else:
        failed.append("higher_gross_margin")

    # F9: Higher Asset Turnover
    if asset_turnover > prev_asset_turnover:
        score += 1
        passed.append("higher_asset_turnover")
    else:
        failed.append("higher_asset_turnover")

    return {
        "roa": roa,
        "prev_roa": prev_roa,
        "score": score,
        "passed": passed,
        "failed": failed,
    }