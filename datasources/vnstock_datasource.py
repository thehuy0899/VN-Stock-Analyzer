from vnstock import Vnstock


class VNStockDataSource:

    @staticmethod
    def financial(ticker: str):

        stock = Vnstock().stock(
            symbol=ticker,
            source="VCI",
        )

        income = stock.finance.income_statement(
            period="year",
            lang="vi",
        )

        balance = stock.finance.balance_sheet(
            period="year",
            lang="vi",
        )

        cashflow = stock.finance.cash_flow(
            period="year",
            lang="vi",
        )

        return {
            "income": income,
            "balance": balance,
            "cashflow": cashflow,
        }