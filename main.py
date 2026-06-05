import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Hotel Booking Analytics",
    page_icon="🏨",
    layout="wide"
)



# Navigation Menu
pg = st.navigation([
    st.Page(
        "home.py",
        title="🏠 Home",
        
    ),
    st.Page(
        "pages/Dashboard.py",
        title="📊 Executive Dashboard",
        
    ),
    st.Page(
        "pages/2_data_distribution_and_outliers.py",
        title="📈 Distribution & Outliers",
       
    ),
    st.Page(
        "pages/3_Univariate_Analysis.py",
        title="🔍 Univariate Analysis",
        
    ),
    st.Page(
        "pages/4_Bivariate_Analysis.py",
        title="🔗 Bivariate Analysis",
        
    ),
    st.Page(
        "pages/5_Multivariate_Analysis.py",
        title="🧠 Multivariate Analysis",
        
    )
])

pg.run()
