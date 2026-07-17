import streamlit as st

from services.business_service import (
    BusinessService,
)

from engines.business_engine import (
    analyze_business,
)


def show_list(title, value):

    st.subheader(title)

    if not value:
        st.write("-")
        return

    items = [
        item.strip()
        for item in value.split(",")
    ]

    for item in items:
        st.markdown(f"• {item}")


def render_business_page(
    ticker: str,
):

    business = (
        BusinessService.get_business(
            ticker
        )
    )
    result = analyze_business(
        business
    )

    st.header("🏢 Business Analysis")

    if business is None:
        st.warning(
            "Chưa có dữ liệu Business."
        )
        return

    st.subheader("Business Model")

    st.info(
        business.business_model
    )

    show_list(
        "Customers",
        business.customer,
    )

    show_list(
        "Growth Drivers",
        business.growth_driver,
    )

    show_list(
        "Threats",
        business.threat,
    )
    st.divider()

    st.subheader(
        "Business Score"
    )

    st.metric(
        "Score",
        result.score,
    )

    st.write(
        result.summary
    )