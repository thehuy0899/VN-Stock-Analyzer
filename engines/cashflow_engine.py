from core.engine_result import EngineResult
from core.constants import (
    OPERATING_CASHFLOW_ID,
    CAPEX_ID,
)
def _get_cashflow_row(cashflow, item_id):
    row = cashflow[
        cashflow["item_id"] == item_id
    ]

    if row.empty:
        return None

    return row.iloc[0]


def _get_year_columns(cashflow):
    years = []

    for column in cashflow.columns:
        column_text = str(column)

        if (
            column_text.isdigit()
            and len(column_text) == 4
        ):
            years.append(column_text)

    return sorted(
        years,
        key=int,
    )


def analyze_cashflow(
    cashflow,
    growth_result,
):
    if cashflow is None or cashflow.empty:
        return {
            "status": "error",
            "message": "Không có dữ liệu lưu chuyển tiền tệ.",
        }

    cfo_row = _get_cashflow_row(
        cashflow,
        OPERATING_CASHFLOW_ID,
    )

    capex_row = _get_cashflow_row(
        cashflow,
        CAPEX_ID,
    )

    if cfo_row is None:
        return {
            "status": "error",
            "message": "Không tìm thấy dòng tiền từ hoạt động kinh doanh.",
        }

    years = _get_year_columns(cashflow)

    if not years:
        return {
            "status": "error",
            "message": "Không xác định được kỳ dữ liệu dòng tiền.",
        }

    latest_year = years[-1]

    cfo = cfo_row.get(latest_year)

    capex = None

    if capex_row is not None:
        capex = capex_row.get(latest_year)

    if cfo is None:
        return {
            "status": "error",
            "message": "Không có dữ liệu CFO kỳ gần nhất.",
        }

    free_cash_flow = None

    if capex is not None:
        free_cash_flow = cfo + capex

    profit = growth_result.get("profit")

    cash_conversion = None

    if (
        profit is not None
        and profit != 0
    ):
        cash_conversion = (
            cfo / profit
        )

    signals = []

    if cfo > 0:
        signals.append(
            "operating_cashflow_positive"
        )

    if free_cash_flow is not None:
        if free_cash_flow > 0:
            signals.append(
                "free_cashflow_positive"
            )

        elif free_cash_flow < 0:
            signals.append(
                "free_cashflow_negative"
            )

    if (
        cash_conversion is not None
        and cash_conversion >= 1
    ):
        signals.append(
            "strong_cash_conversion"
        )

    elif (
        cash_conversion is not None
        and cash_conversion < 0.7
    ):
        signals.append(
            "weak_cash_conversion"
        )
    return {
        "status": "success",
        "latest_year": int(latest_year),
        "operating_cashflow": cfo,
        "capex": capex,
        "free_cashflow": free_cash_flow,
        "cash_conversion": cash_conversion,
        "signals": signals,
    }