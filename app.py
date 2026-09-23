"""
Gate 3 — Local Taiwan GIS Web
Interactive Dashboard using Streamlit & Folium.
Data is read strictly from data.db (Gate 2).
"""

import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Taiwan Weather GIS", layout="wide", initial_sidebar_state="expanded")

# Taiwan county coordinates mapping since CWA data might miss lat/lon
COORDINATES = {
    "臺北市": [25.0330, 121.5654], "新北市": [25.0112, 121.4617],
    "基隆市": [25.1287, 121.7397], "桃園市": [24.9937, 121.3009],
    "新竹市": [24.8138, 120.9675], "新竹縣": [24.8385, 121.0177],
    "苗栗縣": [24.5601, 120.8234], "臺中市": [24.1477, 120.6736],
    "彰化縣": [24.0820, 120.5385], "南投縣": [23.9037, 120.6698],
    "雲林縣": [23.7092, 120.4313], "嘉義市": [23.4800, 120.4491],
    "嘉義縣": [23.4518, 120.2554], "臺南市": [22.9998, 120.2268],
    "高雄市": [22.6272, 120.3014], "屏東縣": [22.6719, 120.4879],
    "宜蘭縣": [24.7570, 121.7408], "花蓮縣": [23.9871, 121.6015],
    "臺東縣": [22.7583, 121.1444], "澎湖縣": [23.5711, 119.5793],
    "金門縣": [24.4297, 118.3205], "連江縣": [26.1505, 119.9328]
}

@st.cache_data
def load_data():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT * FROM weather_forecasts", conn)
    conn.close()
    
    # Sort out coordinates
    df['display_lat'] = df.apply(lambda row: COORDINATES.get(row['location_name'], [23.5, 121.0])[0], axis=1)
    df['display_lon'] = df.apply(lambda row: COORDINATES.get(row['location_name'], [23.5, 121.0])[1], axis=1)
    return df

st.title("🌤️ Taiwan Weather Forecast GIS")
st.markdown("Dynamic data fetched directly from our SQLite database (Gate 2), sourced from CWA API (Gate 1).")

try:
    df = load_data()
except Exception as e:
    st.error("Could not load data.db. Did you run Gate 1 & 2?")
    st.stop()

# ── Sidebar Filters ──
st.sidebar.header("Filter Settings")
locations = sorted(df['location_name'].unique())
selected_loc = st.sidebar.selectbox("Select Region (地區)", ["All"] + locations)

available_times = sorted(df['forecast_start'].unique())
selected_time = st.sidebar.selectbox("Select Forecast Time (時間)", available_times)

# Filter Data for the Map (current selected time)
map_data = df[df['forecast_start'] == selected_time]
if selected_loc != "All":
    map_data = map_data[map_data['location_name'] == selected_loc]

# ── 3A to 3G: Map Rendering ──
st.subheader(f"Taiwan Weather Map: {selected_time[:16].replace('T', ' ')}")

# Centered slightly left to cover Taiwan better
m = folium.Map(location=[23.7, 121.0], zoom_start=7, tiles="OpenStreetMap")

# Add markers
for idx, row in map_data.iterrows():
    popup_text = f"""
    <div style='width: 150px;'>
        <h4>{row['location_name']}</h4>
        <p><b>Weather:</b> {row['weather']}</p>
        <p><b>Temp:</b> {row['min_temp']}°C ~ {row['max_temp']}°C</p>
        <p><b>PoP:</b> {row['rain_probability'] if pd.notnull(row['rain_probability']) else '-'}%</p>
    </div>
    """
    
    # Custom icon coloring based on temperature
    color = "green"
    if pd.notnull(row['max_temp']):
        if row['max_temp'] >= 32:
            color = "red"
        elif row['max_temp'] >= 28:
            color = "orange"
        elif row['max_temp'] < 20:
            color = "blue"
            
    folium.Marker(
        location=[row['display_lat'], row['display_lon']],
        popup=folium.Popup(popup_text, max_width=200),
        tooltip=row['location_name'],
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# Render map in Streamlit
st_folium(m, width=900, height=600)

# ── Detailed Charts & Tables ──
st.divider()

if selected_loc != "All":
    st.subheader(f"7-Day Forecast for {selected_loc}")
    loc_data = df[df['location_name'] == selected_loc].sort_values('forecast_start')
    
    # Display Chart
    chart_data = loc_data[['forecast_start', 'min_temp', 'max_temp']].set_index('forecast_start')
    # Clean up index for display
    chart_data.index = [str(x)[:16].replace('T', ' ') for x in chart_data.index]
    st.line_chart(chart_data)
    
    # Display Table (hide some columns)
    display_df = loc_data[['forecast_start', 'forecast_end', 'weather', 'min_temp', 'max_temp', 'rain_probability']]
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("Select a specific region from the sidebar to view detailed 7-day charts and tables.")

st.markdown("---")
st.markdown("*(GATE 3 PASS CHECK)*")
