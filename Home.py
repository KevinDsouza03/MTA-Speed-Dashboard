# Home.py (Speed Analysis as main page)
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import create_data_controls


@st.cache_data
def create_speed_time_scatter(route_df, switch):
    if route_df.empty:
        return None, None
        
    #Calculate mean speed for each hour and route
    grouping = "Month" if switch else "Hour of Day"
    hourly_means = route_df.groupby(['Route ID', grouping])['Average Road Speed'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for route_id in route_df['Route ID'].unique():
        #Creating scatter plot
        grouped = hourly_means[hourly_means['Route ID'] == route_id]
        ax.scatter(grouped[grouping], grouped['Average Road Speed'], 
                  s=100, alpha=0.7, label=f'Route {route_id}')
        ax.plot(grouped[grouping], grouped['Average Road Speed'], 
                alpha=0.4, linestyle='--')
                
        #Labels for each point
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
    
    #Set x-axis ticks
    if switch:
        ax.set_xticks(range(int(route_df[grouping].min()), int(route_df[grouping].max())+1))
    else:
        ax.set_xticks(range(0, 24))
    
    # Set y-axis limits with extra padding to accommodate labels
    ax.set_ylim(bottom=0, top=route_df['Average Road Speed'].max() * 1.2)
    
    ax.legend()
    plt.tight_layout()
    
    return fig, hourly_means

def main():
    st.title('MTA Bus Speed Analysis')
    
    #Function to render data across pages
    df = create_data_controls()
    
    route_selection = st.multiselect(
        "Select Route(s)", 
        options=sorted(df['Route ID'].unique()), 
        default=[]
    )
    
    route_df = df[df['Route ID'].isin(route_selection)]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        switch = st.toggle("View by Month", value=False)
    
    with col2:
        if route_selection:
            st.metric("Selected Routes", len(route_selection))
            st.metric("Total Data Points", len(route_df))
    
    if route_selection:
        fig, hourly_means = create_speed_time_scatter(route_df, switch)
        if fig:
            st.pyplot(fig)
            
            with st.expander("View Dataframe"):
                st.dataframe(
                    hourly_means.style.format({
                        'Average Road Speed': '{:.2f}'
                    })
                )
    else:
        st.warning("Please select at least one route to visualize data.")

if __name__ == "__main__":
    main()