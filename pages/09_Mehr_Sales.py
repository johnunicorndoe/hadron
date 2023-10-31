import pandas as pd
import streamlit as st
import plotly.express as px

def main():
    # Load data
    df = pd.read_excel('hadron.xlsx', nrows=28, sheet_name="Mehr Sales")

    # Set Streamlit page configuration
    st.set_page_config(
        page_title="Mehr Sales",
        layout="wide"
    )

    # Title
    st.title('Mehr Sales')

    # Filter
    st.subheader("Please Filter Here:")

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

    product_name = st.multiselect(
        "Select Product Name:",
        options=df["Product Name"].unique(),
        default=df["Product Name"].unique()
    )

    selection_query = df[df['Product Name'].isin(product_name)]

    st.markdown("---")

    # Totals
    total_sales = selection_query["Total Price"].sum()
    total_quantity = selection_query["Total Quantity"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## • Total Sales:")
        st.subheader(f"{total_sales:,} Rials")

    with col2:
        st.markdown("## • Total Quantity:")
        st.subheader(f"{total_quantity}")

    st.markdown("---")

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

    # Display data with modified index
    selection_query.index += 1
    st.dataframe(selection_query, height=423)

    # Create a bar chart
    product_quantity = selection_query.groupby("Product Name")["Total Quantity"].sum().reset_index()
    fig = px.bar(product_quantity, x="Product Name", y="Total Quantity", title="# Total Quantity of Each Product")

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
