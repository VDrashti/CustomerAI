import streamlit as st
import numpy as np
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import altair as alt

def Pricing():
    
    from PandasDF import pd_df_prc
    RESULT=pd_df_prc
    # Sort the DataFrame by the "STOCK_CODE" and "WEEK" columns
    RESULT = RESULT.sort_values(by=["STOCK_CODE", "WEEK"], ascending=[True, False])
    # Keep only the most recent week rows for each unique "STOCK_CODE"
    RESULT = RESULT.drop_duplicates(subset="STOCK_CODE")

   

    prods = st.container()
    upper_panel = st.container()

    with upper_panel:
        col_DEPA, col_CATE,CO1 = st.columns([1,1,4])
        department = np.sort(RESULT['DEPARTMENT'].unique()).tolist()
        dep_selection = col_DEPA.selectbox('DEPARTMENT', department,index=0)
        DF = RESULT.loc[RESULT["DEPARTMENT"]==dep_selection]  
        category = np.sort(DF['CATEGORY'].unique()).tolist()
        category_selection = col_CATE.selectbox('CATEGORY', category,index=0)

        df3 = DF.loc[DF["CATEGORY"]==category_selection]
        stockname = np.sort(df3['STOCK_NAME'].unique()).tolist()
        final_df = DF.loc[DF["CATEGORY"].isin(category)]

        final_df=DF.loc[DF["CATEGORY"]==category_selection]


        # Convert the 'WEEK' column to datetime format
        DF['WEEK'] = pd.to_datetime(DF['WEEK'])
        # Modify the 'WEEK' column to format it as 'MM/DD/YYYY'
        DF['WEEK'] = DF['WEEK'].dt.strftime('%m/%d/%Y')

        result = final_df[["STOCK_CODE","DEPARTMENT","CATEGORY","STOCK_NAME","UNIT_PRICE_FOR_WEEK1","UNIT_PRICE_FOR_WEEK2","UNIT_PRICE_FOR_WEEK3","NEXT_WEEK_PREDICTION"]]
        fig = go.Figure(data=[go.Table(columnwidth=[1.4,2,1.5,2.4,1.8,1.8,1.8,2],header=dict(values=("<b>STOCK CODE<b>","<b>DEPARTMENT<b>","<b>CATEGORY<b>","<b>STOCK NAME<b>","<b>UNIT PRICE LEAD_W1<b>","<b>UNIT PRICE LEAD_W2<b>","<b>UNIT PRICE LEAD_W3<b>","<b>NEXT WEEK PREDICTION<b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 13,height=35),cells=dict(values=[result.STOCK_CODE,result.DEPARTMENT,result.CATEGORY,result.STOCK_NAME,result.UNIT_PRICE_FOR_WEEK1,result.UNIT_PRICE_FOR_WEEK2,result.UNIT_PRICE_FOR_WEEK3,result.NEXT_WEEK_PREDICTION],fill_color = [['white','lightgrey']*3200], align=['left'], font_size = 12))])

        fig.update_layout(autosize=False,width=998,height=350,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff")

        st.markdown('<h1 style="color: #00568D; font-size: 28px;">Price Prediction Insights</h1>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)

		#CHART
		# Find the most recent week for each stock_name
        most_recent_df = final_df.groupby('STOCK_NAME')['WEEK'].max().reset_index()
        most_recent_df = most_recent_df.rename(columns={'WEEK': 'MOST_RECENT_WEEK'})

        # Merge with the original DataFrame to get the unit_price
        final_df = final_df.merge(most_recent_df, on='STOCK_NAME')

                # Filter the DataFrame to only include the most recent week data
        final_df = final_df[final_df['WEEK'] == final_df['MOST_RECENT_WEEK']]
        final_df = final_df.sort_values(by='UNIT_PRICE', ascending=False)

        pd_df_lsrr = final_df[["STOCK_NAME", "UNIT_PRICE", "NEXT_WEEK_PREDICTION"]]
        pd_df_lsrr.rename(columns={'NEXT_WEEK_PREDICTION': 'PREDICTED UNIT PRICE'}, inplace=True)
        pd_df_lsrr.rename(columns={'UNIT_PRICE': 'UNIT PRICE'},inplace=True)

        pd_df_lsrr_pivot = pd_df_lsrr.melt(id_vars='STOCK_NAME', var_name='Price Type', value_name='Price')
               

        # Define custom colors for each Price Type
        color_scale = alt.Scale(
                    domain=['UNIT PRICE', 'PREDICTED UNIT PRICE'],  # Replace with your Price Type values
                    range=['#83C9FF', '#0068C9']  # Define your desired colors
                )

        # Chart for displaying current week Vs predicted price
        st.markdown('<h1 style="color: #00568D; font-size: 28px;">Predicting Future Trends Based on Last Weeks</h1>', unsafe_allow_html=True)
        fig = alt.Chart(pd_df_lsrr_pivot).mark_bar().encode(
                    x=alt.X('STOCK_NAME:N', title='STOCK NAME', axis=alt.Axis(labelAngle=-80, labelFontSize=8)),
                    y=alt.Y('Price:Q', title='PRICE'),
                    color=alt.Color('Price Type:N', scale=color_scale),  # Apply the custom color scale
                    tooltip=[
                        alt.Tooltip('STOCK_NAME:N', title='Stock Name'),
                        alt.Tooltip('Price:Q', title='Price'),
                        alt.Tooltip('Price Type:N', title='Price Type')
                    ]
                ).properties(
                    width=700,
                    height=500,
                )
        st.altair_chart(fig, use_container_width=True)


        def condition(x):
                            if x in [12,1,2]:
                                return 'Winter'
                            elif x in [3,4,5]:
                                return 'Spring'
                            elif x in [6,7,8]:
                                return 'Summer'
                            elif x in [9,10,11]:
                                return 'Fall'

        # Convert 'WEEK' column to datetime format
        final_df['WEEK'] = pd.to_datetime(final_df['WEEK'])
        final_df["MONTH_YEAR"] = final_df["WEEK"].dt.month

        final_df['SEASONS'] = final_df["MONTH_YEAR"].apply(condition)

        # Group by category and season and calculate the average profit margin percentage
        seasonal_avg_profit = final_df.groupby(['CATEGORY', 'SEASONS'])['PROFIT_MARGIN_PERCENTAGE'].mean().reset_index()
        
        # Creating bar chart for Seasonal Analysis

        fig2 = px.bar(seasonal_avg_profit, x="SEASONS", y="PROFIT_MARGIN_PERCENTAGE", color="CATEGORY",
                            labels={"PROFIT_MARGIN_PERCENTAGE": "Average Profit Margin (%)", "SEASONS": "SEASON"}
                            , height=400, width=1000, template="gridon",text="PROFIT_MARGIN_PERCENTAGE")
                
        fig2.update_xaxes(title_text="SEASON", title_font=dict(size=14))
        fig2.update_yaxes(title_text="AVERAGE PROFIT MARGIN (%)", title_font=dict(size=14))

        # Format the text on the bars as percentage
        fig2.update_traces(texttemplate='<b>%{text:.2f}%</b>', textposition='inside', hoverinfo='none')
        fig2.update_traces(hovertemplate='')
        fig2.update_traces(textfont=dict(color='white', size=15))  

        # Display the chart in Streamlit
        st.markdown(f'<h1 style="color: #00568D; font-size: 28px;">Average Profit Margin for Category: {category_selection}</h1>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        return 0
