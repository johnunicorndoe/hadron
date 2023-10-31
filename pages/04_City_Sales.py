import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load data from Excel sheet
file_path = 'hadron.xlsx'
sheet_name = 'City Sales'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Title
st.title('City Sales')

# Filter
st.subheader("Please Filter Here:")

# Multiselect filters
selected_cities = st.multiselect("Select Cities:", df["City"].unique(), default=df["City"].unique())
selected_months = st.multiselect("Select Months:", df.columns[1:], default=df.columns[1:].tolist())

# Filter the data
filtered_data = df[df["City"].isin(selected_cities)][["City"] + selected_months]

# Total sales for each city's row
filtered_data['Total Sales'] = filtered_data[selected_months].sum(axis=1)

# Total sales for each month
column_totals = filtered_data[selected_months].sum()

# Total of "Total Sales" column
total_sales_total = filtered_data['Total Sales'].sum()

# Pie chart for "Total Sales"
fig_pie = px.pie(
    values=filtered_data['Total Sales'],
    names=filtered_data['City'],
    title="# Total Sales Distribution"
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
    yaxis_title='Sales',
    title="# Sales of Each City in Each Month",
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
st.write("**# The Amount of Monthly Sales of Products by City**")
filtered_data.index += 1
st.dataframe(filtered_data)

col1, col2, col3 = st.columns(3)

col1.write("**# Total Sales for Each City's Row**")
col1.dataframe(filtered_data[['City', 'Total Sales']])

col2.write("**# Total Sales for Each Month**")
col2.dataframe(pd.DataFrame({"Total Sales": column_totals}))

col3.write("**# Total of Total Sales**")
col3.markdown(f"- {total_sales_total:,} Rials")

st.plotly_chart(fig_pie)

st.plotly_chart(fig_bar)
