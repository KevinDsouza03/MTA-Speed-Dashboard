import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set the path to your CSV file here
csv_path = "path/to/your/file.csv"

# Load the data
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(csv_path)

# Title
st.title("Enhanced Data Visualization App")

# Display the first few rows of the dataset
st.subheader("Data Preview")
st.write(df.head())

# Display basic statistics
st.subheader("Basic Statistics")
st.write(df.describe())

# Sidebar for chart selection
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["Histogram", "Scatter Plot", "Line Plot", "Bar Chart", "Box Plot", "Violin Plot", "Pair Plot", "Correlation Heatmap", "3D Scatter Plot"]
)

# Function to get numeric columns
def get_numeric_columns(df):
    return df.select_dtypes(include=['float64', 'int64']).columns

# Function to get categorical columns
def get_categorical_columns(df):
    return df.select_dtypes(include=['object', 'category']).columns

if chart_type == "Histogram":
    st.subheader("Histogram")
    column = st.selectbox("Select a column for histogram", get_numeric_columns(df))
    fig = px.histogram(df, x=column)
    st.plotly_chart(fig)

elif chart_type == "Scatter Plot":
    st.subheader("Scatter Plot")
    x_column = st.selectbox("Select X-axis", get_numeric_columns(df))
    y_column = st.selectbox("Select Y-axis", get_numeric_columns(df))
    fig = px.scatter(df, x=x_column, y=y_column)
    st.plotly_chart(fig)

elif chart_type == "Line Plot":
    st.subheader("Line Plot")
    x_column = st.selectbox("Select X-axis", df.columns)
    y_column = st.selectbox("Select Y-axis", get_numeric_columns(df))
    fig = px.line(df, x=x_column, y=y_column)
    st.plotly_chart(fig)

elif chart_type == "Bar Chart":
    st.subheader("Bar Chart")
    x_column = st.selectbox("Select X-axis", get_categorical_columns(df))
    y_column = st.selectbox("Select Y-axis", get_numeric_columns(df))
    fig = px.bar(df, x=x_column, y=y_column)
    st.plotly_chart(fig)

elif chart_type == "Box Plot":
    st.subheader("Box Plot")
    x_column = st.selectbox("Select X-axis (categorical)", get_categorical_columns(df))
    y_column = st.selectbox("Select Y-axis (numerical)", get_numeric_columns(df))
    fig = px.box(df, x=x_column, y=y_column)
    st.plotly_chart(fig)

elif chart_type == "Violin Plot":
    st.subheader("Violin Plot")
    x_column = st.selectbox("Select X-axis (categorical)", get_categorical_columns(df))
    y_column = st.selectbox("Select Y-axis (numerical)", get_numeric_columns(df))
    fig = px.violin(df, x=x_column, y=y_column)
    st.plotly_chart(fig)

elif chart_type == "Pair Plot":
    st.subheader("Pair Plot")
    columns = st.multiselect("Select columns for pair plot", get_numeric_columns(df), default=get_numeric_columns(df)[:3])
    if len(columns) < 2:
        st.warning("Please select at least two columns for the pair plot.")
    else:
        fig = sns.pairplot(df[columns])
        st.pyplot(fig)

elif chart_type == "Correlation Heatmap":
    st.subheader("Correlation Heatmap")
    corr = df.select_dtypes(include=['float64', 'int64']).corr()
    fig = px.imshow(corr, color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
    st.plotly_chart(fig)

elif chart_type == "3D Scatter Plot":
    st.subheader("3D Scatter Plot")
    x_column = st.selectbox("Select X-axis", get_numeric_columns(df))
    y_column = st.selectbox("Select Y-axis", get_numeric_columns(df))
    z_column = st.selectbox("Select Z-axis", get_numeric_columns(df))
    fig = px.scatter_3d(df, x=x_column, y=y_column, z=z_column)
    st.plotly_chart(fig)