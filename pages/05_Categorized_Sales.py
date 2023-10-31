import pandas as pd
import streamlit as st
import plotly.express as px

# Function to load Excel data
def load_data():
    return pd.read_excel('hadron.xlsx', header=0, nrows=7, sheet_name="Categorized Sales")

# Function to filter the DataFrame based on selected months and columns
def filter_data(df, selected_months, selected_columns):
    filtered_df = df[df["Month"].isin(selected_months)][selected_columns]
    return filtered_df

# Function to calculate column totals
def calculate_column_totals(df):
    return df.drop("Month", axis=1).sum()

# Function to display the data and column totals
def display_data(filtered_df, column_totals):
    st.markdown("---")
    col1, col2 = st.columns(2)

    col1.dataframe(filtered_df)
    col2.markdown("**Total by Category:**")
    col2.dataframe(pd.DataFrame({"Totals": column_totals}))

# Function to create and display a line chart
def display_line_chart(filtered_data, x_column, y_columns):
    if len(filtered_data) > 0:
        fig = px.line(filtered_data, x=x_column, y=y_columns, markers=True, line_shape="linear")
        st.plotly_chart(fig)
    else:
        st.warning("No data selected for the chart. Please select at least one month and one category.")

# Main function
def main():
    st.set_page_config(
        page_title="Categorized Sales",
        layout="wide"
    )

    st.title('Categorized Sales')

    df = load_data()

    available_columns = [col for col in df.columns if col != "Month"]
    selected_columns = st.multiselect("Select Categories:", available_columns, default=available_columns)
    selected_months = st.multiselect("Select Months:", df["Month"].unique(), default=df["Month"].unique())

    if "Month" not in selected_columns:
        selected_columns.insert(0, "Month")

    filtered_df = filter_data(df, selected_months, selected_columns)
    column_totals = calculate_column_totals(filtered_df)

    # Display dataframes first
    display_data(filtered_df, column_totals)

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
            # If both are deselected, show a plain chart axis
            st.plotly_chart(px.line(pd.DataFrame(columns=["Month"]), x="Month"))

    # Create a list of selected columns excluding "Speaker" and "Cable"
    other_categories = [col for col in selected_columns if col not in ["Speaker", "Cable"]]

    if other_categories:
        display_line_chart(filtered_df, "Month", other_categories)

if __name__ == "__main__":
    main()
