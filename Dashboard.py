import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


dataset = pd.read_excel('hadron.xlsx', nrows = 194)

# Set page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
    )

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

product_name = st.sidebar.multiselect(
		"Select Product Name:",
		options = dataset["Product Name"].unique(),
		default = dataset["Product Name"].unique()
        )

month = st.sidebar.multiselect(
		"Select Month:",
		options = dataset["Month"].unique(),
		default = dataset["Month"].unique()
)

selection_query = dataset.query(
    '`Product Name` == @product_name & `Month` == @month'
    )

# ---- MAINPAGE ----
st.title("Sales Dashboard")

total_sales = (selection_query["Total Price"].sum())
total_quantity = (selection_query["Quantity"].sum())


first_column, second_column = st.columns(2)

with first_column:
	st.markdown("# Total Sales:")
	st.subheader(f"{total_sales:,} Rials")
with second_column:
	st.markdown("# Total Quantity:")
	st.subheader(f"{total_quantity}")

st.markdown("---")

st.dataframe(selection_query)



filtered_dataset = dataset[(dataset['Product Name'].isin(product_name)) & (dataset['Month'].isin(month))]

fig = go.Figure()

# Iterate over selected product names and add traces to the figure
for product_name in product_name:
    product_data = filtered_dataset[filtered_dataset['Product Name'] == product_name]

# Format the 'Total Price' column using locale to display it in rials
    formatted_prices = product_data['Total Price'].apply(lambda x: '{:,.0f} rials'.format(x))
    

    fig.add_trace(go.Bar(
        x=product_data['Month'],
        y=product_data['Total Price'],  # Assuming you have a 'Total Price' column
        name=product_name,
    ))

# Customize the layout
fig.update_layout(barmode='group', xaxis_tickangle=-45)
st.plotly_chart(fig)




sales_by_product = (selection_query.groupby(by = ["Product Name"]).sum()[["Total Price"]].sort_values(by = "Total Price"))

sales_by_product_barchart = px.bar(sales_by_product,
									 x = "Total Price",
									 y = sales_by_product.index,
									 title = "Sales by Product",
									 color_discrete_sequence = ["#7752FE"]
									 )

sales_by_product_barchart.update_layout(plot_bgcolor = "rgba(0, 0, 0, 0)",
										xaxis = (dict(showgrid = False)),
										height = 700
										)

sales_by_product_piechart = px.pie(sales_by_product,
								   names = sales_by_product.index,
								   values = "Total Price",
								   title = "Sales by Product",
								   hole = .3,
								   color = sales_by_product.index,
								   color_discrete_sequence = px.colors.sequential.RdPu_r
								   )

sales_by_product_piechart.update_layout(width = 700, height = 750)

# left_column, right_column = st.columns(2)
st.plotly_chart(sales_by_product_barchart, use_container_width = True)
st.plotly_chart(sales_by_product_piechart, use_container_width = True)

hide = """
	<style>
		#MainMenu {
			visibility: hidden;
			}
		footer {
			visibility: hidden;
			}
		header {
			visibility: hidden;
			}
	</style>
"""

st.markdown(hide, unsafe_allow_html = True)

# @st.cache_data
# def get_data_from_excel():
# 	df = pd.read_excel(
# 		io = 'summary.xlsx',
# 		engine = 'openpyxl',
# 		sheet_name = 'hadron',
# 		skiprows = 0,
# 		usecols = 'A:I',
# 		nrows = 539,
# 	)
# 	# Add 'hour' column to dataframe
# 	# df["hour"] = pd.to_datetime(df["Time"], format = "%H:%M:%S").dt.hour
# 	return df
# df = get_data_from_excel()


