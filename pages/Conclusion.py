import streamlit as st

st.title("📌 Conclusion & Recommendations")

st.markdown("""
## 🏨 Executive Summary

The Hotel Booking Analysis reveals key patterns in customer behavior, booking trends, pricing strategies, and cancellation risks.

### 📊 Booking Trends
- City Hotels account for the majority of reservations and cancellations.
- Hotel demand exhibits strong seasonality, with peak bookings occurring during July and August.
- Booking activity declines significantly during off-peak months such as January, November, and December.

### 👥 Customer Behavior
- Transient customers represent the largest customer segment.
- Most cancellations originate from Transient guests, particularly in City Hotels.
- Contract customers demonstrate the most reliable booking behavior with the lowest cancellation rates.

### 💰 Revenue & Pricing Insights
- ADR (Average Daily Rate) is highly right-skewed, indicating the presence of premium bookings.
- Premium room categories consistently command higher ADR values.
- ADR fluctuates across seasons, highlighting opportunities for dynamic pricing strategies.

### ⏳ Cancellation Analysis
- Longer lead times are associated with higher cancellation risk.
- Guests booking far in advance are more likely to cancel than those booking closer to arrival.
- Peak travel months generate the highest cancellation volumes due to increased booking activity.

### 🔍 Multivariate Findings
- No single variable strongly determines booking outcomes.
- Booking behavior is influenced by a combination of:
    - Customer Type
    - Hotel Type
    - Lead Time
    - Room Category
    - Seasonality
    - Pricing (ADR)

- Correlation analysis indicates weak-to-moderate relationships among most numerical features.

---
""")

st.success("""
🎯 Business Recommendations

1. Implement targeted cancellation prevention strategies for Transient guests.
2. Apply dynamic pricing during high-demand seasons to maximize ADR and revenue.
3. Introduce incentives for early bookings to reduce cancellation risk.
4. Expand Contract and Group booking channels to diversify customer segments.
5. Focus marketing efforts during low-demand months to improve occupancy rates.
6. Use predictive analytics to identify high-risk cancellations and optimize inventory management.
""")

st.info("""
📈 Final Takeaway

Hotel performance is driven by a combination of customer behavior, seasonality, room allocation, and pricing strategy. Understanding these factors enables hotels to improve occupancy, reduce cancellations, and maximize revenue through data-driven decision-making.
""")