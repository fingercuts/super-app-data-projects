import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils_i18n import T

st.set_page_config(layout="wide")

if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"
t = T[st.session_state["lang"]]

# Styling override
st.markdown('''
    <style>
        .reportview-container {
            background: #0e1117;
        }
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            color: #FFFFFF;
        }
    </style>
''', unsafe_allow_html=True)

st.title(t["geo_title"])
st.markdown(t["geo_subtitle"])

@st.cache_data(ttl=3600)
def load_geo_data():
    path = "data/production/locations.parquet"
    if not os.path.exists(path):
        # Fallback to local staging or root if paths differ in container
        alt_path = "../data/production/locations.parquet"
        if os.path.exists(alt_path):
            path = alt_path
        else:
            return pd.DataFrame()
            
    # Load sample for performance
    df = pd.read_parquet(path)
    if 'pickup_lat' in df.columns and 'pickup_long' in df.columns:
        df = df.rename(columns={"pickup_lat": "lat", "pickup_long": "lon"})
    return df

geo_df = load_geo_data()

if geo_df.empty:
    st.warning(" NO-GEO data available. Please run data generation first.")
else:
    # Set city filter
    all_label = t["all_cities"]
    cities = [all_label] + list(geo_df['city'].unique())
    selected_city = st.selectbox(t["select_city"], cities)
    
    if selected_city != all_label:
        map_df = geo_df[geo_df['city'] == selected_city]
    else:
        map_df = geo_df

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"### {t['demand_dist']}")
        city_counts = geo_df['city'].value_counts().reset_index()
        city_counts.columns = [t['city_hub'], t['request_count']]
        st.dataframe(
            city_counts,
            use_container_width=True,
            hide_index=True
        )
        
        # Add dynamic metrics for selected view
        st.metric(t["total_in_view"], f"{len(map_df):,}")
        st.metric(t["avg_lat"], f"{map_df['lat'].mean():.4f}")
        st.metric(t["avg_lon"], f"{map_df['lon'].mean():.4f}")

    with col2:
        st.markdown(f"### {t['hotspot']}")
        
        # Build premium dark mapbox scatter plot
        fig = px.scatter_mapbox(
            map_df.head(20000), # Cap at 20k points for sub-second page rendering
            lat="lat",
            lon="lon",
            color="city",
            hover_name="city",
            zoom=10 if selected_city != all_label else 4.5,
            mapbox_style="carto-darkmatter",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(10, 10, 10, 0.8)",
                font=dict(color="#ffffff")
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.info(t["pro_tip"])

