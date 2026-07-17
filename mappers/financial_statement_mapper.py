from core.financial_statement import FinancialStatement


class FinancialStatementMapper:

    @staticmethod
    def map(data: dict) -> FinancialStatement:
        income = data["income"]
        balance = data["balance"]
        cashflow = data["cashflow"]

        # Tạm thời trả dữ liệu giả
        return FinancialStatement(
            revenue=0,
            gross_profit=0,
            operating_income=0,
            net_income=0,
            total_assets=0,
            current_assets=0,
            total_liabilities=0,
            current_liabilities=0,
            long_term_debt=0,
            equity=0,
            operating_cashflow=0,
            free_cashflow=0,
            shares_outstanding=0,
        )