import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px
from datetime import datetime
from utils_i18n import T

# Setup paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.sla_tracker import SLATracker

# Page configuration
st.set_page_config(
    page_title="SwiftHub SLA Center",
    page_icon="",
    layout="wide"
)

if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"
t = T[st.session_state["lang"]]

# Custom premium styling
st.markdown('''
    <style>
        .sla-card {
            background: linear-gradient(135deg, #1A2E26, #111e18);
            padding: 24px;
            border-radius: 12px;
            border-left: 4px solid #10B981;
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            text-align: center;
        }
        .sla-title { color: #A7F3D0; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }
        .sla-value { color: #FFFFFF; font-size: 2.8rem; font-weight: 800; margin-top: 10px; }
        h1, h2, h3 { color: #FFFFFF; font-family: 'Inter', sans-serif; }
    </style>
''', unsafe_allow_html=True)

st.title(t["sla_title"])
st.markdown(t["sla_subtitle"])
st.divider()

tracker = SLATracker()
stats = tracker.get_aggregate_stats()
history = tracker.get_compliance_history(30)

# Executive KPI display
c1, c2, c3, c4 = st.columns(4)

with c1:
    sla = stats.get("avg_sla", 0.0)
    sla_color = "#10B981" if sla >= 99.5 else ("#F59E0B" if sla >= 95.0 else "#EF4444")
    st.markdown(f'''
        <div class="sla-card" style="border-left-color: {sla_color};">
            <div class="sla-title">{t["rolling_sla"]}</div>
            <div class="sla-value" style="color: {sla_color};">{sla:.2f}%</div>
        </div>
    ''', unsafe_allow_html=True)

with c2:
    st.markdown(f'''
        <div class="sla-card" style="border-left-color: #3B82F6;">
            <div class="sla-title">{t["total_runs"]}</div>
            <div class="sla-value">{stats.get("total_runs", 0)}</div>
        </div>
    ''', unsafe_allow_html=True)

with c3:
    st.markdown(f'''
        <div class="sla-card" style="border-left-color: #10B981;">
            <div class="sla-title">{t["passed"]}</div>
            <div class="sla-value">{stats.get("total_passed", 0):,}</div>
        </div>
    ''', unsafe_allow_html=True)

with c4:
    fail_color = "#EF4444" if stats.get("total_failed", 0) > 0 else "#10B981"
    st.markdown(f'''
        <div class="sla-card" style="border-left-color: {fail_color};">
            <div class="sla-title">{t["failed"]}</div>
            <div class="sla-value" style="color: {fail_color};">{stats.get("total_failed", 0):,}</div>
        </div>
    ''', unsafe_allow_html=True)

st.divider()

if not history:
    st.info(t["no_history"])
else:
    # Build dataframe for Plotly
    df = pd.DataFrame(history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    
    col_chart, col_table = st.columns([3, 2])
    
    with col_chart:
        st.subheader(t["sla_trend"])
        # Line chart showing pass_rate trend
        fig = px.line(
            df, 
            x="timestamp", 
            y="pass_rate", 
            markers=True,
            labels={"timestamp": t["exec_time"], "pass_rate": t["pass_rate"]},
            title=t["sla_chart_title"]
        )
        fig.add_hline(y=99.5, line_dash="dash", line_color="red", annotation_text="Target SLA (99.5%)")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_range=[90, 101]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_table:
        st.subheader(t["job_history"])
        
        # Clean history dataframe for tabular representation
        table_df = df.copy().sort_values("timestamp", ascending=False)
        table_df["Time"] = table_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        table_df = table_df.rename(columns={
            "run_id": "Job ID",
            "total_checks": "Total Checks",
            "passed_checks": "Passed",
            "failed_checks": "Failed",
            "pass_rate": "SLA %"
        })
        
        st.dataframe(
            table_df[["Job ID", "Time", "Total Checks", "Passed", "Failed", "SLA %"]],
            hide_index=True,
            use_container_width=True
        )
