import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="GrowEasy Insights", layout="wide")

# Load dataset
st.sidebar.header("📁 Upload Your Data (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
default_data_path = "df_GrowEasyAnalytics.csv"

try:
    df = pd.read_csv(default_data_path)
except:
    st.error("Dataset not found. Please upload a file.")
    st.stop()

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)


# --- Cluster Recommendations ---
RECOMMENDATIONS = {
    "Elite Spenders": [
        "💎 Push premium collections and exclusive early access",
        "🎁 Introduce tiered loyalty perks",
        "🤝 Collaborate with luxury influencers"
    ],
    "Balance Buyers": [
        "🎯 Roll out loyalty programs with redeemable points",
        "📬 Personalize offers using frequent purchase data",
        "🛍 Highlight mixed-cart bundle deals"
    ],
    "Fresh Fanatics": [
        "🥬 Promote a farm-to-shelf freshness guarantee",
        "👨‍🍳 Use fitness influencers and recipe content",
        "🚚 Offer same-day delivery on fresh produce"
    ],
    "Value Seekers": [
        "🧮 Highlight combo deals and weekly discounts",
        "🪙 Launch price-match guarantees",
        "📲 Send flash-sale alerts via WhatsApp"
    ],
    "Dry Good Dependents": [
        "📦 Push bulk purchase discounts",
        "🔔 Enable refill reminders via app",
        "📋 Create dry-goods bundles for monthly stock-ups"
    ],
    "Occasional Shoppers": [
        "🎟 Offer welcome-back coupons",
        "🛒 Retarget with last-purchased items",
        "📧 Send inactivity-based re-engagement emails"
    ]
}

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Data")
selected_city = st.sidebar.selectbox("Select City", ["All"] + sorted(df["outlet_city"].unique()))
selected_cluster = st.sidebar.selectbox("Select Cluster", ["All"] + sorted(df["cluster_name"].unique()))
strategy_segment = st.sidebar.selectbox("Select Recommendation Segment", ["All"] + sorted(df["cluster_name"].unique()))

# --- Filter Logic ---
filtered_df = df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["outlet_city"] == selected_city]
if selected_cluster != "All":
    filtered_df = filtered_df[filtered_df["cluster_name"] == selected_cluster]

# --- Title ---
st.title("🛍 GrowEasy Sales Dashboard – Customer Segmentation")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- KPI Section ---
st.markdown("### 📌 Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Sales", f"{filtered_df['Total_sales'].sum():,.0f}")

with kpi2:
    st.metric("Avg. Luxury Sales", f"{filtered_df['luxury_sales'].mean():,.2f}")

with kpi3:
    st.metric("Unique Customers", f"{filtered_df['Customer_ID'].nunique()}")

with kpi4:
    most_common_cluster = filtered_df['cluster_name'].mode()[0] if not filtered_df.empty else "-"
    st.metric("Most Common Cluster", most_common_cluster)

# --- Charts Section ---
st.markdown("### 📊 Sales Visualizations")

col1, col2 = st.columns(2)

with col1:
    bar_fig = px.bar(filtered_df.groupby('cluster_name')['Total_sales'].sum().reset_index(),
                     x='cluster_name', y='Total_sales',
                     title='Total Sales by Cluster', color='cluster_name')
    st.plotly_chart(bar_fig, use_container_width=True)

with col2:
    pie_fig = px.pie(filtered_df, names='cluster_name', values='Total_sales',
                     title='Sales Share by Cluster')
    st.plotly_chart(pie_fig, use_container_width=True)

# --- Box Plot for Luxury Sales ---
st.markdown("### 💼 Luxury Sales Distribution by Cluster")
box_fig = px.box(filtered_df, x='cluster_name', y='luxury_sales', color='cluster_name',
                 title='Luxury Sales Distribution')
st.plotly_chart(box_fig, use_container_width=True)

# --- Strategy Section ---
st.markdown("### 🎯 Targeted Marketing Recommendations")

if strategy_segment != "All":
    st.markdown(f"*Segment: {strategy_segment}*")
    for tip in RECOMMENDATIONS[strategy_segment]:
        st.markdown(f"- {tip}")
else:
    for seg, tips in RECOMMENDATIONS.items():
        st.markdown(f"{seg}")
        for tip in tips:
            st.markdown(f"- {tip}")
        st.markdown("---")

# --- Data Preview + Export ---
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False)
st.download_button("📥 Download Filtered Data", data=csv, file_name="groweasy_filtered.csv", mime="text/csv")