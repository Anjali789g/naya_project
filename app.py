import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Data Analyst Portfolio Project", layout="wide")

st.title("📊 E-Commerce Sales & Insights Dashboard")
st.markdown("An interactive dashboard analyzing sales performance, regional trends, and profitability.")

# 1. Load Data (Using a sample dataset or upload your CSV)
@st.cache_data
def load_data():
    # You can replace this with your own cleaned CSV file
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/raw/tips.csv"
    return pd.read_csv(url)

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
selected_day = st.sidebar.multiselect("Select Day", options=df['day'].unique(), default=df['day'].unique())

filtered_df = df[df['day'].isin(selected_day)]

# KPI Metrics
total_sales = filtered_df['total_bill'].sum()
avg_tip = filtered_df['tip'].mean()

col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Average Tip/Order", f"${avg_tip:,.2f}")

st.divider()

# Visualizations
st.subheader("Visual Breakdown")
fig = px.bar(filtered_df, x="day", y="total_bill", color="sex", barmode="group", title="Total Sales by Day and Gender")
st.plotly_chart(fig, use_container_width=True)

# Show raw data option
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)