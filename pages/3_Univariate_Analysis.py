import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import math
pio.templates.default = "plotly_dark"
PALETTE   = px.colors.qualitative.Vivid
CANCEL_C  = {"0": "#00C9A7", "1": "#FF6B6B"}

@st.cache_data
def load_data():
    return pd.read_csv("data/hotel_bookings_cleaned.csv")

df = load_data()


st.title("📈 Univariate Analysis")

st.markdown("""
<hr style="
border:1px solid white;
margin-top:25px;
margin-bottom:25px;">
""", unsafe_allow_html=True)

hotel_counts = (
    df["hotel"]
    .value_counts()
    .reset_index()
)

hotel_counts.columns = ["Hotel","Count"]

fig_hotel = px.pie(
    hotel_counts,
    names="Hotel",
    values="Count",
    hole=0.5,
    title="Hotel Type Distribution"
)

st.plotly_chart(
    fig_hotel,
    use_container_width=True
)

with st.expander("Hotel Type Distribution Insights"):
    st.markdown("""
    - **City Hotels dominate the dataset**, accounting for approximately **66.4%** of all bookings.
    - **Resort Hotels contribute around 33.6%** of total reservations.
    - The booking volume of City Hotels is nearly **twice that of Resort Hotels**.
    - Higher City Hotel demand may be driven by business travel, urban tourism, and shorter stays.
    - Resort Hotels represent a smaller but potentially higher-value segment, often associated with vacations and leisure travel.
    - Future analyses should compare cancellation rates, ADR, and guest behavior separately for each hotel type.
    """)

st.markdown("""
<hr style="
border:1px solid white;
margin-top:25px;
margin-bottom:25px;">
""", unsafe_allow_html=True)

ct_hotel = (df.groupby(["hotel","customer_type","is_canceled_str"])
              .size().reset_index(name="Count"))

fig_customer= px.bar(
    ct_hotel,
    x="customer_type", y="Count",
    color="is_canceled_str",
    facet_col="hotel",
    barmode="group",
    color_discrete_map={
    "No": "#00D4AA",
    "Yes": "#FF5C8A"
},
    text="Count",
    labels={"is_canceled_str":"Canceled","customer_type":"Customer Type"},
    title="Customer Type × Hotel vs Cancellations"
)
fig_customer.update_traces(textposition="outside", textfont_size=8,
                  marker_line_color="#1a1a2e", marker_line_width=1)
fig_customer.update_layout(title_x=0.5, height=500, xaxis_tickangle=-25,
                  legend_title="Canceled (1=Yes)")
fig_customer.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
st.plotly_chart(
    fig_customer,
    use_container_width=True
)
with st.expander("📌 Customer Type & Cancellation Insights"):
    st.markdown("""
    - **Transient customers dominate bookings** across both City and Resort Hotels.
    - City Hotels receive significantly more bookings than Resort Hotels for every customer segment.
    - The **highest number of cancellations comes from Transient customers**, making them the primary contributor to booking losses.
    - Contract customers show the **lowest cancellation rates**, indicating more reliable booking behavior.
    - Group bookings are relatively small and experience fewer cancellations compared to Transient guests.
    - Transient-Party customers exhibit moderate cancellation behavior but remain more stable than pure Transient guests.
    - Resort Hotels have fewer overall bookings and cancellations, suggesting more committed leisure travelers.
    - Cancellation reduction strategies should primarily target **Transient guests**, especially in City Hotels.
    """)

st.markdown("""
<hr style="
border:1px solid white;
margin-top:25px;
margin-bottom:25px;">
""", unsafe_allow_html=True)

month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

month_cnt = (df["arrival_date_month"]
               .value_counts()
               .reindex(month_order)
               .reset_index())
month_cnt.columns = ["Month", "Count"]

fig_month = px.bar(
    month_cnt, x="Month", y="Count",
    color="Count", color_continuous_scale="Plasma",
    text="Count",
    title="📅 Monthly Booking Volume"
)
fig_month.update_traces(textposition="outside", textfont_size=11,
                  marker_line_color="#1a1a2e", marker_line_width=1)
fig_month.update_layout(title_x=0.5, height=460,
                  xaxis_tickangle=-35,
                  coloraxis_showscale=False)

st.plotly_chart(
    fig_month,
    use_container_width=True
)
with st.expander("📅 Monthly Booking Volume Insights"):
    st.markdown("""
    - Booking volume shows a clear seasonal pattern throughout the year.
    - Reservations steadily increase from **January (5,929)** to **August (13,877)**.
    - **August records the highest number of bookings**, indicating peak travel demand.
    - July and August represent the busiest months, likely driven by summer vacations and holiday travel.
    - After August, booking volume gradually declines through the remainder of the year.
    - **November and December show the lowest demand** after January, suggesting an off-peak season.
    - Hotels should allocate additional staff and resources during peak months to maintain service quality.
    - Promotional campaigns and discounts can be targeted during low-demand months to improve occupancy rates.
    """)

st.markdown("""
<hr style="
border:1px solid white;
margin-top:25px;
margin-bottom:25px;">
""", unsafe_allow_html=True)

ctype = df["customer_type"].value_counts().reset_index()
ctype.columns = ["Type", "Count"]

fig_cust = px.bar(
    ctype, x="Type", y="Count",
    color="Type",
    color_discrete_sequence=PALETTE,
    text="Count",
    title="Customer Type Breakdown"
)
fig_cust.update_traces(textposition="outside", textfont_size=13,
                  marker_line_color="#1a1a2e", marker_line_width=1.5)
fig_cust.update_layout(title_x=0.5, height=420, showlegend=False)

st.plotly_chart(
    fig_cust,
    use_container_width=True
)
with st.expander("👥 Customer Type Insights"):
    st.markdown("""
    - **Transient customers dominate the dataset**, accounting for the vast majority of hotel bookings.
    - With approximately **89,000 bookings**, Transient guests are the primary revenue-driving customer segment.
    - **Transient-Party** is the second-largest segment with over **25,000 bookings**, but remains significantly smaller than Transient customers.
    - **Contract customers** contribute a relatively small share of total bookings, indicating limited long-term corporate agreements.
    - **Group bookings** are extremely rare, representing less than 1% of total reservations.
    - The hotel business heavily depends on individual travelers rather than organized groups or contracted clients.
    - Marketing and retention strategies focused on Transient guests are likely to have the greatest impact on occupancy and revenue.
    - Diversifying customer acquisition toward Contract and Group segments could help reduce dependency on a single customer type.
    """)
# room_counts = (
#     df["reserved_room_type"]
#     .value_counts()
#     .reset_index()
# )

# room_counts.columns = [
#     "Room Type",
#     "Count"
# ]

# fig_room = px.bar(
#     room_counts,
#     x="Room Type",
#     y="Count",
#     color="Room Type"
# )
# Monthly ADR
