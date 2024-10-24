import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


def create_frequency_graph(route_df):
    #TODO
    df = pd.DataFrame(route_df)

    df['']


    return None
def create_speed_time_scatter(route_df,switch):
    # Calculate mean speed for each hour
    grouping = None
    if switch:
        grouping = "Month"
        hourly_means = route_df.groupby('Month')['Average Road Speed'].mean().reset_index()
    else:
        grouping = "Hour of Day"
        hourly_means = route_df.groupby('Hour of Day')['Average Road Speed'].mean().reset_index()
    
    # Create figure and axis objects with a single subplot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create the scatter plot with mean values
    ax.scatter(hourly_means[grouping], hourly_means['Average Road Speed'], 
              s=100, alpha=0.7, color='#2E86C1', label='Hourly Mean')
    
    # Add connecting lines to show trend
    ax.plot(hourly_means[grouping], hourly_means['Average Road Speed'], 
           alpha=0.4, color='#2E86C1', linestyle='--')
    
    ax.set_title(f'Average Road Speed by {grouping} ({grouping} Means)', fontsize=14, pad=15)
    ax.set_xlabel(grouping, fontsize=12)
    ax.set_ylabel('Average Road Speed', fontsize=12)
    
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Set x-axis ticks to show all hours
    ax.set_xticks(range(0, 24))

    #labels    
    for x, y in zip(hourly_means[grouping], hourly_means['Average Road Speed']):
        ax.annotate(f'{y:.1f}', 
                   (x, y), 
                   textcoords="offset points", 
                   xytext=(0,10), 
                   ha='center')
    
    # Set y-axis to start from 0
    ax.set_ylim(bottom=0)
    
    # Add legend
    ax.legend()
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return fig, hourly_means

@st.cache_data
def load_data(nrows):
    filename_df = "Speeds.csv"
    path_df = Path(filename_df)

    data = pd.read_csv(
        path_df,
        nrows= nrows,#10000 currently but, i wanna vary this
    )

    return data
#So ive displayed the average speed per hour of day according to route. Generalize to month, fastest months
#now i would want to show frequency of buses, so how often are we actually getting a bus at a stop and how far off from the scheduled time. Maybe a table?
#
def main():
# Load data
    df_len = 9495123
    nrows = st.slider(
        "Select number of rows to load", 
        min_value=100, 
        max_value=df_len, 
        value=10000,  # Default value
        step=50000
    )
    df = load_data(nrows)

    # Create a new DataFrame for the line segments

    # Streamlit app
    st.title('MTA Bus Route Visualization')

    #First, ill just make a table depending on user Bus Route Selection and display insights.

    route = st.selectbox(
        "Select Route",
        options = df['Route ID'].unique()   
        )

    mask = df['Route ID'] == route
    route_df = df[mask]

    #speed against timestmap
    #So can group by the hours of hte day, 1-24 then take the mean of that Average Road Speed w that. And then keep scalng that up to per month.
    switch = st.toggle("View by Month", value=False)

    fig, hourly = create_speed_time_scatter(route_df,switch)
    st.pyplot(fig)
    st.table(hourly)
if __name__ == "__main__":
    main()
