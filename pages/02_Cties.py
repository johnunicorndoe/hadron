import pandas as pd
import streamlit as st

# Load data from the "hadron.xlsx" Excel file, specifically from the "cities" sheet
df = pd.read_excel('hadron.xlsx', sheet_name='Cities')

# Set Streamlit page configuration
st.set_page_config(
    page_title="Cities",
    layout="wide"
)

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

# Title
st.title('Cities')

# Filter
st.subheader("Please Filter Here:")

# Multiselect filter for cities
selected_cities = st.multiselect("Select Cities:", df['City'].unique(), default=df['City'].unique())

# Multiselect filter for months
selected_months = st.multiselect("Select Months:", df['Month'].unique(), default=df['Month'].unique())

st.markdown("---")

# Filter the DataFrame based on user selection
filtered_df = df[df['City'].isin(selected_cities) & df['Month'].isin(selected_months)]

# Totals
total_sales = filtered_df["Total Price"].sum()
total_invoices = int(filtered_df["Invoices"].sum())

col1, col2 = st.columns(2)

with col1:
    st.markdown("## • Total Sales:")
    st.subheader(f"{total_sales:,} Rials")

with col2:
    st.markdown("## • Total Invoices:")
    st.subheader(f"{total_invoices}")

st.markdown("---")

# Display the filtered DataFrame in Streamlit
filtered_df.index += 1
st.dataframe(filtered_df, height=423)
