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
num_data = {
    "Column Name": [
        "lead_time",
        "arrival_date_year",
        "arrival_date_day_of_month",
        "is_repeated_guest",
        "previous_cancellations",
        "booking_changes",
        "days_in_waiting_list",
        "adr",
        "total_of_special_requests",
        "total_stay",
        "family",
        "cancel_risk"
    ],
    
    "Description": [
        "Days between booking and arrival",
        "Year of arrival",
        "Day of month of arrival",
        "Whether customer is a repeated guest (0/1)",
        "Number of previous cancellations",
        "Number of booking modifications",
        "Days spent on waiting list",
        "Average Daily Rate (room revenue per day)",
        "Number of special requests made",
        "Total number of nights stayed",
        "Number of family members",
        "Cancellation risk score"
    ]
}

cat_data = {
    "Column Name": [
        "hotel",
        "is_canceled",
        "arrival_date_month",
        "market_segment",
        "distribution_channel",
        "assigned_room_type",
        "customer_type",
        "is_canceled_str"
    ],
    
    "Description": [
        "Type of hotel (City Hotel or Resort Hotel)",
        "Booking cancellation status",
        "Month of guest arrival",
        "Customer market segment",
        "Booking distribution channel",
        "Assigned room category",
        "Customer type",
        "Text version of cancellation status"
    ]
}
st.markdown("""Dataset Conatain 32,000+ records of hotel bookings with 20+ features including 12 categorical and 8 numerical columns.""")

tab1, tab2 = st.tabs([      
    "Categorical Columns",
    "Numerical Columns"
])

st.markdown(""" Data source: [Hotel Booking Dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) """)

status = st.info("Loading dataset and preparing visualizations...")

with tab1:
    st.dataframe(
        pd.DataFrame(num_data),
        use_container_width=True
    )

with tab2:
    st.dataframe(
        pd.DataFrame(cat_data),
        use_container_width=True
    )

    


st.header("🛠️ Tools & Technologies")

st.markdown("""
- Python
- Pandas
- NumPy
- Plotly
- Streamlit
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