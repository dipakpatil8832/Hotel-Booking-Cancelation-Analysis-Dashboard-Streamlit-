import streamlit as st
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math


st.title("📉 Bivariate Analysis")


@st.cache_data
def load_data():
    return pd.read_csv("data/hotel_bookings_cleaned.csv")


df = load_data()

hotel_cancel = (
    df.groupby(["hotel", "is_canceled_str"])
      .size()
      .reset_index(name="Count")
)


fig_hotel_cancel = px.bar(
    hotel_cancel,
    x="hotel",
    y="Count",
    color="is_canceled_str",
    barmode="group",
    title="Hotel Type vs Cancellation"
)

ct_hotel = (df.groupby(["hotel", "customer_type", "is_canceled_str"])
            .size()
            .reset_index(name="Count")
            )

fig_customer_cancel = px.bar(
    ct_hotel,
    x="customer_type",
    y="Count",
    color="is_canceled_str",
    facet_col="hotel",
    barmode="group",
    text="Count",
    title="Customer Type × Hotel vs Cancellations",
    color_discrete_map={
        "No": "#10B981",
        "Yes": "#EF4444"
    }
)


fig_customer_cancel.update_layout(
    height=500,
    title_x=0.5
)


segment_cancel = (
    df.groupby(
        ["market_segment", "is_canceled_str"]
    )
    .size()
    .reset_index(name="Count")
)

fig_segment = px.bar(
    segment_cancel,
    x="market_segment",
    y="Count",
    color="is_canceled_str",
    barmode="group"
)


df["adr"] = df["adr"].clip(upper=500)
fig_adr_hotel = px.violin(
    df,
    x="hotel",
    y="adr",
    color="hotel",
    title="ADR Distribution by Hotel Type"
)


fig_lead_adr = px.scatter(
    df.sample(5000),
    x="lead_time",
    y="adr",
    color="hotel",
    opacity=0.6,
    title="Lead Time vs ADR"
)


fig_room_adr = px.box(
    df,
    x="assigned_room_type",
    y="adr",
    color="assigned_room_type",
    title="ADR by Assigned Room Type"
)


df["reservation_status_date"] = pd.to_datetime(
    df["reservation_status_date"], format="%Y-%m-%d")
# Monthly ADR
monthly_adr = (
    df.groupby([
        pd.Grouper(key='reservation_status_date', freq='ME'),
        'assigned_room_type'
    ])['adr']
    .mean()
    .reset_index()
)

rooms = sorted(monthly_adr['assigned_room_type'].unique())

# Grid size
cols = 3
rows = math.ceil(len(rooms) / cols)

fig1 = make_subplots(
    rows=rows,
    cols=cols,
    subplot_titles=[f"Room Type {room}" for room in rooms],
    vertical_spacing=0.08,
    horizontal_spacing=0.05,
    shared_yaxes=True
)

for idx, room in enumerate(rooms):
    row = idx // cols + 1
    col = idx % cols + 1

    temp = monthly_adr[
        monthly_adr['assigned_room_type'] == room
    ]

    fig1.add_trace(
        go.Scatter(
            x=temp['reservation_status_date'],
            y=temp['adr'],
            mode='lines+markers',
            fill='tozeroy',
            name=f'Room {room}',
            showlegend=False
        ),
        row=row,
        col=col
    )

fig1.update_layout(
    title={
        'text': 'Monthly ADR Trend by Assigned Room Type',
        'x': 0.5,
        'font': {'size': 24}
    },
    template='plotly_dark',
    height=350 * rows,
    width=1400
)

fig1.update_xaxes(title_text="Date")
fig1.update_yaxes(title_text="ADR")


# Lead Time Distribution by Cancellation Status
fig_Lead_Time_Distribution_by_Cancellation = go.Figure()
for status, color, label in [("No", "#00C9A7", "Not Canceled"), ("Yes", "#FF6B6B", "Canceled")]:
    fig_Lead_Time_Distribution_by_Cancellation.add_trace(go.Histogram(
        x=df[df["is_canceled"] == status]["lead_time"],   # ← int, not string
        name=label, nbinsx=60,
        marker_color=color, opacity=0.7,
        hovertemplate=f"<b>{label}</b><br>Lead Time: %{{x}}<br>Count: %{{y}}<extra></extra>"
    ))
fig_Lead_Time_Distribution_by_Cancellation.update_layout(
    barmode="overlay",
    title=dict(text="⏳ Lead Time Distribution by Cancellation Status",
               font_size=20, x=0.5),
    height=460,
    xaxis_title="Lead Time (days)",
    yaxis_title="Count",
    legend_title="Status"
)

# Monthly ADR Trend by Room Type
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
month_cancel = (df.groupby(["arrival_date_month", "is_canceled_str"])
                  .size().reset_index(name="Count"))
month_cancel["Month_num"] = pd.Categorical(
    month_cancel["arrival_date_month"], categories=month_order, ordered=True)
month_cancel = month_cancel.sort_values("Month_num")

