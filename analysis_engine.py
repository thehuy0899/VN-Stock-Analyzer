def find_row_by_item_id(data, item_id):
    row = data[
        data["item_id"].eq(item_id)
    ]

    if row.empty:
        return None

    return row.iloc[0]


def get_year_columns(data):
    years = []

    for column in data.columns:
        column_text = str(column)

        if column_text.isdigit():
            years.append(column)

    return sorted(
        years,
        key=lambda year: int(str(year))
    )


def get_value(row, year):
    if row is None:
        return None

    value = row[year]

    if value is None:
        return None

    return float(value)


def analyze_margin(income):
    revenue_row = find_row_by_item_id(
        income,
        "net_sales"
    )

    gross_profit_row = find_row_by_item_id(
        income,
        "gross_profit"
    )

    operating_profit_row = find_row_by_item_id(
        income,
        "operating_profit_loss"
    )

    selling_expense_row = find_row_by_item_id(
        income,
        "selling_expenses"
    )

    admin_expense_row = find_row_by_item_id(
        income,
        "general_and_admin_expenses"
    )

    required_rows = [
        revenue_row,
        gross_profit_row,
        operating_profit_row
    ]

    if any(row is None for row in required_rows):
        return {
            "status": "error",
            "message": "Không đủ dữ liệu phân tích biên lợi nhuận."
        }

    years = get_year_columns(income)

    margin_history = {}

    for year in years:
        revenue = get_value(
            revenue_row,
            year
        )

        gross_profit = get_value(
            gross_profit_row,
            year
        )

        operating_profit = get_value(
            operating_profit_row,
            year
        )

        if not revenue:
            continue

        gross_margin = (
            gross_profit / revenue
        ) * 100

        operating_margin = (
            operating_profit / revenue
        ) * 100

        year_result = {
            "gross_margin": gross_margin,
            "operating_margin": operating_margin
        }

        if selling_expense_row is not None:
            selling_expense = abs(
                get_value(
                    selling_expense_row,
                    year
                )
            )

            year_result["selling_ratio"] = (
                selling_expense / revenue
            ) * 100

        if admin_expense_row is not None:
            admin_expense = abs(
                get_value(
                    admin_expense_row,
                    year
                )
            )

            year_result["admin_ratio"] = (
                admin_expense / revenue
            ) * 100

        margin_history[str(year)] = year_result

    available_years = list(
        margin_history.keys()
    )

    if len(available_years) < 2:
        return {
            "status": "error",
            "message": "Không đủ số năm để phân tích xu hướng."
        }

    first_year = available_years[0]
    latest_year = available_years[-1]

    first_data = margin_history[first_year]
    latest_data = margin_history[latest_year]

    gross_margin_change = (
        latest_data["gross_margin"]
        - first_data["gross_margin"]
    )

    operating_margin_change = (
        latest_data["operating_margin"]
        - first_data["operating_margin"]
    )

    selling_ratio_change = None
    admin_ratio_change = None

    if (
        "selling_ratio" in first_data
        and "selling_ratio" in latest_data
    ):
        selling_ratio_change = (
            latest_data["selling_ratio"]
            - first_data["selling_ratio"]
        )

    if (
        "admin_ratio" in first_data
        and "admin_ratio" in latest_data
    ):
        admin_ratio_change = (
            latest_data["admin_ratio"]
            - first_data["admin_ratio"]
        )

    signals = []

    if gross_margin_change < 0:
        signals.append(
            "gross_margin_down"
        )

    if gross_margin_change > 0:
        signals.append(
            "gross_margin_up"
        )

    if operating_margin_change < 0:
        signals.append(
            "operating_margin_down"
        )

    if operating_margin_change > 0:
        signals.append(
            "operating_margin_up"
        )

    if (
        selling_ratio_change is not None
        and selling_ratio_change < 0
    ):
        signals.append(
            "selling_efficiency_improved"
        )

    if (
        admin_ratio_change is not None
        and admin_ratio_change < 0
    ):
        signals.append(
            "admin_efficiency_improved"
        )

    if (
        gross_margin_change < 0
        and operating_margin_change > 0
    ):
        signals.append(
            "margin_divergence"
        )

    return {
        "status": "success",
        "first_year": first_year,
        "latest_year": latest_year,
        "history": margin_history,
        "gross_margin": latest_data[
            "gross_margin"
        ],
        "operating_margin": latest_data[
            "operating_margin"
        ],
        "gross_margin_change": gross_margin_change,
        "operating_margin_change": operating_margin_change,
        "selling_ratio_change": selling_ratio_change,
        "admin_ratio_change": admin_ratio_change,
        "signals": signals
    }


def calculate_cagr(
    first_value,
    latest_value,
    number_of_years
):
    if (
        first_value is None
        or latest_value is None
        or number_of_years <= 0
    ):
        return None

    if first_value <= 0 or latest_value <= 0:
        return None

    return (
        (
            latest_value / first_value
        ) ** (
            1 / number_of_years
        )
        - 1
    ) * 100


