from pages.business_page import (
    render_business_page,
)

import streamlit as st

st.set_page_config(
    layout="wide"
)

render_business_page(
    "HPG"
)