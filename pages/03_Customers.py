import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load data from Excel sheet
file_path = 'hadron.xlsx'
sheet_name = 'Customers'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Title
st.title('Customers')

# Filter
st.subheader("Please Filter Here:")

# Multiselect filters
selected_cities = st.multiselect("Select Cities:", df["City"].unique(), default=df["City"].unique())
selected_months = st.multiselect("Select Months:", df.columns[1:], default=df.columns[1:].tolist())

# Filter the data
filtered_data = df[df["City"].isin(selected_cities)][["City"] + selected_months]

# Total customers for each month
column_totals = filtered_data[selected_months].sum()

# Total of "Total Customers" column
total_customers_total = filtered_data['Total Customers'].sum()

# Pie chart for "Total Sales"
fig_pie = px.pie(
    values=filtered_data['Total Customers'],
    names=filtered_data['City'],
    title="# Total Customers Distribution"
)

# Bar chart for sales of each city in each column
fig_bar = go.Figure()

for city in selected_cities:
    data_for_city = filtered_data[filtered_data['City'] == city]
    trace = go.Bar(
        x=selected_months,
        y=[data_for_city[column].values[0] for column in selected_months],
        name=city
    )
    fig_bar.add_trace(trace)

fig_bar.update_layout(
    barmode='group',
    xaxis_title='City',
    yaxis_title='Customers',
    title="# Customers of Each City in Each Month",
)

# Streamlit App

# Hide Streamlit's menu, header, and footer
st.markdown(
    """
    <style>
        #MainMenu { visibility:hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("---")

# Display DataFrames and Charts
st.write("**# Monthly Customers by city**")
st.dataframe(filtered_data)

col1, col2, col3 = st.columns(3)

col1.write("**# Total Customers for Each City**")
col1.dataframe(filtered_data[['City', 'Total Customers']])

col2.write("**# Total Customers for Each Month**")
col2.dataframe(column_totals)

col3.write("**# Total of Total Customers**")
col3.markdown(f"- {total_customers_total:,} 🧍🧍‍♀️🧍‍♂️")

st.plotly_chart(fig_pie)

st.plotly_chart(fig_bar)
