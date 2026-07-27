import streamlit as st
import pandas as pd
import duckdb
import os
import sys
from utils_i18n import init_translation, T

# ----------------- UI CONFIG -----------------
st.set_page_config(
    page_title="SwiftHub Control Center",
    page_icon="Dashboard",
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

# Initialize localization
init_translation()
t = T[st.session_state["lang"]]

st.title(t["home_title"])
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### {t['home_welcome']}")
    st.markdown(t["home_desc"])
    
    st.markdown(f"#### {t['home_stack']}")
    st.markdown("""
    - **Storage**: Vectorized Parquet Data Lake (2M+ Records)
    - **Orchestration**: Dockerized Apache Airflow
    - **Transformation**: dbt Core + DuckDB (Star Schema)
    - **Streaming**: Apache Kafka Event Bus
    """)
    
    st.markdown(f"#### {t['home_nav']}")
    st.markdown(t["home_nav_desc"])

with col2:
    st.image("docs/assets/dashboard_preview.png", caption="System Architecture Preview")
    
st.divider()

# Quick System Status
st.markdown(f"### {t['system_status']}")
c1, c2, c3 = st.columns(3)

def check_data():
    return os.path.exists("data/production/transactions.parquet")

def check_duckdb():
    return os.path.exists("data/swifthub.duckdb")

with c1:
    status = t["online"] if check_data() else t["offline"]
    st.metric(t["batch_lake"], status)

with c2:
    status = t["active"] if check_duckdb() else t["pending"]
    st.metric(t["dbt_warehouse"], status)

with c3:
    st.metric(t["last_refresh"], t["today"])
