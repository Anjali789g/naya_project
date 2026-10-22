import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Setup
st.set_page_config(page_title="E-Commerce Sales Dashboard", page_icon="🛍️", layout="wide")

st.title("🛍️ E-Commerce Sales & Business Insights Dashboard")
st.markdown("An interactive analytics dashboard tracking sales performance, profitability, product category trends, and regional breakdown.")

# Load Data locally (Generates offline dataset automatically - no internet needed!)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
    n_rows = 1500
    
    data = {
        'order_id': [f"ORD-2023-{i:04d}" for i in range(1, n_rows + 1)],
        'order_date': np.random.choice(dates, size=n_rows),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=n_rows),
        'category': np.random.choice(['Furniture', 'Office Supplies', 'Technology'], size=n_rows),
        'sub_category': np.random.choice(['Chairs', 'Binders', 'Phones', 'Storage', 'Tables', 'Art'], size=n_rows),
        'sales': np.random.uniform(50, 2000, size=n_rows).round(2),
        'profit': np.random.uniform(-100, 500, size=n_rows).round(2)
    }
    
    df = pd.DataFrame(data)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Analytics")

region_filter = st.sidebar.multiselect(
    "Select Region:",
    options=df['region'].unique(),
    default=df['region'].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Product Category:",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Apply Filters
filtered_df = df[
    (df['region'].isin(region_filter)) & 
    (df['category'].isin(category_filter))
]

# KPI Metrics Row
col1, col2, col3, col4 = st.columns(4)
total_sales = filtered_df['sales'].sum() if not filtered_df.empty else 0
total_profit = filtered_df['profit'].sum() if not filtered_df.empty else 0
total_orders = filtered_df['order_id'].nunique() if not filtered_df.empty else 0
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

# Interactive Charts - Row 1
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Revenue Trend Over Time")
    monthly_sales = filtered_df.set_index('order_date').resample('ME')['sales'].sum().reset_index()
    fig_line = px.line(
        monthly_sales, 
        x='order_date', 
        y='sales', 
        title="Monthly Sales Growth",
        labels={'order_date': 'Order Date', 'sales': 'Total Sales ($)'}
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.subheader("📦 Sales & Profit by Category")
    cat_summary = filtered_df.groupby('category')[['sales', 'profit']].sum().reset_index()
    fig_bar = px.bar(
        cat_summary, 
        x='category', 
        y=['sales', 'profit'], 
        barmode='group',
        title="Category Revenue vs Profitability",
        labels={'value': 'Amount ($)', 'category': 'Category'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Interactive Charts - Row 2
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("🌍 Sales Distribution by Region")
    region_sales = filtered_df.groupby('region')['sales'].sum().reset_index()
    fig_pie = px.pie(
        region_sales, 
        values='sales', 
        names='region', 
        title="Revenue share by Region",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart4:
    st.subheader("🏆 Top Sub-Categories by Sales")
    top_subcats = filtered_df.groupby('sub_category')['sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_sub = px.bar(
        top_subcats, 
        x='sales', 
        y='sub_category', 
        orientation='h', 
        color='sales',
        title="Top Performing Sub-Categories",
        color_continuous_scale="Blues"
    )
    fig_sub.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_sub, use_container_width=True)

# Data Explorer Table
st.divider()
st.subheader("🔍 Explore Raw Sales Data")
if st.checkbox("Show Data Sample"):
    st.dataframe(filtered_df[['order_id', 'order_date', 'region', 'category', 'sub_category', 'sales', 'profit']].head(100))