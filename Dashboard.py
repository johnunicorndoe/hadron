import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Read the dataset
dataset = pd.read_excel('hadron.xlsx', nrows=194)

# Set page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.markdown(
        """
        <style>
            .stMultiSelect [data-baseweb=select] span{
                max-width: 200px;
                font-size: 0.75rem;
            }
        </style>
        """, unsafe_allow_html=True
    )

# Title
st.title("Sales Dashboard")

# Filter
st.subheader("Please Filter Here:")

# Multiselect options
product_name = st.multiselect("Select Product Name:", dataset["Product Name"].unique(), dataset["Product Name"].unique())
month = st.multiselect("Select Month:", dataset["Month"].unique(), dataset["Month"].unique())

# Filter the dataset based on user selection
selection_query = dataset.query('`Product Name` == @product_name & `Month` == @month')

# Display total sales and total quantity
st.markdown("---")
total_sales = selection_query["Total Price"].sum()
total_quantity = selection_query["Quantity"].sum()

col1, col2 = st.columns(2)

col1.markdown("## • Total Sales:")
col1.subheader(f"{total_sales:,.0f} Rials")
col2.markdown("## • Total Quantity:")
col2.subheader(f"{total_quantity}")

# Display filtered data in a DataFrame
st.markdown("---")
selection_query.index += 1
st.dataframe(selection_query, height=423)

# Create a bar chart for sales by product
filtered_dataset = dataset[(dataset['Product Name'].isin(product_name)) & (dataset['Month'].isin(month))]
fig = go.Figure()

for product in product_name:
    product_data = filtered_dataset[filtered_dataset['Product Name'] == product]
    formatted_prices = product_data['Total Price']

    fig.add_trace(go.Bar(
        x=product_data['Month'],
        y=product_data['Total Price'],
        name=product,
    ))

fig.update_layout(barmode='group', xaxis_tickangle=-45, width=900, title='# Sales by Product')
st.plotly_chart(fig)

# Create a bar chart and pie chart for sales by product
sales_by_product = selection_query.groupby(by=["Product Name"]).sum()[["Total Price"]].sort_values(by="Total Price")
sales_by_product_barchart = px.bar(sales_by_product, x="Total Price", y=sales_by_product.index, title="# Sales by Product", color_discrete_sequence=["#7752FE"])
sales_by_product_barchart.update_layout(plot_bgcolor="rgba(0, 0, 0, 0)", xaxis=dict(showgrid=False), height=700)

sales_by_product_piechart = px.pie(sales_by_product, names=sales_by_product.index, values="Total Price", title="# Sales by Product Distribution", hole=0.3, color=sales_by_product.index, color_discrete_sequence=px.colors.sequential.RdPu_r)
sales_by_product_piechart.update_layout(width=700, height=750)

# Display bar chart and pie chart
st.plotly_chart(sales_by_product_barchart, use_container_width=True)
st.plotly_chart(sales_by_product_piechart, use_container_width=True)

# Hide Streamlit menu and footer
hide_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

st.markdown(hide_css, unsafe_allow_html=True)
