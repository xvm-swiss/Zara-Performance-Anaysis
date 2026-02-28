import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st          #
from wordcloud import WordCloud

st.set_page_config( 'Analysis Dashboard', ':bar_chart:', 'wide' )

#df = pd.read_csv( r'C:\Users\X2-win\Desktop\Python Kursmaterialien\New Horizon\Data Science\ds_Session_10_Zara_3_lösungen\data\cleaned data\cleaned_data.csv' )
df = pd.read_csv('\data\cleaned data\cleaned_data.csv')




# KPIs Calculation



# Filter SideBar
prom = st.sidebar.multiselect( 'Promotion',
                       options= df['Promotion'].unique(),
                       default= df['Promotion'].unique())
section = st.sidebar.multiselect( 'section',
                       options= df['section'].unique(),
                       default= df['section'].unique())

price = st.sidebar.slider( 'price',
                            min_value= df['price'].min(),
                            max_value= df['price']. max() )


filtered_df = df.query( ' Promotion ==  @prom and section == @section and price >= @price' )

no_of_transactions = len( filtered_df )
no_of_terms = filtered_df['terms'].nunique()
no_of_units_sold = int( filtered_df['Sales_Volume'].sum() )
avg_price = float( round( filtered_df['price'].mean(), 2 ) )
total_sales = float( round( filtered_df['Total_Sales'].sum(), 2 ) )

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns( 5 )

kpi_1.markdown( f'<h3>Total No. of tranasactions<br>{ no_of_transactions }</h3>', unsafe_allow_html=True )
kpi_2.markdown( f'<h3>Total No. of Terms (Categories)<br>{ no_of_terms }</h3>', unsafe_allow_html=True )
kpi_3.markdown( f'<h3>Total No. of Units Sold<br>{ no_of_units_sold }</h3>', unsafe_allow_html=True )
kpi_4.markdown( f'<h3>Avg. Price of a product<br>{ avg_price }</h3>', unsafe_allow_html=True )
kpi_5.markdown( f'<h3>Total Revenue<br>{ total_sales }</h3>', unsafe_allow_html=True )


# Visualization Part
sales_volume_product_pos =   px.histogram( filtered_df, x = 'Sales_Volume', y = 'Product_Position', color = 'Product_Position' ,
             color_discrete_map= {
                 'Aisle' : '#000926',
                 'End-cap' : '#0F52BA',
                 'Front of Store' : '#A6C5D7'
                 
             }, template = 'simple_white', title = 'Sum of Sales Volume By Product Position', width = 800)

total_sales_by_terms =   px.histogram( filtered_df, x = 'terms', y = 'Total_Sales', color = 'terms',
             color_discrete_sequence= px.colors.qualitative.Prism, template = 'simple_white',
             title = 'Total Sales By Term (Category)')

row_1_col_1, row_1_col_2, row_1_col_3 = st.columns( 3, border = False )

row_1_col_1.plotly_chart( sales_volume_product_pos )
row_1_col_2.plotly_chart( total_sales_by_terms )


value_to_use = row_1_col_3.selectbox( 'Select a column to calc. below sunburst',
                      options = [ 'price', 'Total_Sales', 'Sales_Volume' ])

sunburst_section_and_terms =  px.sunburst( filtered_df, path = [ 'section', 'terms' ], values = value_to_use,
                                          title = f'{value_to_use} by section & terms')
row_1_col_3.plotly_chart( sunburst_section_and_terms )



row_2_col_1, row_2_col_2 = st.columns( 2 )

fig, ax = plt.subplots( figsize = ( 15, 7 ) )

wc_name =  WordCloud( background_color= 'white' ).generate( ' '.join( df['name'] ) )
ax.imshow( wc_name ); ax.axis( 'off' )

row_2_col_1.markdown( '<h3>Frequency of words in product names</h3>', unsafe_allow_html=True )
row_2_col_1.pyplot( fig )

wc_desc = WordCloud( background_color= 'white' ).generate( ' '.join( df['description'] ) )

fig, ax = plt.subplots()
ax.imshow( wc_desc ); ax.axis( 'off' )
row_2_col_2.markdown( '<h3>Frequency of words in product description</h3>', unsafe_allow_html=True )
row_2_col_2.pyplot( fig )
