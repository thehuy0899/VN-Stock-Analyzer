import warnings

from vnstock import Finance

from data_loader import (
    load_income_statement,
)

from market_data_loader import (
    load_market_data,
)

from company_data_loader import (
    load_company_data,
)


warnings.filterwarnings(
    "ignore",
    message=(
        "Downcasting object dtype arrays "
        "on .fillna, .ffill, .bfill "
        "is deprecated.*"
    ),
    category=FutureWarning,
)


def load_financial_data(
    symbol,
):
    symbol = symbol.upper().strip()

    income = load_income_statement(
        symbol
    )

    finance = Finance(
        symbol=symbol,
        source="VCI",
    )

    balance_sheet = (
        finance.balance_sheet(
            period="year",
        )
    )

    cashflow = (
        finance.cash_flow(
            period="year",
        )
    )

    market_data = load_market_data(
        symbol
    )

    company_data = load_company_data(
        symbol
    )


    return {
        "symbol": symbol,
        "income": income,
        "balance_sheet": balance_sheet,
        "cashflow": cashflow,
        "company": company_data,
        "market": market_data,
    }