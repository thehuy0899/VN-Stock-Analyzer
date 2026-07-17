from constants.financial_items import *


class FinancialMetrics:

    def __init__(self, income, balance, cashflow, year):
        self.income = income
        self.balance = balance
        self.cashflow = cashflow
        self.year = year

    def value(self, df, item):

        row = df[df["item"] == item]

        if row.empty:
            raise KeyError(item)

        return float(row.iloc[0][self.year])

    def revenue(self):
        return self.value(
            self.income,
            NET_REVENUE,
        )

    def net_profit(self):
        return self.value(
            self.income,
            NET_PROFIT,
        )

    def operating_cf(self):
        return self.value(
            self.cashflow,
            OPERATING_CF,
        )

    def capex(self):
        return self.value(
            self.cashflow,
            CAPEX,
        )

    def free_cashflow(self):
        return self.operating_cf() + self.capex()
    
    def total_assets(self):
        return self.value(
            self.balance,
            TOTAL_ASSETS,
        )


    def total_equity(self):
        return self.value(
            self.balance,
            TOTAL_EQUITY,
        )


    def total_liabilities(self):
        return self.value(
            self.balance,
            TOTAL_LIABILITIES,
        )
    
    def roe(self):
        return self.net_profit() / self.total_equity()
    
    def roa(self):
        return self.net_profit() / self.total_assets()