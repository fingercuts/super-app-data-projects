import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
import os
from utils_i18n import T, fmt_rp

st.set_page_config(layout="wide")

if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"
t = T[st.session_state["lang"]]

st.markdown('''
    <style>
        .premium-card {
            background: linear-gradient(145deg, #1E1E1E, #2A2A2A);
            padding: 24px;
            border-radius: 12px;
            border-left: 4px solid #00D2D3;
            box-shadow: 0 6px 12px rgba(0,0,0,0.4);
            text-align: center;
        }
        .metric-title { color: #8A92A3; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { color: #FFFFFF; font-size: 2.2rem; font-weight: 800; margin-top: 10px; }
    </style>
''', unsafe_allow_html=True)

st.title(t["exec_title"])
st.markdown(t["exec_subtitle"])

try:
    con = duckdb.connect("data/swifthub.duckdb", read_only=True)
    
    # KPIs from normalized Fact table
    metrics = con.execute("""
        SELECT 
            SUM(total_amount) as rev,
            COUNT(*) as tx,
            COUNT(DISTINCT user_id) as users,
            AVG(total_amount) as aov
        FROM fct_transactions
    """).df()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="premium-card"><div class="metric-title">{t["total_revenue"]}</div><div class="metric-value">{fmt_rp(metrics["rev"][0])}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="premium-card"><div class="metric-title">{t["transactions"]}</div><div class="metric-value">{metrics["tx"][0]:,}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="premium-card"><div class="metric-title">{t["active_users"]}</div><div class="metric-value">{metrics["users"][0]:,}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="premium-card"><div class="metric-title">{t["avg_order"]}</div><div class="metric-value">{fmt_rp(metrics["aov"][0])}</div></div>', unsafe_allow_html=True)

    st.divider()

    # Trend Analysis
    st.markdown(f"### {t['revenue_trend']}")
    trend_df = con.execute("""
        SELECT 
            date_trunc('month', transaction_timestamp) as month,
            department,
            SUM(total_amount) as revenue
        FROM fct_transactions
        GROUP BY 1, 2
        ORDER BY 1
    """).df()
    
    fig = px.area(trend_df, x="month", y="revenue", color="department", 
                  template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(xaxis_title="", yaxis_title="Revenue (Rp)", legend_title="Department")
    st.plotly_chart(fig, use_container_width=True)

    con.close()

except Exception as e:
    st.error(f"Error connecting to dbt warehouse: {e}")
    st.info("Ensure you have run 'dbt build' in the dbt_project directory.")
