import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_dark"
st.title("📊 Data Distribution & Outlier Analysis")

@st.cache_data
def load_data():
    return pd.read_csv("data/hotel_bookings_cleaned.csv")

df = load_data()

tab1, tab2 = st.tabs([
    "Distribution Analysis",
    "Outlier Analysis"
])


with tab1:

    st.header("📈 Distribution Analysis")
    st.markdown("Analyze the distribution of key numerical features in the hotel booking dataset.")

    num_cols = [
        "adr",
        "total_stay",
        "lead_time",
        "total_of_special_requests",
        "family",
        "arrival_date_day_of_month"
    ]

    titles = [
        "Average Daily Rate (ADR)",
        "Total Stay (Nights)",
        "Lead Time (Days)",
        "Special Requests",
        "Family Size",
        "Arrival Date Day of Month"
    ]

    colors = [
        "#FF6B6B",
        "#00C9A7",
        "#FFA048",
        "#A78BFA",
        "#38BDF8",
        "#F472B6"
    ]

    col1, col2 = st.columns(2)

    for i, (feature, title, color) in enumerate(zip(num_cols, titles, colors)):

        fig = px.histogram(
            df,
            x=feature,
            nbins=40,
            title=title
        )

        fig.update_traces(
            marker_color=color,
            opacity=0.85,
            hovertemplate=f"<b>{title}</b><br>Value: %{{x}}<br>Count: %{{y}}<extra></extra>"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20),

            title={
            "x": 0.5,
            "font": {"size": 18, "color": "white"}
                 },

            xaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False,
                color="white"
                
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False,
                color="white"
            )
        )

        if i % 2 == 0:
            with col1:
                st.plotly_chart(fig, use_container_width=True)
        else:
            with col2:
                st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📋 Summary Statistics")

    

    st.dataframe(
        df[num_cols].describe().T,
        use_container_width=True
    )

with tab2:

    st.header("📦 Outlier Analysis")
    st.markdown("Identify outliers and understand data spread using Box and Violin plots.")

    plots = [
        ("arrival_date_day_of_month", "Arrival Day of Month", "box", "#FFA048"),
        ("adr", "Average Daily Rate (ADR)", "box", "#38BDF8"),
        ("total_stay", "Total Stay (Nights)", "violin", "#00C9A7"),
        ("total_of_special_requests", "Special Requests", "box", "#A78BFA"),
        ("family", "Family Size", "violin", "#FF6B6B"),
        ("lead_time", "Lead Time", "box", "#F472B6")
    ]

    col1, col2 = st.columns(2)

    for i, (column, title, kind, color) in enumerate(plots):

        fig = go.Figure()

        if kind == "box":

            fig.add_trace(
                go.Box(
                    x=df[column],
                    marker_color=color,
                    boxmean=True,
                    hovertemplate=f"<b>{title}</b><br>Value: %{{x}}<extra></extra>"
                )
            )

        else:

            fig.add_trace(
                go.Violin(
                    x=df[column],
                    fillcolor=color,
                    opacity=0.75,
                    line_color="white",
                    box_visible=True,
                    meanline_visible=True,
                    hovertemplate=f"<b>{title}</b><br>Value: %{{x}}<extra></extra>"
                )
            )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            title={
                "text": title,
                "x": 0.5,
                "font": {"size": 18,"color": "white"}
            },
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20),

            xaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                zeroline=False
            )
        )

        if i % 2 == 0:
            with col1:
                st.plotly_chart(fig, use_container_width=True)
        else:
            with col2:
                st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📊 Outlier Summary (IQR Method)")

    outlier_summary = []

    for column, _, _, _ in plots:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[column] < lower) | (df[column] > upper)]

        outlier_summary.append({
            "Feature": column,
            "Outliers": len(outliers),
            "Outlier %": round((len(outliers) / len(df)) * 100, 2)
        })

    st.dataframe(
        pd.DataFrame(outlier_summary),
        use_container_width=True
    )



st.subheader("📌 Distribution Insights")

with st.expander("📊 ADR (Average Daily Rate)"):
    st.markdown("""
    - ADR is right-skewed.
    - Most bookings have ADR between **50–150**.
    - A small number of bookings have ADR above **300**.
    - Revenue is influenced by a small segment of high-paying customers.
    """)

with st.expander("🏨 Total Stay"):
    st.markdown("""
    - Most guests stay for **1–4 nights**.
    - Long stays (>10 nights) are rare.
    - The hotel business is driven primarily by short-term travelers.
    """)

with st.expander("⏳ Lead Time"):
    st.markdown("""
    - Lead time is heavily right-skewed.
    - Most bookings occur within **0–100 days** before arrival.
    - Some reservations are made over **400 days** in advance.
    - Longer lead times may indicate higher cancellation risk.
    """)

with st.expander("⭐ Special Requests"):
    st.markdown("""
    - Most guests make **no special requests**.
    - Requests become less common as the count increases.
    - Guests with multiple requests may represent a premium segment.
    """)

with st.expander("👨‍👩‍👧 Family Size"):
    st.markdown("""
    - Most bookings involve **1–2 guests**.
    - Large families/groups are uncommon.
    - Demand is concentrated among small travel groups.
    """)