def classify_growth_rate(value):
    if value is None:
        return "unknown"

    if value < -20:
        return "collapse"

    if value < 0:
        return "declining"

    if value < 5:
        return "stagnant"

    if value < 15:
        return "moderate"

    if value < 30:
        return "strong"

    return "exceptional"

def analyze_growth(income):
    revenue_row = find_row_by_item_id(
        income,
        "net_sales"
    )

    profit_row = find_row_by_item_id(
        income,
        "attributable_to_parent_company"
    )

    if revenue_row is None:
        return {
            "status": "error",
            "message": "Không tìm thấy doanh thu thuần."
        }

    if profit_row is None:
        return {
            "status": "error",
            "message": "Không tìm thấy lợi nhuận công ty mẹ."
        }

    years = get_year_columns(income)

    if len(years) < 2:
        return {
            "status": "error",
            "message": "Không đủ dữ liệu để phân tích tăng trưởng."
        }

    growth_history = {}

    previous_revenue = None
    previous_profit = None

    for year in years:
        revenue = get_value(
            revenue_row,
            year
        )

        profit = get_value(
            profit_row,
            year
        )

        revenue_growth = None
        profit_growth = None

        if (
            previous_revenue is not None
            and previous_revenue != 0
            and revenue is not None
        ):
            revenue_growth = (
                (
                    revenue / previous_revenue
                )
                - 1
            ) * 100

        if (
            previous_profit is not None
            and previous_profit != 0
            and profit is not None
        ):
            profit_growth = (
                (
                    profit / previous_profit
                )
                - 1
            ) * 100

        growth_history[str(year)] = {
            "revenue": revenue,
            "profit": profit,
            "revenue_growth": revenue_growth,
            "profit_growth": profit_growth
        }

        previous_revenue = revenue
        previous_profit = profit

    available_years = list(
        growth_history.keys()
    )

    first_year = available_years[0]
    latest_year = available_years[-1]

    number_of_years = (
        int(latest_year)
        - int(first_year)
    )

    first_data = growth_history[first_year]
    latest_data = growth_history[latest_year]

    revenue_cagr = calculate_cagr(
        first_data["revenue"],
        latest_data["revenue"],
        number_of_years
    )

    profit_cagr = calculate_cagr(
        first_data["profit"],
        latest_data["profit"],
        number_of_years
    )

    signals = []

    latest_revenue_growth = latest_data[
        "revenue_growth"
    ]

    latest_profit_growth = latest_data[
        "profit_growth"
    ]
    
    revenue_growth_class = classify_growth_rate(
        latest_revenue_growth
    )

    profit_growth_class = classify_growth_rate(
        latest_profit_growth
    )

    revenue_cagr_class = classify_growth_rate(
        revenue_cagr
    )

    profit_cagr_class = classify_growth_rate(
        profit_cagr
    )

    if (
        latest_revenue_growth is not None
        and latest_revenue_growth > 0
    ):
        signals.append(
            "revenue_growth_positive"
        )

    if (
        latest_revenue_growth is not None
        and latest_revenue_growth < 0
    ):
        signals.append(
            "revenue_growth_negative"
        )

    if (
        latest_profit_growth is not None
        and latest_profit_growth > 0
    ):
        signals.append(
            "profit_growth_positive"
        )

    if (
        latest_profit_growth is not None
        and latest_profit_growth < 0
    ):
        signals.append(
            "profit_growth_negative"
        )

    if (
        latest_revenue_growth is not None
        and latest_profit_growth is not None
        and latest_profit_growth
        > latest_revenue_growth
    ):
        signals.append(
            "profit_growth_faster_than_revenue"
        )

    if (
        latest_revenue_growth is not None
        and latest_profit_growth is not None
        and latest_revenue_growth > 0
        and latest_profit_growth < 0
    ):
        signals.append(
            "growth_divergence"
        )

    if (
        revenue_cagr is not None
        and revenue_cagr >= 10
    ):
        signals.append(
            "strong_revenue_cagr"
        )

    if (
        profit_cagr is not None
        and profit_cagr >= 10
    ):
        signals.append(
            "strong_profit_cagr"
        )

    return {
        "status": "success",
        "first_year": first_year,
        "latest_year": latest_year,
        "history": growth_history,
        "revenue": latest_data["revenue"],
        "profit": latest_data["profit"],
        "revenue_growth": latest_revenue_growth,
        "profit_growth": latest_profit_growth,
        "revenue_cagr": revenue_cagr,
        "profit_cagr": profit_cagr,
        "revenue_growth_class": revenue_growth_class,
        "profit_growth_class": profit_growth_class,
        "revenue_cagr_class": revenue_cagr_class,
        "profit_cagr_class": profit_cagr_class,
        "signals": signals
    }