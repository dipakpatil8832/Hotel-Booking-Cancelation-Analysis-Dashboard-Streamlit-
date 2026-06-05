import streamlit as st
import pandas as pd


st.markdown("""
<style>
[data-testid="metric-container"]{
    background-color:#F8FAFC;
    border:1px solid #E2E8F0;
    padding:15px;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)


st.title("🏨 Hotel Booking Analysis ")

st.markdown("---")

st.header("📌 Project Overview")

st.write("""
This project analyzes hotel booking data to uncover patterns in customer behavior,
cancellations, room preferences, pricing trends, and booking characteristics.

The dashboard provides interactive visualizations that help stakeholders understand
booking trends and make data-driven business decisions.
""")

st.header("🎯 Business Objectives")

st.markdown("""
- Analyze customer booking behavior.
- Identify cancellation patterns.
- Understand ADR (Average Daily Rate) trends.
- Explore room type preferences.
- Detect seasonal demand fluctuations.
- Support pricing and revenue optimization strategies.
""")

st.header("📊 Dataset Information")

st.markdown("""
**Source:** Hotel Booking Demand Dataset

**Records:** 119,000+

**Features:** 30+

**Hotels Included:**
- Resort Hotel
- City Hotel
""")

st.header("🛠️ Tools & Technologies")

st.markdown("""
- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Scikit-Learn
""")

st.header("📈 Dashboard Sections")

st.markdown("""
1. Data Distribution & Outlier Analysis
2. Univariate Analysis
3. Bivariate Analysis
4. Multivariate Analysis
5. Executive Dashboard
""")

st.success("Navigate using the sidebar to explore the analysis.")