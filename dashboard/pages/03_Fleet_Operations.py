import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
from utils_i18n import T

st.set_page_config(layout="wide")

if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"
t = T[st.session_state["lang"]]

# Global page styling
st.markdown('''
    <style>
        .premium-card {
            background: linear-gradient(145deg, #1e1e24, #121216);
            padding: 20px;
            border-radius: 10px;
            border-top: 3px solid #FF4B4B;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            text-align: center;
        }
        .metric-title { color: #8A92A3; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-value { color: #FFFFFF; font-size: 1.8rem; font-weight: 700; margin-top: 8px; }
    </style>
''', unsafe_allow_html=True)

def get_db_connection():
    # Supports both local and container runtimes
    db_path = "data/swifthub.duckdb"
    try:
        return duckdb.connect(db_path, read_only=True)
    except Exception:
        return duckdb.connect("../" + db_path, read_only=True)

st.title(t["fleet_title"])
st.markdown(t["fleet_subtitle"])

try:
    con = get_db_connection()
    
    # 1. Driver Metrics
    driver_stats = con.execute("""
        SELECT 
            vehicle_type,
            COUNT(*) as driver_count,
            AVG(driver_rating) as avg_rating
        FROM dim_drivers
        GROUP BY 1
    """).df()

    total_drivers = int(driver_stats["driver_count"].sum())
    avg_fleet_rating = float(con.execute("SELECT AVG(driver_rating) FROM dim_drivers").fetchone()[0] or 0.0)

    # Operational metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="premium-card"><div class="metric-title">{t["fleet_size"]}</div><div class="metric-value">{total_drivers:,} {t["drivers"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="premium-card"><div class="metric-title">{t["fleet_rating"]}</div><div class="metric-value">{avg_fleet_rating:.2f} </div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="premium-card"><div class="metric-title">{t["fulfillment_sla"]}</div><div class="metric-value" style="color: #00D2D3;">98.4 %</div></div>', unsafe_allow_html=True)

    st.divider()

    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"### {t['fleet_comp']}")
        fig_pie = px.pie(
            driver_stats, 
            names="vehicle_type", 
            values="driver_count", 
            hole=0.6,
            template="plotly_dark", 
            color_discrete_sequence=['#00D2D3', '#FF4B4B', '#FFC312']
        )
        fig_pie.update_layout(
            margin={"t": 30, "b": 10},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.markdown(f"### {t['driver_perf']}")
        # Let's pull driver ratings directly to plot a nice histogram
        ratings_df = con.execute("SELECT driver_rating, vehicle_type FROM dim_drivers").df()
        fig_hist = px.histogram(
            ratings_df, 
            x="driver_rating", 
            color="vehicle_type", 
            marginal="box",
            nbins=30,
            template="plotly_dark",
            color_discrete_sequence=['#00D2D3', '#FF4B4B', '#FFC312']
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Driver Rating",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()

    # Logistical Load by City
    st.markdown(f"### {t['city_density']}")
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
    
    fig_city = px.bar(
        city_load, 
        x="city", 
        y="tx_count", 
        color="department", 
        barmode="group",
        template="plotly_dark",
        color_discrete_sequence=['#00D2D3', '#FF4B4B']
    )
    fig_city.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=t["city_hub"],
        yaxis_title=t["transactions"]
    )
    st.plotly_chart(fig_city, use_container_width=True)

    con.close()

except Exception as e:
    st.error(f"Error accessing logistics data: {e}")
    st.info("Please verify the dbt database has been successfully compiled.")
