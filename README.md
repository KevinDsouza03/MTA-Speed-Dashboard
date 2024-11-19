# MTA Speed Dashboard

A dynamic Streamlit application for visualizing MTA bus speeds and total number of trips per bus in New York City. Created for the MTAOpenData contest.

## 🚌 Overview

MTA Speed Dashboard provides an interactive interface to analyze and visualize:
- Speed Analysis
- Route Frequency Analysis

## 🌐 Live Demo

Try out the [Dashboard](https://mta-speed-dashboard.streamlit.app/)


## 🎯 Features

### Speed Analysis
- How fast are the buses I take?
- Hourly speed patterns between selected timepoints
- Monthly speed trend visualization
- Comparative speed analysis across routes

### Route Frequency Analysis
- How much does a bus run?
- Borough-specific presets
- Route type filtering (Local, Express, Select Bus Service)
- Custom route selection

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/KevinDsouza03/MTA-Speed-Dashboard.git

# Navigate to the project directory
cd MTA-Speed-Dashboard

# Install required packages
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## 📦 Dependencies

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- Seaborn
- NumPy
- Dataset (It will be automatically downloaded if ran locally, but will depend on your internet speed.)

## 🚀 Usage

1. Launch the application using `streamlit run Home.py`
2. Select a borough or specific route from the sidebar
3. Choose your desired time period for analysis
4. Interact with the visualizations to explore speed and frequency patterns
5. Change in utils/data_loader.py line 13 if running locally to the length of the data. Streamlit tends to crash if its too much.

## 📊 Data Sources

- [MTA Bus Route Segment Speeds (Beginning 2023)](https://data.ny.gov/Transportation/MTA-Bus-Route-Segment-Speeds-Beginning-2023/58t6-89vi/about_data)

## 🏆 MTAOpenData Contest

This project was created as part of the MTAOpenData contest!
