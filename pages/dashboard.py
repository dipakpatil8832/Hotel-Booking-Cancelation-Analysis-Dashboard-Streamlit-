import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.markdown("""
<style>
.hero {
    position: relative;
    height: 250px;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 0px;
    background-image: url('https://images.unsplash.com/photo-1566073771259-6a8506099945');
    background-size: cover;
    background-position: center;
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.65);
}

.hero-content {
    position: relative;
    z-index: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 60px;
}

.hero-title {
    color: white;
    font-size: 50px;
    font-weight: 800;
}

.hero-subtitle {
    color: #E5E7EB;
    font-size: 22px;
    margin-top: 10px;
}
</style>

<div class="hero">
    <div class="hero-content">
        <div class="hero-title">
             Hotel Booking Analysis Dashboard
        </div>

        
    
</div>

""", unsafe_allow_html=True)

st.markdown("---")
# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- imports ---- */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ---- main background ---- */
.stApp { background: #0D1117; }
section[data-testid="stSidebar"] { background: #161B22; border-right: 1px solid #21262D; }

/* ---- hide streamlit chrome ---- */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem; max-width: 100%; }

/* ---- KPI card ---- */
.kpi-card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}
.kpi-card:hover { border-color: #388BFD; }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.blue::before   { background: #388BFD; }
.kpi-card.green::before  { background: #3FB950; }
.kpi-card.red::before    { background: #F85149; }
.kpi-card.amber::before  { background: #D29922; }
.kpi-card.purple::before { background: #8B5CF6; }
.kpi-card.teal::before   { background: #39D353; }

.kpi-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: #8B949E;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 600;
    color: #E6EDF3;
    line-height: 1;
    margin-bottom: 6px;
    font-family: 'DM Mono', monospace;
}
.kpi-delta {
    font-size: 12px;
    font-weight: 500;
}
.kpi-delta.pos { color: #3FB950; }
.kpi-delta.neg { color: #F85149; }
.kpi-delta.neu { color: #8B949E; }

/* ---- section header ---- */
.section-header {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #8B949E;
    border-left: 3px solid #388BFD;
    padding-left: 10px;
    margin: 1.5rem 0 1rem;
}

/* ---- insight box ---- */
.insight-box {
    background: #161B22;
    border: 1px solid #21262D;
    border-left: 4px solid #388BFD;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    font-size: 13px;
    color: #8B949E;
    margin: 0.5rem 0;
    line-height: 1.6;
}
.insight-box strong { color: #E6EDF3; }

/* ---- metric container override ---- */
[data-testid="metric-container"] {
    background: #161B22 !important;
    border: 1px solid #21262D !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}

/* ---- sidebar elements ---- */
.sidebar-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #8B949E;
    margin: 1rem 0 .4rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data loading ───────────────────────────────────────────────────────────────
MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

@st.cache_data
def load_data():
    df = pd.read_csv("data/hotel_bookings_cleaned.csv")
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])
    df["arrival_date_month"] = pd.Categorical(
        df["arrival_date_month"], categories=MONTH_ORDER, ordered=True
    )
    df["is_cancelled_bool"] = df["is_canceled"] == "Yes"
    df["adr"] = df["adr"].clip(upper=500)
    return df

df_raw = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    st.markdown('<div class="sidebar-title">Hotel Type</div>', unsafe_allow_html=True)
    hotels = st.multiselect(
        label="hotel_type",
        options=df_raw["hotel"].unique().tolist(),
        default=df_raw["hotel"].unique().tolist(),
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-title">Year</div>', unsafe_allow_html=True)
    years = st.multiselect(
        label="year",
        options=sorted(df_raw["arrival_date_year"].unique().tolist()),
        default=sorted(df_raw["arrival_date_year"].unique().tolist()),
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-title">Market Segment</div>', unsafe_allow_html=True)
    segments = st.multiselect(
        label="segment",
        options=df_raw["market_segment"].unique().tolist(),
        default=df_raw["market_segment"].unique().tolist(),
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-title">Customer Type</div>', unsafe_allow_html=True)
    cust_types = st.multiselect(
        label="customer_type",
        options=df_raw["customer_type"].unique().tolist(),
        default=df_raw["customer_type"].unique().tolist(),
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        '<div style="font-size:11px;color:#8B949E;text-align:center">119,390 records · 2015–2017</div>',
        unsafe_allow_html=True,
    )

# ── Filter ─────────────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["hotel"].isin(hotels) &
    df_raw["arrival_date_year"].isin(years) &
    df_raw["market_segment"].isin(segments) &
    df_raw["customer_type"].isin(cust_types)
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()

# ── Helper: Plotly dark theme ──────────────────────────────────────────────────
DARK_LAYOUT = dict(
    paper_bgcolor="#0D1117",
    plot_bgcolor="#0D1117",
    font=dict(color="#8B949E", family="DM Sans", size=12),
    xaxis=dict(gridcolor="#21262D", linecolor="#21262D", zerolinecolor="#21262D"),
    yaxis=dict(gridcolor="#21262D", linecolor="#21262D", zerolinecolor="#21262D"),
    margin=dict(l=10, r=10, t=40, b=10),
    title_font=dict(color="#E6EDF3", size=14, family="DM Sans"),
)

LEGEND_DEFAULT = dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262D", font=dict(color="#8B949E"))
LEGEND_H       = dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262D", font=dict(color="#8B949E"), orientation="h", y=1.08, x=0)
LEGEND_H_BOT   = dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262D", font=dict(color="#8B949E"), orientation="h", y=-0.05)
LEGEND_H_TOP   = dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262D", font=dict(color="#8B949E"), orientation="h", y=1.08)

PALETTE = {
    "blue":   "#388BFD",
    "green":  "#3FB950",
    "red":    "#F85149",
    "amber":  "#D29922",
    "purple": "#8B5CF6",
    "teal":   "#39D353",
    "coral":  "#FF7B72",
    "muted":  "#8B949E",
}
SEQ_COLORS = [PALETTE["blue"], PALETTE["green"], PALETTE["amber"],
              PALETTE["purple"], PALETTE["coral"], PALETTE["teal"], PALETTE["red"]]

# ── Derived stats ──────────────────────────────────────────────────────────────
total       = len(df)/1000
cancel_rate = df["is_cancelled_bool"].mean() * 100
avg_adr     = df["adr"].mean()
avg_lead    = df["lead_time"].mean()
avg_stay    = df["total_stay"].mean()
repeat_pct  = df["is_repeated_guest"].mean() * 100
special_req = df["total_of_special_requests"].mean()
revenue_est = (df["adr"] * df["total_stay"]).sum()

# ── Page title ─────────────────────────────────────────────────────────────────
# st.markdown("""
# <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:.25rem">
#   <h1 style="font-size:24px;font-weight:600;color:#E6EDF3;margin:0">Hotel Booking Analytics</h1>
#   <span style="font-size:13px;color:#8B949E">Executive Dashboard</span>
# </div>
# <div style="font-size:12px;color:#8B949E;margin-bottom:1.5rem">
#   Showing <strong style="color:#E6EDF3">{:,}</strong> bookings across <strong style="color:#E6EDF3">{}</strong>
# </div>
# """.format(total, ", ".join(hotels)), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — KPI Cards
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

def kpi_card(label, value, delta_text, delta_type, color):
    return f"""
<div class="kpi-card {color}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-delta {delta_type}">{delta_text}</div>
</div>"""

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(kpi_card("Total Bookings", f"{total:,}k", "All filtered records", "neu", "blue"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card("Avg Daily Rate", f"{avg_adr:.2f}", "City: 105 · Resort: 95", "neu", "green"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card("Cancellation Rate", f"{cancel_rate:.1f}%", "City: 41.7% · Resort: 27.8%", "neg", "red"), unsafe_allow_html=True)
with c4:
    st.markdown(kpi_card("Avg Lead Time", f"{avg_lead:.0f} Days", "Days before check-in", "neu", "amber"), unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.markdown(kpi_card("Est. Total Revenue", f"{revenue_est/1e6:.1f}M", "ADR ×days' stayed", "pos", "purple"), unsafe_allow_html=True)
with c6:
    st.markdown(kpi_card("Avg Stay Duration", f"{avg_stay:.1f} Days", "Per booking", "neu", "teal"), unsafe_allow_html=True)
with c7:
    st.markdown(kpi_card("Repeat Guest Rate", f"{repeat_pct:.1f}%", "Returning customers", "pos", "green"), unsafe_allow_html=True)
with c8:
    st.markdown(kpi_card("Avg Special Requests", f"{special_req:.2f}", "Per booking", "neu", "blue"), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Overview: Monthly Trends + Hotel Split
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Booking Overview</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    # Monthly bookings stacked bar
    monthly = (df.groupby(["arrival_date_month", "hotel"], observed=True)
                 .size().reset_index(name="Count"))
    monthly["arrival_date_month"] = monthly["arrival_date_month"].astype(str)

    fig_monthly = px.bar(
        monthly, x="arrival_date_month", y="Count", color="hotel",
        color_discrete_map={"City Hotel": PALETTE["blue"], "Resort Hotel": PALETTE["green"]},
        barmode="stack",
        labels={"arrival_date_month": "Month", "Count": "Bookings", "hotel": "Hotel"},
    )
    fig_monthly.update_layout(**DARK_LAYOUT, title="Monthly Booking Volume", height=300, legend=LEGEND_H)
    fig_monthly.update_traces(marker_line_width=0)
    st.plotly_chart(fig_monthly, use_container_width=True)

with col_right:
    # Hotel type donut
    hotel_counts = df["hotel"].value_counts().reset_index()
    hotel_counts.columns = ["hotel", "count"]
    fig_donut = go.Figure(go.Pie(
        labels=hotel_counts["hotel"], values=hotel_counts["count"],
        hole=0.62,
        marker=dict(colors=[PALETTE["blue"], PALETTE["green"]], line=dict(color="#0D1117", width=2)),
        textinfo="percent", textfont=dict(color="#E6EDF3", size=12),
        hovertemplate="<b>%{label}</b><br>%{value:,} bookings<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b>{total:,}</b><br>Total",
        x=0.5, y=0.5, showarrow=False,
        font=dict(color="#E6EDF3", size=14, family="DM Mono"),
    )
    fig_donut.update_layout(**DARK_LAYOUT, title="Hotel Split", height=300,  legend=LEGEND_H_BOT)
    st.plotly_chart(fig_donut, use_container_width=True)

# Year-over-year trend
monthly_year = (df.groupby(["arrival_date_month", "arrival_date_year"], observed=True)
                  .size().reset_index(name="Count"))
monthly_year["arrival_date_month"] = monthly_year["arrival_date_month"].astype(str)
monthly_year["arrival_date_year"] = monthly_year["arrival_date_year"].astype(str)

fig_yoy = px.line(
    monthly_year, x="arrival_date_month", y="Count", color="arrival_date_year",
    color_discrete_sequence=[PALETTE["blue"], PALETTE["green"], PALETTE["amber"]],
    markers=True,
    labels={"arrival_date_month": "Month", "Count": "Bookings", "arrival_date_year": "Year"},
)
fig_yoy.update_layout(**DARK_LAYOUT, title="Year-over-Year Monthly Trend", height=260, legend=LEGEND_H)
fig_yoy.update_traces(line=dict(width=2), marker=dict(size=5))
st.plotly_chart(fig_yoy, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Revenue & ADR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Revenue & Average Daily Rate</div>', unsafe_allow_html=True)

ra1, ra2 = st.columns(2)

with ra1:
    # ADR by hotel violin
    VIOLIN_FILLS = {
        "City Hotel":   "rgba(56,139,253,0.15)",
        "Resort Hotel": "rgba(63,185,80,0.15)",
    }
    fig_violin = go.Figure()
    for hotel, color in [("City Hotel", PALETTE["blue"]), ("Resort Hotel", PALETTE["green"])]:
        sub = df[df["hotel"] == hotel]["adr"]
        fig_violin.add_trace(go.Violin(
            y=sub, name=hotel, line_color=color,
            fillcolor=VIOLIN_FILLS[hotel],
            box_visible=True, meanline_visible=True,
            points=False,
        ))
    fig_violin.update_layout(**DARK_LAYOUT, title="ADR Distribution by Hotel", height=320, legend=LEGEND_H_TOP)
    st.plotly_chart(fig_violin, use_container_width=True)

with ra2:
    # ADR by room type box
    fig_room = px.box(
        df, x="assigned_room_type", y="adr", color="assigned_room_type",
        color_discrete_sequence=SEQ_COLORS,
        labels={"assigned_room_type": "Room Type", "adr": "ADR ($)"},
        points=False,
    )
    fig_room.update_layout(**DARK_LAYOUT, title="ADR by Room Type", height=320,
                            showlegend=False)
    st.plotly_chart(fig_room, use_container_width=True)

# Monthly ADR trend
monthly_adr = (df.groupby(["arrival_date_month", "hotel"], observed=True)["adr"]
                 .mean().reset_index())
monthly_adr["arrival_date_month"] = monthly_adr["arrival_date_month"].astype(str)

fig_adr_trend = px.line(
    monthly_adr, x="arrival_date_month", y="adr", color="hotel",
    color_discrete_map={"City Hotel": PALETTE["blue"], "Resort Hotel": PALETTE["green"]},
    markers=True,
    labels={"arrival_date_month": "Month", "adr": "Avg ADR ($)", "hotel": "Hotel"},
)
fig_adr_trend.update_traces(line=dict(width=2), marker=dict(size=6))
fig_adr_trend.update_layout(**DARK_LAYOUT, title="Monthly ADR Trend by Hotel", height=280, legend=LEGEND_H)
st.plotly_chart(fig_adr_trend, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — Booking Behavior
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Booking Behavior</div>', unsafe_allow_html=True)

bb1, bb2 = st.columns(2)

with bb1:
    # Stay duration distribution
    stay_dist = df["total_stay"].value_counts().reset_index()
    stay_dist.columns = ["Nights", "Count"]
    stay_dist = stay_dist[stay_dist["Nights"] <= 15].sort_values("Nights")
    fig_stay = px.bar(
        stay_dist, x="Nights", y="Count",
        color="Count", color_continuous_scale=[[0, "#21262D"], [1, PALETTE["teal"]]],
        labels={"Nights": "Total Nights", "Count": "Bookings"},
        title="Stay Duration Distribution",
        text="Count",
    )
    fig_stay.update_traces(texttemplate="%{text:,}", textposition="outside",
                            textfont=dict(size=9), marker_line_width=0)
    fig_stay.update_layout(**DARK_LAYOUT, height=320, showlegend=False,
                            coloraxis_showscale=False)
    st.plotly_chart(fig_stay, use_container_width=True)

with bb2:
    # Booking changes distribution
    changes_dist = (df["booking_changes"].value_counts().reset_index()
                      .rename(columns={"booking_changes":"Changes","count":"Count"}))
    changes_dist = changes_dist[changes_dist["Changes"] <= 8].sort_values("Changes")
    fig_changes = px.bar(
        changes_dist, x="Changes", y="Count",
        color="Count", color_continuous_scale=[[0, "#21262D"], [1, PALETTE["amber"]]],
        labels={"Changes": "Number of Changes", "Count": "Bookings"},
        title="Booking Modifications Distribution",
        text="Count",
    )
    fig_changes.update_traces(texttemplate="%{text:,}", textposition="outside",
                               textfont=dict(size=9), marker_line_width=0)
    fig_changes.update_layout(**DARK_LAYOUT, height=320, showlegend=False,
                               coloraxis_showscale=False)
    st.plotly_chart(fig_changes, use_container_width=True)

# Repeated guest cancellation comparison
repeat_cancel = (df.groupby("is_repeated_guest")["is_cancelled_bool"]
                   .mean().mul(100).reset_index())
repeat_cancel["Guest Type"] = repeat_cancel["is_repeated_guest"].map({0: "New Guest", 1: "Repeat Guest"})
repeat_cancel.columns = ["is_repeated_guest","Cancel Rate (%)","Guest Type"]

bb3, bb4 = st.columns(2)
with bb3:
    fig_repeat = px.bar(
        repeat_cancel, x="Guest Type", y="Cancel Rate (%)",
        color="Guest Type",
        color_discrete_map={"New Guest": PALETTE["red"], "Repeat Guest": PALETTE["green"]},
        text=repeat_cancel["Cancel Rate (%)"].apply(lambda v: f"{v:.1f}%"),
        title="New vs Repeat Guest — Cancel Rate",
        labels={"Guest Type": ""},
    )
    fig_repeat.update_traces(textposition="outside", textfont=dict(size=13, color="#E6EDF3"),
                              marker_line_width=0)
    fig_repeat.update_layout(**DARK_LAYOUT, height=300, showlegend=False)
    st.plotly_chart(fig_repeat, use_container_width=True)

with bb4:
    # Special requests vs cancellation
    req_cancel = (df.groupby("total_of_special_requests")["is_cancelled_bool"]
                    .mean().mul(100).reset_index())
    req_cancel = req_cancel[req_cancel["total_of_special_requests"] <= 5]
    req_cancel.columns = ["Special Requests", "Cancel Rate (%)"]
    fig_req_c = px.line(
        req_cancel, x="Special Requests", y="Cancel Rate (%)",
        markers=True,
        color_discrete_sequence=[PALETTE["purple"]],
        title="Special Requests vs Cancel Rate",
        labels={"Special Requests": "No. of Special Requests"},
    )
    fig_req_c.update_traces(line=dict(width=2.5), marker=dict(size=9, color=PALETTE["purple"],
                                                               line=dict(color="#0D1117", width=2)))
    fig_req_c.update_layout(**DARK_LAYOUT, height=300)
    st.plotly_chart(fig_req_c, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — Raw Data Explorer
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Data Explorer</div>', unsafe_allow_html=True)

with st.expander("View filtered dataset", expanded=False):
    display_cols = ["hotel","arrival_date_year","arrival_date_month","market_segment",
                    "customer_type","assigned_room_type","is_canceled","lead_time",
                    "adr","total_stay","booking_changes","total_of_special_requests"]
    st.dataframe(df[display_cols].head(500), use_container_width=True, height=340)

col_dl1, col_dl2 = st.columns([1, 4])
with col_dl1:
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="⬇ Download filtered CSV",
        data=csv_data,
        file_name="hotel_bookings_filtered.csv",
        mime="text/csv",
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:11px;color:#8B949E;padding:.5rem 0">'
    'Hotel Booking Analytics Dashboard · Built with Streamlit & Plotly · Data: 2015–2017'
    '</div>',
    unsafe_allow_html=True,
)