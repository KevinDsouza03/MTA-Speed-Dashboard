import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st
import re
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("MTA_Bus_Route_Segment_Speeds__Beginning_2023_20241015.csv", nrows=10000)
sim33c = df[df['Route ID'] == "SIM33C"]

def parse_wkt_point(wkt_point):
    coords = re.findall(r'-?\d+\.\d+', wkt_point)
    return float(coords[1]), float(coords[0])  # lat, lon

# Parse coordinates
sim33c['Initial lat'], sim33c['Initial lon'] = zip(*sim33c['Timepoint Stop Georeference'].apply(parse_wkt_point))
sim33c['End lat'], sim33c['End lon'] = zip(*sim33c['Next Timepoint Stop Georeference'].apply(parse_wkt_point))

# Create a new DataFrame for the line segments
line_data = sim33c[['Initial lon', 'Initial lat', 'End lon', 'End lat']].to_dict('records')

# Streamlit app
st.title('MTA Bus Route SIM33C Visualization')

# Create a map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=sim33c['Initial lat'].mean(),
        longitude=sim33c['Initial lon'].mean(),
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=sim33c,
            get_position='[Initial lon, Initial lat]',
            get_color=[0, 255, 0, 160],  # Green for initial points
            get_radius=50,
            pickable=True,
            auto_highlight=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=sim33c,
            get_position='[End lon, End lat]',
            get_color=[255, 0, 0, 160],  # Red for end points
            get_radius=50,
            pickable=True,
            auto_highlight=True,
        ),
        pdk.Layer(
            'LineLayer',
            data=line_data,
            get_source_position='[Initial lon, Initial lat]',
            get_target_position='[End lon, End lat]',
            get_color=[0, 0, 255, 80],  # Blue for lines
            get_width=2,
            pickable=True,
            auto_highlight=True,
        ),
    ],
    tooltip={
        'html': '<b>Initial Stop:</b> {Timepoint Stop Name}<br/>'
                '<b>Next Stop:</b> {Next Timepoint Stop Name}<br/>'
                '<b>Speed:</b> {Speed} mph',
        'style': {
            'backgroundColor': 'steelblue',
            'color': 'white'
        }
    }
))

# Display the data
st.subheader('SIM33C Route Data')
st.write(sim33c)

# Add some statistics
st.subheader('Route Statistics')
st.write(f"Average Speed: {sim33c['Average Road Speed'].mean():.2f} mph")
st.write(f"Total Segments: {len(sim33c)}")

# Optional: Add a histogram of speeds
st.subheader('Speed Distribution')
fig, ax = plt.subplots()
sim33c['Average Road Speed'].hist(bins=20, ax=ax)
ax.set_xlabel('Average Road Speed (mph)')
ax.set_ylabel('Frequency')
st.pyplot(fig)