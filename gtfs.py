import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os

class TransitViewer:
    def __init__(self, gtfs_directory):
        """Initialize with the directory path containing GTFS files"""
        self.gtfs_directory = gtfs_directory
        self.data = {}
        self.load_files()
    
    def load_files(self):
        """Load all GTFS files from the specified directory"""
        files_to_load = {
            'agency': 'agency.txt',
            'calendar': 'calendar.txt',
            'routes': 'routes.txt',
            'shapes': 'shapes.txt',
            'stops': 'stops.txt',
            'stop_times': 'stop_times.txt',
            'trips': 'trips.txt'
        }
        
        for key, filename in files_to_load.items():
            file_path = os.path.join(self.gtfs_directory, filename)
            try:
                self.data[key] = pd.read_csv(file_path)
                print(f"✓ Loaded {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    def create_route_map(self, selected_route=None):
        """Create a map showing routes and stops"""
        if 'stops' not in self.data or 'shapes' not in self.data:
            st.error("Missing required files: stops.txt or shapes.txt")
            return
        
        # Create base map
        center_lat = self.data['stops']['stop_lat'].mean()
        center_lon = self.data['stops']['stop_lon'].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        if selected_route:
            # Get shapes for selected route
            route_trips = self.data['trips'][self.data['trips']['route_id'] == selected_route]
            route_shapes = self.data['shapes'][self.data['shapes']['shape_id'].isin(route_trips['shape_id'])]
            
            # Draw route lines
            for shape_id in route_shapes['shape_id'].unique():
                shape_points = route_shapes[route_shapes['shape_id'] == shape_id].sort_values('shape_pt_sequence')
                points = [[row['shape_pt_lat'], row['shape_pt_lon']] for _, row in shape_points.iterrows()]
                folium.PolyLine(points, color='blue', weight=2, opacity=0.8).add_to(m)
            
            # Get stops for this route
            route_stop_times = self.data['stop_times'][self.data['stop_times']['trip_id'].isin(route_trips['trip_id'])]
            route_stops = self.data['stops'][self.data['stops']['stop_id'].isin(route_stop_times['stop_id'])]
        else:
            route_stops = self.data['stops']
        
        # Add stop markers
        for _, stop in route_stops.iterrows():
            folium.CircleMarker(
                [stop['stop_lat'], stop['stop_lon']],
                radius=5,
                color='red',
                fill=True,
                popup=stop['stop_name']
            ).add_to(m)
        
        return m
    
    def get_route_schedule(self, route_id, selected_date=None):
        """Get schedule for a specific route"""
        if not all(key in self.data for key in ['trips', 'stop_times', 'stops', 'calendar']):
            st.error("Missing required files for schedule display")
            return None
        
        # Get trips for route
        route_trips = self.data['trips'][self.data['trips']['route_id'] == route_id]
        
        # Get stop times for these trips
        schedule = pd.merge(
            route_trips[['trip_id', 'service_id']],
            self.data['stop_times'],
            on='trip_id'
        )
        
        # Add stop information
        schedule = pd.merge(
            schedule,
            self.data['stops'][['stop_id', 'stop_name']],
            on='stop_id'
        )
        
        # Filter by date if provided
        if selected_date:
            day_name = selected_date.strftime('%A').lower()
            valid_services = self.data['calendar'][self.data['calendar'][day_name] == 1]['service_id']
            schedule = schedule[schedule['service_id'].isin(valid_services)]
        
        return schedule.sort_values(['trip_id', 'stop_sequence'])

    def get_route_info(self, route_id):
        """Get detailed information about a specific route"""
        if 'routes' not in self.data:
            return None
            
        route_info = self.data['routes'][self.data['routes']['route_id'] == route_id].iloc[0]
        trips_count = len(self.data['trips'][self.data['trips']['route_id'] == route_id])
        
        # Get unique stops for this route
        route_trips = self.data['trips'][self.data['trips']['route_id'] == route_id]
        route_stops = self.data['stop_times'][self.data['stop_times']['trip_id'].isin(route_trips['trip_id'])]
        unique_stops = len(route_stops['stop_id'].unique())
        
        return {
            'route_info': route_info,
            'trips_count': trips_count,
            'stops_count': unique_stops
        }

def main():
    st.title("Transit System Explorer")
    
    # Define your GTFS directory path here
    DIRS = {"Staten Island": "./google_transit_staten_island",
            "Brooklyn": "./google_transit_brooklyn",
            "Queens": "./google_transit_queens",
            "Bronx": "./google_transit_bronx",
            "Manhattan": "./google_transit_manhattan",
            "Trains": "google_transit",
            "All":          
            } #should make these into useable CSV's, just for my own usage. This is annoying
    GTFS_DIR = st.selectbox(
            "Select Borough",
            options=DIRS.values()
    )
    

    viewer = TransitViewer(GTFS_DIR)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Route Map", "Schedule", "System Info"])
    
    with tab1:
        st.header("Route Map")
        if 'routes' in viewer.data:
            route_options = viewer.data['routes']['route_id'].unique()
            selected_route = st.selectbox(
                "Select Route",
                options=route_options,
                format_func=lambda x: f"{x}"
            )
            
            if selected_route:
                route_info = viewer.get_route_info(selected_route)
                if route_info:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Trips", route_info['trips_count'])
                    with col2:
                        st.metric("Stops", route_info['stops_count'])
                
            map_obj = viewer.create_route_map(selected_route)
            if map_obj:
                st_folium(map_obj)
    
    with tab2:
        st.header("Route Schedule")
        if 'routes' in viewer.data:
            route_id = st.selectbox(
                "Select Route",
                options=viewer.data['routes']['route_id'].unique(),
                format_func=lambda x: f"Route {x}",
                key="schedule_route"
            )
            date = st.date_input("Select Date", datetime.now())
            
            schedule = viewer.get_route_schedule(route_id, date)
            if schedule is not None:
                st.dataframe(
                    schedule[[
                        'trip_id', 'stop_name', 'arrival_time', 
                        'departure_time', 'stop_sequence'
                    ]]
                )
    
    with tab3:
        st.header("System Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'routes' in viewer.data:
                st.metric("Total Routes", len(viewer.data['routes']))
        
        with col2:
            if 'stops' in viewer.data:
                st.metric("Total Stops", len(viewer.data['stops']))
        
        with col3:
            if 'trips' in viewer.data:
                st.metric("Total Trips", len(viewer.data['trips']))
        
        if 'agency' in viewer.data:
            st.subheader("Agency Details")
            st.dataframe(viewer.data['agency'])

if __name__ == "__main__":
    main()