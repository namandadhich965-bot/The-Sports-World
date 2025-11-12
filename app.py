import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------
# App Title and Description
# -------------------------------
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("🛍️ Retail Sales Dashboard")
st.write("Analyze retail sales data with interactive filters and insights using **Pandas**, **NumPy**, and **Streamlit**.")

# -------------------------------
# Upload CSV
# -------------------------------
st.sidebar.header("📂 Upload Your Sales Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # -------------------------------
    # Basic Data Cleaning
    # -------------------------------
    df.columns = df.columns.str.strip()  # remove extra spaces
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Check if necessary columns exist
    required_cols = ['Date', 'Product', 'Quantity', 'Price']
    if all(col in df.columns for col in required_cols):
        
        # Ensure numeric columns
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

        # Calculate Total Sales
        df['Total_Sales'] = df['Quantity'] * df['Price']

        # -------------------------------
        # Filters
        # -------------------------------
        st.sidebar.subheader("🔍 Filter Options")

        products = st.sidebar.multiselect("Select Products", df['Product'].unique())
        if products:
            df = df[df['Product'].isin(products)]

        # Date Range Filter
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        min_date, max_date = df['Date'].min(), df['Date'].max()
        date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        # -------------------------------
        # KPI Metrics
        # -------------------------------
        total_sales = df['Total_Sales'].sum()
        avg_sale = df['Total_Sales'].mean()
        total_quantity = df['Quantity'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Sales", f"₹{total_sales:,.2f}")
        col2.metric("📦 Total Quantity Sold", f"{total_quantity:,.0f}")
        col3.metric("📊 Average Sale per Order", f"₹{avg_sale:,.2f}")

        # -------------------------------
        # Sales by Product
        # -------------------------------
        st.subheader("🏷️ Sales by Product")
        sales_by_product = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
        st.bar_chart(sales_by_product)

        # -------------------------------
        # Daily Sales Trend
        # -------------------------------
        st.subheader("📅 Daily Sales Trend")
        sales_trend = df.groupby('Date')['Total_Sales'].sum()
        st.line_chart(sales_trend)

    else:
        st.warning("⚠️ CSV must include columns: Date, Product, Quantity, and Price")
else:
    st.info("⬆️ Please upload a CSV file to start.")
