import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# (1) Category dropdown
st.write("### (1) Category Selection")
categories = df['Category'].unique()
selected_category = st.selectbox(
    "Select a Category:",
    categories,
    index=0
)

st.write(f"You selected: {selected_category}")

# (2) Sub-Category multi-select
st.write("### (2) Sub-Category Selection")
# Filter subcategories based on selected category
subcategories_in_category = df[df['Category'] == selected_category]['Sub_Category'].unique()
selected_subcategories = st.multiselect(
    f"Select Sub-Categories in {selected_category}:",
    subcategories_in_category,
    default=subcategories_in_category[:2] if len(subcategories_in_category) >= 2 else subcategories_in_category
)

st.write(f"You selected subcategories: {selected_subcategories}")

# (3) Line chart of sales for selected subcategories
st.write("### (3) Sales Over Time for Selected Sub-Categories")
if selected_subcategories:
    # Filter data for selected subcategories
    filtered_df = df[df['Sub_Category'].isin(selected_subcategories)]
    
    # Group by month and subcategory to show sales over time
    sales_by_month_subcategory = filtered_df.groupby([pd.Grouper(freq='M'), 'Sub_Category'])['Sales'].sum().unstack(fill_value=0)
    
    st.line_chart(sales_by_month_subcategory)
else:
    st.write("Please select at least one sub-category to display the chart.")

# (4) Three metrics for selected subcategories
st.write("### (4) Metrics for Selected Sub-Categories")
if selected_subcategories:
    # Filter data for selected subcategories
    filtered_df = df[df['Sub_Category'].isin(selected_subcategories)]
    
    # Calculate metrics
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    # Calculate overall average profit margin for comparison
    overall_total_sales = df['Sales'].sum()
    overall_total_profit = df['Profit'].sum()
    overall_profit_margin = (overall_total_profit / overall_total_sales * 100) if overall_total_sales > 0 else 0
    
    # Calculate delta for profit margin
    profit_margin_delta = profit_margin - overall_profit_margin
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.2f}"
        )
    
    with col2:
        st.metric(
            label="Total Profit", 
            value=f"${total_profit:,.2f}"
        )
    
    with col3:
        st.metric(
            label="Profit Margin",
            value=f"{profit_margin:.2f}%",
            delta=f"{profit_margin_delta:.2f}% vs overall avg"
        )
else:
    st.write("Please select at least one sub-category to display metrics.")
