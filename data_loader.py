from datetime import date, timedelta

from vnstock import Vnstock


def load_stock(symbol):
    symbol = symbol.upper().strip()

    stock = Vnstock().stock(
        symbol=symbol,
        source="VCI"
    )

    return stock


def load_income_statement(symbol):
    stock = load_stock(symbol)

    income = stock.finance.income_statement(
        period="year",
        lang="vi",
        dropna=True
    )

    return income


def load_balance_sheet(symbol):
    stock = load_stock(symbol)

    balance = stock.finance.balance_sheet(
        period="year",
        lang="vi",
        dropna=True
    )

    return balance


def load_cash_flow(symbol):
    stock = load_stock(symbol)

    cash_flow = stock.finance.cash_flow(
        period="year",
        lang="vi",
        dropna=True
    )

    return cash_flow


def load_price_history(symbol, years=1):
    stock = load_stock(symbol)

    end_date = date.today()

    start_date = end_date - timedelta(
        days=365 * years
    )

    price = stock.quote.history(
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )

    return price


def load_financial_data(symbol):
    income = load_income_statement(symbol)

    balance = load_balance_sheet(symbol)

    cash_flow = load_cash_flow(symbol)

    return {
        "income": income,
        "balance": balance,
        "cash_flow": cash_flow
    }