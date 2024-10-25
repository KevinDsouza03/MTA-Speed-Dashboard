import streamlit as st
from utils.data_loader import create_data_controls


def main():
    st.title('Route Frequency Analysis')
    
    df = create_data_controls()
    

if __name__ == "__main__":
    main()