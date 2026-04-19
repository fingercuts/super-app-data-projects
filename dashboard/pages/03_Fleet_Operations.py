import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

st.set_page_config(layout="wide")

def get_db_connection():
    return duckdb.connect("data/swifthub.duckdb", read_only=True)

st.title("🚜 Fleet & Logistics Operations")
st.markdown("Analyzing RideWay and ParcelPro operational efficiency and driver ratings.")

try:
    con = get_db_connection()
    
    # Driver Metrics
    driver_stats = con.execute("""
        SELECT 
            vehicle_type,
            COUNT(*) as driver_count,
            AVG(driver_rating) as avg_rating
        FROM dim_drivers
        GROUP BY 1
    """).df()

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏍️ Fleet Composition")
        fig_pie = px.pie(driver_stats, names="vehicle_type", values="driver_count", hole=0.5,
                         template="plotly_dark", color_discrete_sequence=['#00D2D3', '#FF4B4B'])
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.markdown("### ⭐ Driver Performance Index")
        fig_bar = px.bar(driver_stats, x="vehicle_type", y="avg_rating", color="vehicle_type",
                         template="plotly_dark", color_discrete_sequence=['#00D2D3', '#FF4B4B'])
        fig_bar.update_layout(showlegend=False, yaxis_range=[4.0, 5.0])
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # Logistical Load by City
    st.markdown("### 🏙️ Logistical Request Density by City")
    city_load = con.execute("""
        SELECT 
            city,
            department,
            COUNT(*) as tx_count
        FROM fct_transactions
        WHERE department IN ('RideWay', 'ParcelPro')
        GROUP BY 1, 2
        ORDER BY 3 DESC
    """).df()
    
    fig_city = px.bar(city_load, x="city", y="tx_count", color="department", barmode="group",
                      template="plotly_dark")
    st.plotly_chart(fig_city, use_container_width=True)

    con.close()

except Exception as e:
    st.error(f"Error accessing logistics data: {e}")
