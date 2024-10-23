import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st
import re
import matplotlib.pyplot as plt
from pathlib import Path

# import folium
import gtfs_kit as gk

# Load data
filename_df = "MTA_Bus_Route_Segment_Speeds__Beginning_2023_20241017.csv"
path_df = Path(filename_df)
df = pd.read_csv(path_df, nrows=10000)
sim33c = df[df['Route ID'] == "SIM33C"]

# Function to extract coordinates from POINT string
def extract_coordinates(point_str):
    match = re.search(r'POINT \(([-\d.]+) ([-\d.]+)\)', point_str)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

# Extract coordinates
sim33c['Start_Lon'], sim33c['Start_Lat'] = zip(*sim33c['Timepoint Stop Georeference'].apply(extract_coordinates))
sim33c['End_Lon'], sim33c['End_Lat'] = zip(*sim33c['Next Timepoint Stop Georeference'].apply(extract_coordinates))

# Create a new DataFrame for the line segments
line_data = sim33c[['Start_Lon', 'Start_Lat', 'End_Lon', 'End_Lat']].to_dict('records')

filename = "gtfs/google_transit_staten_island.zip"

@st.cache_data
def load_feed(path):
    feed = gk.read_feed(path, dist_units="km")
    return feed


@st.cache_data
def get_trip_stats(_feed):
    return _feed.compute_trip_stats()

path = Path(filename)
feed = load_feed(path)


# Streamlit app
st.title('MTA Bus Route SIM33C Visualization')



# # Create a map
# st.pydeck_chart(pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=pdk.ViewState(
#         latitude=sim33c['Start_Lat'].mean(),
#         longitude=sim33c['Start_Lon'].mean(),
#         zoom=11,
#         pitch=50,
#     ),
#     layers=[
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=sim33c,
#             get_position=['Start_Lon', 'Start_Lat'],
#             get_color=[0, 255, 0, 160],  # Green for initial points
#             get_radius=50,
#             pickable=True,
#             auto_highlight=True,
#         ),
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=sim33c,
#             get_position=['End_Lon', 'End_Lat'],
#             get_color=[255, 0, 0, 160],  # Red for end points
#             get_radius=50,
#             pickable=True,
#             auto_highlight=True,
#         ),
#         pdk.Layer(
#             'LineLayer',
#             data=line_data,
#             get_source_position=['Start_Lon', 'Start_Lat'],
#             get_target_position=['End_Lon', 'End_Lat'],
#             get_color=[0, 0, 255, 80],  # Blue for lines
#             get_width=2,
#             pickable=True,
#             auto_highlight=True,
#         ),
#     ],
#     tooltip={
#         'html': '<b>Initial Stop:</b> {Timepoint Stop Name}<br/>'
#                 '<b>Next Stop:</b> {Next Timepoint Stop Name}<br/>'
#                 '<b>Speed:</b> {Speed} mph',
#         'style': {
#             'backgroundColor': 'steelblue',
#             'color': 'white'
#         }
#     }
# ))

# # Display the data
# st.subheader('SIM33C Route Data')
# st.write(sim33c)

# # Add some statistics
# st.subheader('Route Statistics')
# st.write(f"Average Speed: {sim33c['Average Road Speed'].mean():.2f} mph")
# st.write(f"Total Segments: {len(sim33c)}")

# # Optional: Add a histogram of speeds
# st.subheader('Speed Distribution')
# fig, ax = plt.subplots()
# sim33c['Average Road Speed'].hist(bins=20, ax=ax)
# ax.set_xlabel('Average Road Speed (mph)')
# ax.set_ylabel('Frequency')
# st.pyplot(fig)