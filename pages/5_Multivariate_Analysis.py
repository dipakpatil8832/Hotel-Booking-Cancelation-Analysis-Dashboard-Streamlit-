import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

@st.cache_data
def load_data():
    return pd.read_csv("data/hotel_bookings_cleaned.csv")

df = load_data()

st.title("📊 Multivariate Analysis")



# 1 Sunburst Chart: Hotel → Customer Type → Cancellation
fig_sunburst = px.sunburst(
    df,
    path=[
        "hotel",
        "customer_type",
        "is_canceled"
    ],
    title="Hotel → Customer Type → Cancellation"
)

# 2 Monthly ADR Trend by Room Type
df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"],format="%Y-%m-%d")
monthly_adr = (
    df.groupby([
        pd.Grouper(
            key="reservation_status_date",
            freq="ME"
        ),
        "assigned_room_type"
    ])["adr"]
    .mean()
    .reset_index()
)
fig_room_trend = px.line(
    monthly_adr,
    x="reservation_status_date",
    y="adr",
    color="assigned_room_type",
    title="Monthly ADR Trend by Room Type"
)

3 # ADR by Room Type & Cancellation (Box Plot)
df["adr"]=df["adr"].clip(upper=500)
fig_adr_by_room_type = px.box(
    df,
    x="assigned_room_type", y="adr",
    color="is_canceled_str",
    color_discrete_map={"0":"#F59E0B","1":"#EF4444"},
    points=False,
    labels={"assigned_room_type":"Room Type","adr":"ADR","is_canceled_str":"Canceled"},
    title="🛏️ ADR by Room Type & Cancellation Status"
)
fig_adr_by_room_type.update_layout(title_x=0.5, height=500, legend_title="Canceled (1=Yes)",
                  boxmode="group")


# 4 Lead Time vs ADR colored by Cancellation
sample = df.sample(min(8000, len(df)), random_state=1)
fig_adr_lead_canced = px.scatter(
    sample,
    x="lead_time", y="adr",
    color="is_canceled_str",
    color_discrete_map={"0":"#00C9A7","1":"#FF6B6B"},
    opacity=0.55,
    labels={"lead_time":"Lead Time (days)","adr":"ADR","is_canceled_str":"Canceled"},
    title="📈 Lead Time vs ADR — Colored by Cancellation Status",
    hover_data=["hotel","market_segment"]
)
fig_adr_lead_canced .update_traces(marker=dict(size=5, line=dict(width=0.3, color="white")))
fig_adr_lead_canced .update_layout(title_x=0.5, height=500, legend_title="Canceled (1=Yes)")

# 5 Lead Time vs ADR by Hotel Type
fig_5 = px.scatter(
    sample,
    x="lead_time", y="adr",
    color="is_canceled_str",
    facet_col="hotel",
    color_discrete_map={ "0": "#F59E0B", "1": "#EF4444" },
    opacity=0.5,
    labels={"lead_time":"Lead Time","adr":"ADR","is_canceled_str":"Canceled"},
    title="🏨 Lead Time vs ADR by Hotel Type"
)

fig_5.update_traces(marker=dict(size=4.5))
fig_5.update_layout(title_x=0.5, height=480, legend_title="Canceled (1=Yes)")
fig_5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# 6 Correlation Heatmap
num_only = df.select_dtypes(include="number").drop(columns=["is_canceled"], errors="ignore")
corr = num_only.corr().round(2)

fig_6= go.Figure(go.Heatmap(
    z          = corr.values,
    x          = corr.columns.tolist(),
    y          = corr.columns.tolist(),
    colorscale = "RdBu_r",
    zmid       = 0,
    text       = corr.values,
    texttemplate="%{text}",
    textfont   = dict(size=10),
    hovertemplate="<b>%{x}</b> × <b>%{y}</b><br>r = %{z}<extra></extra>",
    colorbar   = dict(title="r")
))
fig_6.update_layout(
    title  = dict(text="🔥 Correlation Heatmap — Numeric Features", font_size=20, x=0.5),
    height = 600,
    xaxis  = dict(tickangle=-40, tickfont_size=11),
    yaxis  = dict(tickfont_size=11)
)

# 7 3D Scatter: Lead Time vs ADR vs Stay Nights
fig_3d = px.scatter_3d(
    df.sample(5000),
    x="lead_time",
    y="adr",
    z="total_stay",
    color="hotel",
    title="Lead Time vs ADR vs Stay Nights"
)


tab1, tab2 = st.tabs([
    "Advanced Visuals",
     "Correlation & Trends"
])
DIVIDER = """
<hr style="
border:1px solid white;
margin-top:25px;
margin-bottom:25px;">
"""
with tab1:

    st.plotly_chart(fig_sunburst, use_container_width=True)

    with st.expander("🌞 Hotel → Customer Type → Cancellation Insights"):
        st.markdown("""
        - Transient customers dominate bookings across both hotel types.
        - City Hotels contribute a larger share of cancellations.
        - Customer type significantly influences cancellation behavior.
        """)

    st.markdown(DIVIDER, unsafe_allow_html=True)

    st.plotly_chart(fig_room_trend, use_container_width=True)

    with st.expander("📈 Monthly ADR Trend Insights"):
        st.markdown("""
        - ADR fluctuates throughout the year, indicating seasonality.
        - Premium room categories consistently maintain higher ADR.
        - Peak demand periods drive higher room prices.
        """)

    st.markdown(DIVIDER, unsafe_allow_html=True)

    st.plotly_chart(fig_adr_by_room_type, use_container_width=True)

    with st.expander("🛏️ ADR by Room Type Insights"):
        st.markdown("""
        - Premium room categories command higher ADR.
        - Several room types contain high-value outliers.
        - Room allocation strongly impacts revenue potential.
        """)
    

with tab2:

    st.plotly_chart(fig_adr_lead_canced, use_container_width=True)

    with st.expander("📈 Lead Time vs ADR Insights"):
        st.markdown("""
        - No strong linear relationship exists between Lead Time and ADR.
        - High ADR bookings occur across multiple booking windows.
        - Cancellations are distributed across different price ranges.
        """)

    st.markdown(DIVIDER, unsafe_allow_html=True)

    st.plotly_chart(fig_5, use_container_width=True)

    with st.expander("🏨 Lead Time vs ADR by Hotel Type Insights"):
        st.markdown("""
        - City Hotels show greater booking volume and cancellation activity.
        - Resort Hotels have more concentrated booking patterns.
        - Pricing behavior differs across hotel categories.
        """)

    st.markdown(DIVIDER, unsafe_allow_html=True)

    st.plotly_chart(fig_6, use_container_width=True)

    with st.expander("🔥 Correlation Heatmap Insights"):
        st.markdown("""
        - Most features exhibit weak to moderate correlations.
        - No single variable strongly drives booking outcomes.
        - Booking behavior is influenced by multiple interacting factors.
        """)

    st.markdown(DIVIDER, unsafe_allow_html=True)

    st.plotly_chart(fig_3d, use_container_width=True)

    with st.expander("🌐 3D Scatter Insights"):
        st.markdown("""
        - High ADR bookings appear across varying lead times and stay durations.
        - Most bookings cluster around shorter stays.
        - Pricing patterns depend on several combined factors.
        """)


st.success("""
📌 Key Takeaways

• Customer behavior varies significantly across hotel types.
• Premium room categories generate higher ADR and revenue potential.
• Cancellation patterns are concentrated within specific customer segments.
• Pricing strategies appear to be influenced by seasonality and room allocation.
• Multivariate analysis confirms that booking outcomes depend on a combination of factors rather than a single variable.
""")