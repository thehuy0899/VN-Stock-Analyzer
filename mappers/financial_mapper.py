from core.financial import Financial


class FinancialMapper:

    @staticmethod
    def from_json(data: dict) -> Financial:


        return Financial(
            revenue=data["revenue"],
            profit=data["profit"],
            operating_cashflow=data["operating_cashflow"],
            free_cashflow=data["free_cashflow"],
            roe=data["roe"],
            roic=data["roic"],
        )
    
    @staticmethod
    def from_vnstock(raw: dict) -> Financial:

        income = raw["income"]
        balance = raw["balance"]
        cashflow = raw["cashflow"]

        latest_income = income.iloc[0]
        latest_balance = balance.iloc[0]
        latest_cashflow = cashflow.iloc[0]


    @staticmethod
    def from_vnstock(raw: dict) -> Financial:

        income = raw["income"]
        balance = raw["balance"]
        cashflow = raw["cashflow"]

        latest_year = income.columns[-4]   # Ví dụ: "2025"

        revenue = FinancialMapper._value(
            income,
            "Doanh thu thuần",
            latest_year,
        )

        profit = FinancialMapper._value(
            income,
            "Lãi/(lỗ) thuần sau thuế",
            latest_year,
        )

        operating_cf = FinancialMapper._value(
            cashflow,
            "Lưu chuyển tiền tệ ròng từ các hoạt động sản xuất kinh doanh",
            latest_year,
        )

        capex = FinancialMapper._value(
            cashflow,
            "Tiền chi để mua sắm, xây dựng TSCĐ và các tài sản dài hạn khác",
            latest_year,
        )
        free_cashflow = operating_cf + capex

        return Financial(
            revenue=revenue,
            profit=profit,
            operating_cashflow=operating_cf,
            free_cashflow=free_cashflow,
            roe=0,
            roic=0,
        )
    @staticmethod
    def _value(df, item_name: str, year: str):
        row = df[df["item"] == item_name]

        if row.empty:
            raise KeyError(f"Không tìm thấy chỉ tiêu: {item_name}")

        return float(row.iloc[0][year])