fig7 = px.bar(
    month_cancel,
    x="arrival_date_month", y="Count",
    color="is_canceled_str",
    barmode="group",
    color_discrete_map={"0":"#00C9A7","1":"#FF6B6B"},
    labels={"is_canceled_str":"Canceled","arrival_date_month":"Month"},
    title="📅 Monthly Bookings vs Cancellations",
    text="Count",
    category_orders={"arrival_date_month": month_order}
)
fig7.update_traces(textposition="outside", textfont_size=9,
                  marker_line_color="#1a1a2e", marker_line_width=1)
fig7.update_layout(title_x=0.5, height=480, xaxis_tickangle=-35,
                  legend_title="Canceled (1=Yes)")

tab1, tab2 = st.tabs([
    "Relationships & Segments",
    "Advanced Visuals"
])

with tab1:

    st.plotly_chart(fig_hotel_cancel, use_container_width=True)

    with st.expander("🏨 Hotel Type vs Cancellation Insights"):
        st.markdown("""
        - City Hotels account for the majority of bookings and cancellations.
        - Resort Hotels have lower booking volume but generally more committed guests.
        - Hotel type significantly influences cancellation behavior.
        """)

    st.markdown("""<hr style="border:1px solid white;">""",
                unsafe_allow_html=True)

    st.plotly_chart(fig_customer_cancel, use_container_width=True)

    with st.expander("👥 Customer Type & Cancellation Insights"):
        st.markdown("""
        - Transient customers dominate bookings across both hotel types.
        - Most cancellations originate from Transient guests.
        - Contract customers exhibit the most reliable booking behavior.
        - Cancellation reduction efforts should focus on Transient travelers.
        """)

    st.markdown("""<hr style="border:1px solid white;">""",
                unsafe_allow_html=True)

    st.plotly_chart(fig_segment, use_container_width=True)

    with st.expander("📊 Market Segment Insights"):
        st.markdown("""
        - Online and Offline Travel Agents contribute a major share of bookings.
        - Direct bookings generally indicate stronger customer intent.
        - Different market segments exhibit varying cancellation patterns.
        """)

    st.markdown("""<hr style="border:1px solid white;">""",
                unsafe_allow_html=True)

    st.plotly_chart(fig_adr_hotel, use_container_width=True)

    with st.expander("💰 ADR Distribution Insights"):
        st.markdown("""
        - ADR distribution is right-skewed.
        - A small number of premium bookings generate significantly higher revenue.
        - Resort Hotels often show greater ADR variability.
        - Outliers indicate luxury or peak-season reservations.
        """)


with tab2:

    st.plotly_chart(fig_room_adr, use_container_width=True)

    with st.expander("🛏️ Room Type vs ADR Insights"):
        st.markdown("""
        - ADR varies considerably across room categories.
        - Premium room types command significantly higher rates.
        - Certain room types contain extreme ADR outliers.
        - Room upgrades can contribute substantially to revenue.
        """)

    st.markdown("""<hr style="border:1px solid white;">""",
                unsafe_allow_html=True)

    st.plotly_chart(fig_Lead_Time_Distribution_by_Cancellation,
                    use_container_width=True)

    with st.expander("⏳ Lead Time Distribution Insights"):
        st.markdown("""
         - The distribution is **heavily right-skewed**, with most bookings         made        within the first **100 days** before arrival.
    - Guests with **short lead times are less likely to cancel**, indicating stronger booking commitment.
    - Cancellation frequency increases as lead time increases, suggesting that bookings made far in advance carry higher uncertainty.
    - A noticeable concentration of cancellations occurs between **100–300 days** of lead time.
    - Very long lead-time bookings (>400 days) are rare but show a relatively higher cancellation tendency.
    - Hotels may benefit from implementing reminder campaigns, flexible pricing, or deposit policies for bookings made far in advance.
    - Lead time appears to be an important factor influencing cancellation behavior and should be considered in predictive modeling.
    """)

    st.markdown("""<hr style="border:1px solid white;">""",
                unsafe_allow_html=True)

    st.plotly_chart(fig7, use_container_width=True)

    with st.expander("📅 Monthly Booking & Cancellation Insights"):
         st.markdown("""
    - Booking volume follows a clear seasonal trend throughout the year.
    - **August records the highest number of bookings** and also the highest number of cancellations.
    - Booking demand steadily increases from January and peaks during the summer months (July–August).
    - Cancellations generally rise alongside booking volume, indicating that higher demand periods naturally generate more cancellations.
    - Despite increased cancellations, successful bookings consistently exceed canceled bookings in every month.
    - November and December experience a noticeable decline in both bookings and cancellations, reflecting off-season demand.
    - The cancellation gap is relatively larger during peak travel months, suggesting increased uncertainty in advance reservations.
    - Hotels should focus on cancellation management strategies during high-demand periods to maximize occupancy and revenue.
    """)


    st.plotly_chart(fig1, use_container_width=True)

    with st.expander("📈 Monthly ADR Trend Insights"):
        st.markdown("""
        - ADR fluctuates throughout the year, indicating seasonality.
        - Some room types experience stronger price increases during peak periods.
        - Revenue optimization opportunities exist through dynamic pricing.
        - Monitoring room-specific ADR trends helps maximize profitability.
        """)


st.info("""
🔍 Insight:
Transient customers contribute the largest share of cancellations,
while contract customers show the lowest cancellation rate.
""")
