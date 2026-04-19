import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("🌍 Geospatial Intelligence")
st.markdown("Mapping the density of Super App activities across major Indonesian hubs.")

@st.cache_data(ttl=3600)
def load_geo_data():
    path = "data/production/locations.parquet"
    if not os.path.exists(path):
        return pd.DataFrame()
    # Loading 100k sample for map performance
    df = pd.read_parquet(path, columns=['pickup_lat', 'pickup_long', 'city'])
    df = df.rename(columns={"pickup_lat": "lat", "pickup_long": "lon"})
    return df

geo_df = load_geo_data()

if geo_df.empty:
    st.warning("No geospatial data available. Run the data generation pipeline.")
else:
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown("### 🏬 City Density")
        city_counts = geo_df['city'].value_counts().reset_index()
        st.dataframe(city_counts, use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown("### 🌋 Service Hotspots (Jakarta & Bali focus)")
        st.map(geo_df, size=10, color="#FF4B4B")
        
    st.info("The map shows a 100,000 unit sample distributed via Gaussian Normal across real Indonesian coordinates.")
