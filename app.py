import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st
import re
import matplotlib.pyplot as plt
from pathlib import Path


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


# Streamlit app
st.title('MTA Bus Route SIM33C Visualization')


