import streamlit as st
import pandas as pd
import urllib.request
from pathlib import Path
import time

def create_data_controls(): #Allows user to add/remove more rows from the df for all pages
    with st.sidebar:
        st.header("Data Loading Options")
        nrows = st.slider(
            "Number of rows to analyze", 
            min_value=100, 
            max_value=9495123, 
            value=st.session_state.get('nrows', 10000),
            step=50000
        )
        
        df = load_if_needed(nrows)
        
        st.info(f"Analyzing {len(df):,} rows of data")

        #Manual refresh. Kinda works?        
        if st.button("🔄 Reload Data"):
            st.session_state.data = None
            df = load_if_needed(nrows)
            st.success("Data reloaded successfully!")
        
        return df

@st.cache_data(show_spinner=False)
def load_data(nrows): 
    filename = 'Speeds.csv'
    path = Path(filename)

    message = st.empty()
    if path.exists():
        message.success(f"{filename} has been successfully found.")
    else:
        with st.spinner(f"Downloading {filename}..."):
            urllib.request.urlretrieve(
                r"https://data.ny.gov/api/views/58t6-89vi/rows.csv?fourfour=58t6-89vi&cacheBust=1728072129&date=20241024&accessType=DOWNLOAD&sorting=true",
                filename,
            )
        message.success(f"{filename} has been downloaded!")

    time.sleep(3)
    message.empty()
    data = pd.read_csv(
        path,
        nrows = nrows,
    )
    return data

def get_data(): #Gets data WITHOUT reloading, so we dont have to recalc very long
    return st.session_state.get('data', None)

#Helper for redoing nrows recalc
def load_if_needed(nrows=None):
    if nrows is not None:
        st.session_state.nrows = nrows
        
    if (st.session_state.get('data') is None or 
        len(st.session_state.data) != st.session_state.nrows):
        st.session_state.data = load_data(st.session_state.nrows)
    
    return st.session_state.data
