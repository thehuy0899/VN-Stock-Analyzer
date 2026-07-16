import streamlit as st
from vnstock import Finance

from engines.cashflow_engine import (
    analyze_cashflow,
)

from data_loader import (
    load_income_statement,
)

from analysis_engine import (
    analyze_margin,
    analyze_growth,
)

from cross_analysis import (
    analyze_cross_signals,
)

from financial_health import (
    calculate_financial_health,
)

from final_analysis import (
    generate_final_analysis,
)


st.set_page_config(
    page_title="VN Stock Analyzer",
    page_icon="📊",
    layout="wide",
)


st.title("📊 VN Stock Analyzer")

st.write(
    "Phân tích nhanh chất lượng tăng trưởng "
    "và hiệu quả hoạt động của doanh nghiệp."
)


symbol = st.text_input(
    "Nhập mã cổ phiếu",
    value="FPT",
).upper().strip()


if st.button("Phân tích"):
    if not symbol:
        st.warning("Vui lòng nhập mã cổ phiếu.")

    else:
        try:
            with st.spinner("Đang phân tích dữ liệu..."):
                income = load_income_statement(
                    symbol
                )

                margin_result = analyze_margin(
                    income
                )

                if margin_result["status"] != "success":
                    st.error(
                        margin_result["message"]
                    )
                    st.stop()

                growth_result = analyze_growth(
                    income
                )

                if growth_result["status"] != "success":
                    st.error(
                        growth_result["message"]
                    )
                    st.stop()
                    
                finance = Finance(
                    symbol=symbol,
                    source="VCI",
                )

                cashflow = finance.cash_flow(
                    period="year",
                )

                cashflow_result = analyze_cashflow(
                    cashflow,
                    growth_result,
                )

                if cashflow_result["status"] != "success":
                    st.error(
                        cashflow_result.get(
                            "message",
                            "Không thể phân tích dòng tiền.",
                        )
                    )
                    st.stop()

                cross_result = analyze_cross_signals(
                    margin_result,
                    growth_result,
                )

                if cross_result["status"] != "success":
                    st.error(
                        cross_result.get(
                            "message",
                            "Không thể phân tích tín hiệu chéo."
                        )
                    )
                    st.stop()

                health_result = calculate_financial_health(
                    margin_result,
                    growth_result,
                    cross_result,
                    cashflow_result,
                )

                final_result = generate_final_analysis(
                    margin_result,
                    growth_result,
                    cross_result,
                    health_result,
                )

            st.divider()

            st.subheader(
                f"Kết quả phân tích {symbol}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Financial Health Score",
                    health_result["score"],
                )

            with col2:
                st.metric(
                    "Phân loại",
                    health_result["health_class"].upper(),
                )
            st.subheader("Chất lượng dòng tiền")

            cash_col1, cash_col2, cash_col3 = st.columns(3)

            with cash_col1:
                st.metric(
                    "Dòng tiền HĐKD",
                    f"{cashflow_result['operating_cashflow'] / 1_000_000_000:,.0f} tỷ",
                )

            with cash_col2:
                st.metric(
                    "Free Cash Flow",
                    f"{cashflow_result['free_cashflow'] / 1_000_000_000:,.0f} tỷ",
                )

            with cash_col3:
                cash_conversion = cashflow_result["cash_conversion"]

                if cash_conversion is not None:
                    st.metric(
                        "CFO / Lợi nhuận",
                        f"{cash_conversion:.2f}x",
                    )
                else:
                    st.metric(
                        "CFO / Lợi nhuận",
                        "N/A",
                    )

            st.divider()

            st.subheader("Phân tích")
            

            for text in final_result["analysis"]:
                st.write(
                    f"• {text}"
                )

            st.subheader("Luận điểm phân tích")

            st.markdown("**Động lực tăng trưởng**")
            st.write(
                final_result["growth_driver"]
            )

            st.markdown("**Chất lượng tăng trưởng**")
            st.write(
                final_result["growth_quality"]
            )

            st.markdown("**Yếu tố cần theo dõi**")
            st.warning(
                final_result["key_watch"]
            )
            st.subheader("Kết luận")

            st.success(
                final_result["conclusion"]
            )

        except Exception as error:
            st.error(
                "Không thể phân tích mã cổ phiếu này."
            )

            st.caption(
                f"Chi tiết lỗi: {error}"
            )