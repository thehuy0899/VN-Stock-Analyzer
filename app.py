import streamlit as st

from investment_pipeline import (
    run_investment_pipeline,
)

from report_engine import (
    generate_report,
)

st.set_page_config(
    page_title="VN Stock Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("📊 VN Stock Analyzer")

symbol = st.text_input(
    "Nhập mã cổ phiếu",
    value="FPT",
).upper().strip()

if st.button("Phân tích"):

    try:

        with st.spinner("Đang phân tích..."):

            data = run_investment_pipeline(
                symbol
            )

            report = generate_report(
                data["financial"],
                data["business"],
                data["industry"],
                data["moat"],
                data["management"],
            )

        st.header("Investment Report")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Financial",
                report["financial_score"],
            )

            st.metric(
                "Industry",
                report["industry_score"],
            )

            st.metric(
                "Moat",
                report["moat_score"],
            )

        with col2:

            st.metric(
                "Management",
                report["management_score"],
            )

            st.metric(
                "Investment Score",
                report["investment_score"],
            )

            if report["investment_score"] >= 80:
                rec = "🟢 BUY"

            elif report["investment_score"] >= 65:
                rec = "🟡 HOLD"

            else:
                rec = "🔴 SELL"

            st.metric(
                "Recommendation",
                rec,
            )
            st.metric(
                "Recommendation",
                report["recommendation"],
            )

            st.divider()

            st.subheader("Score Summary")

            scores = {
                "Financial": report["financial_score"],
                "Business": report["business_score"],
                "Industry": report["industry_score"],
                "Moat": report["moat_score"],
                "Management": report["management_score"],
            }

            for name, score in scores.items():
                st.progress(score / 100)
                st.write(f"{name}: {score}/100")

    except Exception as e:

        st.error(e)