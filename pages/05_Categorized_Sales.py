import pandas as pd
import streamlit as st
import plotly.express as px

# Function to load Excel data
def load_data(file_path, sheet_name):
    return pd.read_excel(file_path, header=0, nrows=7, sheet_name=sheet_name)

# Function to filter the DataFrame based on selected months and columns
def filter_data(df, selected_months, selected_columns):
    filtered_df = df[df["Month"].isin(selected_months)][selected_columns]
    return filtered_df

# Function to calculate column totals
def calculate_column_totals(df):
    return df.drop("Month", axis=1).sum()

# Function to display a data table and column totals
def display_data_table(filtered_df, column_totals):
    st.markdown("---")
    col1, col2 = st.columns(2)

    col1.dataframe(filtered_df)
    col2.markdown("**Total by Category:**")
    col2.dataframe(pd.DataFrame({"Totals": column_totals}))

# Function to create and display a line chart
def display_line_chart(data, x_column, y_columns):
    if len(data) > 0:
        fig = px.line(data, x=x_column, y=y_columns, markers=True, line_shape="linear")

        # Update the legend title
        fig.update_layout(legend_title_text="Product Category")

        # Update Y-axis title from "title" to "quantity"
        fig.update_yaxes(title_text="Quantity")

        st.plotly_chart(fig)
    else:
        st.warning("No data selected for the chart. Please select at least one month and one category.")

# Main function
def main():
    st.set_page_config(
        page_title="Categorized Sales",
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
    st.title('Categorized Sales')

    # Filter
    st.subheader("Please Filter Here:")

    file_path = 'hadron.xlsx'
    sheet_name = "Categorized Sales"

    df = load_data(file_path, sheet_name)

    available_columns = [col for col in df.columns if col != "Month"]
    selected_columns = st.multiselect("Select Categories:", available_columns, default=available_columns)
    selected_months = st.multiselect("Select Months:", df["Month"].unique(), default=df["Month"].unique())

    if "Month" not in selected_columns:
        selected_columns.insert(0, "Month")

    filtered_df = filter_data(df, selected_months, selected_columns)
    column_totals = calculate_column_totals(filtered_df)

    # Display data table and column totals
    display_data_table(filtered_df, column_totals)

    # Check if "Speaker" and "Cable" are in selected_columns
    if "Speaker" in selected_columns and "Cable" in selected_columns:
        # If both are selected, show the selected line chart
        filtered_cable_speaker = filtered_df[["Month", "Cable", "Speaker"]]
        display_line_chart(filtered_cable_speaker, "Month", ["Cable", "Speaker"])
    else:
        # If only one category is selected, show that category's line chart
        if "Speaker" in selected_columns:
            display_line_chart(filtered_df, "Month", ["Speaker"])
        elif "Cable" in selected_columns:
            display_line_chart(filtered_df, "Month", ["Cable"])
        else:
            # If both are deselected, show an empty chart
            st.plotly_chart(px.line(pd.DataFrame(columns=["Month"]), x="Month"))

    # Create a list of selected columns excluding "Speaker" and "Cable"
    other_categories = [col for col in selected_columns if col not in ["Speaker", "Cable"]]

    if other_categories:
        display_line_chart(filtered_df, "Month", other_categories)

if __name__ == "__main__":
    main()
