import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import create_data_controls

def get_route_presets(df):
# Make presets for the bar chart since this needs a lot of buses
    return {
        "Staten Island": list(df[df['Borough'] == 'Staten Island']['Route ID'].unique()),
        "Brooklyn": list(df[df['Borough'] == 'Brooklyn']['Route ID'].unique()),
        "Bronx": list(df[df['Borough'] == 'Bronx']['Route ID'].unique()), 
        "Queens": list(df[df['Borough'] == 'Queens']['Route ID'].unique()),
        "Manhattan": list(df[df['Borough'] == 'Manhattan']['Route ID'].unique()),
        "Other": list(df[df['Borough'] == 'Other']['Route ID'].unique()),
        "Express": list(df[df['Route Type'] == 'Express']['Route ID'].unique()),
        "Local": list(df[df['Route Type'] == 'Local']['Route ID'].unique()),
        "Limited": list(df[df['Route Type'] == 'Limited']['Route ID'].unique()),
        "SBS": list(df[df['Route Type'] == 'SBS']['Route ID'].unique()),
        "School": list(df[df['Route Type'] == 'School']['Route ID'].unique()),
    }


def create_frequency_chart(route_df):
    # Creates a bar chart showing bus trip counts for each route
    if route_df.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    #Group by Route ID and get max trips
    max_trips = route_df.groupby(['Route ID'])['Bus Trip Count'].max().reset_index()
    
    ax.bar(max_trips['Route ID'], max_trips['Bus Trip Count'])
    
    ax.set_xlabel('Route ID')
    ax.set_ylabel('Maximum Bus Trip Count')
    ax.set_title('Maximum Bus Trips per Route')
    
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    return fig

def main():
    st.title('Route Frequency Analysis')
    
    df = create_data_controls()
       # Selection method choice
    selection_method = st.radio(
        "Choose selection method:",
        ["Manual Selection", "Use Preset"],
        horizontal=True
    )

    # Get route selection based on method
    if selection_method == "Use Preset":
        presets = get_route_presets(df)
        preset_choice = st.selectbox(
            "Choose a preset",
            options=list(presets.keys())
        )
        route_selection = presets[preset_choice]
        
        # Show which routes are included in preset
        st.write("Routes included in this preset:", ", ".join(route_selection))
    else:
        # Original manual selection
        route_selection = st.multiselect(
            "Select Route(s)", 
            options=sorted(df['Route ID'].unique()), 
            default=[]
        )
    
    
    if route_selection:
        route_df = df[df['Route ID'].isin(route_selection)]
        
        fig = create_frequency_chart(route_df)
        if fig is not None:
            st.pyplot(fig)
    else:
        st.warning("Please select at least one route to visualize data.")


if __name__ == "__main__":
    main()