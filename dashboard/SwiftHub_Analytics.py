import streamlit as st
import pandas as pd
import duckdb
import os
import sys

# ----------------- UI CONFIG -----------------
st.set_page_config(
    page_title="SwiftHub Control Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Global Styles
st.markdown('''
    <style>
        .premium-card {
            background: linear-gradient(145deg, #1E1E1E, #2A2A2A);
            padding: 24px;
            border-radius: 12px;
            border-left: 4px solid #00D2D3;
            box-shadow: 0 6px 12px rgba(0,0,0,0.4);
            text-align: center;
            transition: transform 0.2s ease-in-out;
        }
        .metric-title { color: #8A92A3; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { color: #FFFFFF; font-size: 2.2rem; font-weight: 800; margin-top: 10px; }
        h1, h2, h3 { font-family: 'Inter', sans-serif; color: #FFFFFF; }
        .stButton>button { background-color: #00D2D3; color: white; border-radius: 8px; border: none; }
    </style>
''', unsafe_allow_html=True)

st.title("⚡ SwiftHub Super App: Executive Home")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Welcome to the Platinum Data Platform
    This portal visualizes the **SwiftHub Data Ecosystem**, an Indonesian Super App simulating millions of transactions across logistics, food, and finances.
    
    #### 🏗️ Architecture Stack
    - **Storage**: Vectorized Parquet Data Lake (2M+ Records)
    - **Orchestration**: Dockerized Apache Airflow
    - **Transformation**: dbt Core + DuckDB (Star Schema)
    - **Streaming**: Apache Kafka Event Bus
    
    #### 🚀 Navigation Guide
    Use the sidebar to explore detailed analytics:
    1. **01_Executive_Overview**: High-level KPIs and business health.
    2. **02_Geospatial_Intelligence**: Heatmaps of Indonesian city hubs.
    3. **03_Fleet_Operations**: RideWay and ParcelPro logistics performance.
    """)

with col2:
    st.image("docs/assets/dashboard_preview.png", caption="System Architecture Preview")
    
st.divider()

# Quick System Status
st.markdown("### 🔌 System Connectivity Status")
c1, c2, c3 = st.columns(3)

def check_data():
    return os.path.exists("data/production/transactions.parquet")

def check_duckdb():
    return os.path.exists("data/swifthub.duckdb")

with c1:
    status = "🟢 ONLINE" if check_data() else "🔴 OFFLINE"
    st.metric("Batch Data Lake", status)

with c2:
    status = "🟢 ACTIVE" if check_duckdb() else "🟡 PENDING"
    st.metric("dbt Analytical Warehouse", status)

with c3:
    st.metric("Last Data Refresh", "Today")
