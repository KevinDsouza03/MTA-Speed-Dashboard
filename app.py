import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# """
# TODO:
#     - Make this deployable by tomorrow. How to? lets see
#     - Frequency table stuff maybe


# """
def create_frequency_graph(route_df):
    df = pd.DataFrame(route_df)

    df['']


    return None
@st.cache_data
def create_speed_time_scatter(route_df, switch):
    if route_df.empty:
        return None, None
        
    # Calculate mean speed for each hour and route
    grouping = "Month" if switch else "Hour of Day"
    hourly_means = route_df.groupby(['Route ID', grouping])['Average Road Speed'].mean().reset_index()
    
    # Create figure and axis objects with a single subplot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for route_id in route_df['Route ID'].unique():
        # Creating scatter plot
        grouped = hourly_means[hourly_means['Route ID'] == route_id]
        ax.scatter(grouped[grouping], grouped['Average Road Speed'], 
                  s=100, alpha=0.7, label=f'Route {route_id}')
        ax.plot(grouped[grouping], grouped['Average Road Speed'], 
                alpha=0.4, linestyle='--')
                
        # Labels for each point. 
        for idx, row in grouped.iterrows():
            ax.annotate(f'{row["Average Road Speed"]:.1f}', 
                       (row[grouping], row['Average Road Speed']),
                       xytext=(0, 10),  
                       textcoords='offset points',
                       ha='center', 
                       va='bottom',  
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.5', 
                               fc='white', 
                               ec='gray',
                               alpha=0.7))
    
    ax.set_title(f'Average Road Speed by {grouping} ({grouping} Means)', fontsize=14, pad=15)
    ax.set_xlabel(grouping, fontsize=12)
    ax.set_ylabel('Average Road Speed', fontsize=12)
    
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Set x-axis ticks
    if switch:
        ax.set_xticks(range(int(route_df[grouping].min()), int(route_df[grouping].max())+1))
    else:
        ax.set_xticks(range(0, 24))
    
    # Set y-axis limits with extra padding to accommodate labels
    ax.set_ylim(bottom=0, top=route_df['Average Road Speed'].max() * 1.2)  # Increased padding to 20%
    
    ax.legend()
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

def main():
# Load data
    st.title('MTA Bus Route Visualization')
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

    #First, ill just make a table depending on user Bus Route Selection and display insights.
    

    route_selection = st.multiselect("Select Route(s)", options=df['Route ID'].unique(), default=[])
    route_df = df[df['Route ID'].isin(route_selection)]


    #speed against timestmap
    #So can group by the hours of hte day, 1-24 then take the mean of that Average Road Speed w that. And then keep scalng that up to per month.
    switch = st.toggle("View by Month", value=False)
    if route_selection:
        fig, hourly = create_speed_time_scatter(route_df, switch)
        st.pyplot(fig)
        st.table(hourly)
    else:
        st.warning("Please select at least one route.")
if __name__ == "__main__":
    main()
