import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="GrowEasy Analytics", layout="wide")

st.title("🛒 GrowEasy Analytics Dashboard")
st.markdown("Transforming supermarket sales data into actionable customer insights.")

# Sidebar - Upload CSV
st.sidebar.header("Upload Your Data (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Default dataset path
default_data_path = "df_scaled.csv"

# Load default dataset
try:
    df = pd.read_csv(default_data_path)
    source = "Default dataset"
except Exception as e:
    st.error("Default dataset not found. Please upload a CSV file.")
    st.stop()

# If user uploads a file, use that instead
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    source = "Uploaded file"

st.subheader(f"Data Preview ({source})")
st.dataframe(df.head())

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

if len(numeric_cols) >= 2:
    st.sidebar.subheader("Clustering Options")
    n_clusters = st.sidebar.slider("Number of Customer Segments", 2, 10, 4)

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[numeric_cols])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df_scaled)

    st.subheader("Customer Segmentation Overview")
    st.write("Customer clusters based on selected numerical features.")

    fig, ax = plt.subplots()
    sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]], hue=df['Cluster'], palette="tab10", ax=ax)
    plt.title("Customer Segments")
    st.pyplot(fig)

    st.subheader("Cluster Distribution")
    cluster_counts = df['Cluster'].value_counts().sort_index()
    st.bar_chart(cluster_counts)

    st.subheader("Download Clustered Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV with Clusters", data=csv, file_name="segmented_customers.csv", mime='text/csv')
else:
    st.warning("Dataset must contain at least two numeric columns for clustering.")

st.markdown("---")
st.caption("Built by Team Statstorm | NBQSA 2025")
