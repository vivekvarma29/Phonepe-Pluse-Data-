import json
import streamlit as st
import pandas as pd
import requests
import mysql.connector
import plotly.express as px

#CREATE DATAFRAMES FROM SQL
#sql connection
mydb = mysql.connector.connect(host = "localhost",
                        user = "root",
                        password = "0000",
                        database = "phonepe_pluse",
                        port = "3306"
                        )
cursor = mydb.cursor()

#Aggregated_insurance
cursor.execute("select * from aggregated_insurance;")
table0 = cursor.fetchall()
mydb.commit()
Aggre_insurance = pd.DataFrame(table0,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#Aggregated_transsaction
cursor.execute("select * from aggregated_transaction;")
table1 = cursor.fetchall()
mydb.commit()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
cursor.execute("select * from aggregated_user")
table2 = cursor.fetchall()
mydb.commit()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_insurance
cursor.execute("select * from map_insurance")
table3 = cursor.fetchall()
mydb.commit()
Map_insurance = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_transaction
cursor.execute("select * from map_transaction")
table3 = cursor.fetchall()
mydb.commit()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
table4 = cursor.fetchall()
mydb.commit()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_insurance
cursor.execute("select * from top_insurance")
table5 = cursor.fetchall()
mydb.commit()

Top_insurance = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction
cursor.execute("select * from top_transaction")
table5 = cursor.fetchall()
mydb.commit()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
table6 = cursor.fetchall()
mydb.commit()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))


#Insurance tab
def insurance():
    st.markdown("**Details for Insurance**")
    # Group by 'States' and 'Years' and calculate the sum of 'Transaction_amount'
    state_transaction_sum = Aggre_insurance.groupby('States')['Transaction_amount'].sum().reset_index()

    # Plotting the bar graph using Plotly Express
    fig = px.bar(state_transaction_sum, x='States', y='Transaction_amount',
                 labels={'Transaction_amount': 'Total Transaction Amount', 'States': 'State'})
    fig.update_layout(title='Total Transaction Amount by State')
    st.plotly_chart(fig)
    
    c1, c2 = st.columns(2)
    with c1:
        selected_year = st.selectbox('Select Year', Aggre_insurance['Years'].unique())
    with c2:
        Quarter = st.selectbox('Select Quarter', Aggre_insurance['Quarter'].unique())

    # Filter DataFrame based on selected year and quarter
    filtered_df = Aggre_insurance[(Aggre_insurance['Years'] == selected_year) & (Aggre_insurance['Quarter'] == Quarter)]

    # Group by 'States' and calculate the sum of 'Transaction_amount' for each state
    transaction_sum_by_state = filtered_df.groupby('States')['Transaction_amount'].sum().reset_index()
    
    
    # Fetch GeoJSON data from URL
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = response.json()
    states_name_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    states_name_tra.sort()

    # Create choropleth map
    fig_india_1 = px.choropleth(transaction_sum_by_state, geojson=data1, featureidkey="properties.ST_NM", 
                                locations="States", color="Transaction_amount", 
                                color_continuous_scale="Sunsetdark",
                                range_color=(filtered_df["Transaction_amount"].min(), filtered_df["Transaction_amount"].max()),
                                hover_name="States", title=f"{selected_year} TRANSACTION AMOUNT",
                                width=600, height=600)
    fig_india_1.update_geos(fitbounds="locations",visible=False)
    
    # Display the map in Streamlit
    st.plotly_chart(fig_india_1)
    

    # Plotting the bar graph using Plotly Express
    fig = px.bar(transaction_sum_by_state, x='States', y='Transaction_amount',
                 labels={'Transaction_amount': f'Total Transaction Amount', 'States': 'State'})
    fig.update_layout(title=f'Total Transaction Amount by State in {selected_year} - {Quarter}')
    st.plotly_chart(fig)
    
    # Place the select boxes outside the column layout
    selected_tab = st.selectbox("Top Transactions", ["States", "Districts", "Postal Codes"])


    # Display the selected tab content based on the selection
    if selected_tab == "States":
        st.markdown("**Top 10 States**")
        # Group by 'States' and calculate the sum of 'Transaction_amount' for each state
        state_transaction_sum = filtered_df.groupby('States')['Transaction_amount'].sum().reset_index()
        # Sort DataFrame by transaction amount column in descending order
        sorted_df = state_transaction_sum.sort_values(by='Transaction_amount', ascending=False)
        # Get the top 10 transactions
        top_10_transactions = sorted_df.head(10)
        top_10_transactions.set_index('States', inplace=True)
        st.write(top_10_transactions)
        
    elif selected_tab == "Districts":
        st.markdown("**Top 10 Districts**")
        # Add code to display top 10 districts
        Map_insurance = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))
        filter_df = Map_insurance[(Map_insurance['Years'] == selected_year) & (Aggre_insurance['Quarter'] == Quarter)]

        district_transaction_sum = filter_df.groupby('Districts')['Transaction_amount'].sum().reset_index()
        sort_df = district_transaction_sum.sort_values(by='Transaction_amount', ascending=False)
        top_10_districts = sort_df.head(10)
        top_10_districts.set_index('Districts', inplace=True)
        st.write(top_10_districts)
        
    elif selected_tab == "Postal Codes":
        st.markdown("**Top 10 Postal Codes**")
        Top_insurance = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))
        filter_df_pincode = Top_insurance[(Top_insurance['Years'] == selected_year) & (Aggre_insurance['Quarter'] == Quarter)]
        pincode_transaction_sum = filter_df_pincode.groupby('Pincodes')['Transaction_amount'].sum().reset_index()
        sort_df = pincode_transaction_sum.sort_values(by='Transaction_amount', ascending=False)
        top_10_pincodes = sort_df.head(10)
        top_10_pincodes.set_index('Pincodes', inplace=True)
        
        # Remove commas from Transaction_amount column
        top_10_pincodes['Transaction_amount'] = top_10_pincodes['Transaction_amount'].astype(str).str.replace(',', '')

        # Display the top 10 pincodes DataFrame
        st.write(top_10_pincodes)

 #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                
#Transactions Tab 
def Transactions():
    st.markdown("**Details for Transactions**")
    # Group by 'States' and 'Years' and calculate the sum of 'Transaction_amount'
    state_transaction_sum = Aggre_transaction.groupby('States')['Transaction_amount'].sum().reset_index()

    # Plotting the bar graph using Plotly Express
    fig = px.bar(state_transaction_sum, x='States', y='Transaction_amount',
                 labels={'Transaction_amount': 'Total Transaction Amount', 'States': 'State'})
    fig.update_layout(title='Total Transaction Amount by State')
    st.plotly_chart(fig)
    
    c1, c2 = st.columns(2)
    with c1:
        selected_year = st.selectbox('Select Year', Aggre_transaction['Years'].unique())
    with c2:
        Quarter = st.selectbox('Select Quarter', Aggre_transaction['Quarter'].unique())

    # Filter DataFrame based on selected year and quarter
    filtered_df = Aggre_transaction[(Aggre_transaction['Years'] == selected_year) & (Aggre_transaction['Quarter'] == Quarter)]

    # Group by 'States' and calculate the sum of 'Transaction_amount' for each state
    transactions_sum_by_state = filtered_df.groupby('States')['Transaction_amount'].sum().reset_index()
    
    
    # Fetch GeoJSON data from URL
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = response.json()
    states_name_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    states_name_tra.sort()

    # Create choropleth map
    fig_india_2 = px.choropleth(transactions_sum_by_state, geojson=data1, featureidkey="properties.ST_NM", 
                                locations="States", color="Transaction_amount", 
                                color_continuous_scale="Sunsetdark",
                                range_color=(filtered_df["Transaction_amount"].min(), filtered_df["Transaction_amount"].max()),
                                hover_name="States", title=f"{selected_year} TRANSACTION AMOUNT",
                                width=600, height=600)
    fig_india_2.update_geos(fitbounds="locations",visible=False)
    
    # Display the map in Streamlit
    st.plotly_chart(fig_india_2)
    

    # Plotting the bar graph using Plotly Express
    fig1 = px.bar(transactions_sum_by_state, x='States', y='Transaction_amount',
                 labels={'Transaction_amount': f'Total Transaction Amount', 'States': 'State'})
    fig1.update_layout(title=f'Total Transaction Amount by State in {selected_year} - {Quarter}')
    st.plotly_chart(fig1)
    
    # Place the select boxes outside the column layout
    selected_tab = st.selectbox("Top Transactions", ["States", "Districts", "Postal Codes"])


    # Display the selected tab content based on the selection
    if selected_tab == "States":
        st.markdown("**Top 10 States**")
        
        # Group by 'States' and calculate the sum of 'Transaction_amount' for each state
        state_transaction_sum = filtered_df.groupby('States')['Transaction_amount'].sum().reset_index()
        # Sort DataFrame by transaction amount column in descending order
        sorted_df = state_transaction_sum.sort_values(by='Transaction_amount', ascending=False)
        # Get the top 10 transactions
        top_10_transactions = sorted_df.head(10)
        top_10_transactions.set_index('States', inplace=True)
        st.write(top_10_transactions)
        
    elif selected_tab == "Districts":
        st.markdown("**Top 10 Districts**")
        # Add code to display top 10 districts
        Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))
        filter_df = Map_transaction[(Map_transaction['Years'] == selected_year) & (Map_transaction['Quarter'] == Quarter)]

        district_transaction_sum = filter_df.groupby('Districts')['Transaction_amount'].sum().reset_index()
        sort_df = district_transaction_sum.sort_values(by='Transaction_amount', ascending=False)
        top_10_districts = sort_df.head(10)
        top_10_districts.set_index('Districts', inplace=True)
        st.write(top_10_districts)
        
    elif selected_tab == "Postal Codes":
        st.markdown("**Top 10 Postal Codes**")
        Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))
        filter_df_pincode = Top_transaction[(Top_transaction['Years'] == selected_year) & (Top_transaction['Quarter'] == Quarter)]
        pincode_transaction_sum = filter_df_pincode.groupby('Pincodes')['Transaction_amount'].sum().reset_index()
        sort_df = pincode_transaction_sum.sort_values(by='Transaction_amount', ascending=False)
        top_10_pincodes = sort_df.head(10)
        top_10_pincodes.set_index('Pincodes', inplace=True)
        
        # Remove commas from Transaction_amount column
        top_10_pincodes['Transaction_amount'] = top_10_pincodes['Transaction_amount'].astype(str).str.replace(',', '')

        # Display the top 10 pincodes DataFrame
        st.write(top_10_pincodes)
        
        
    #Categories
    st.markdown("**Categories**")
    filter_df_category = Aggre_transaction[(Aggre_transaction['Years'] == selected_year) & (Aggre_transaction['Quarter'] == Quarter)]
    a=filter_df_category.groupby(['Transaction_type'])['Transaction_amount'].sum().reset_index()
    sort_categories = a.sort_values(by='Transaction_amount', ascending=False)
    sorting=sort_categories.head()
    sorting.set_index('Transaction_type',inplace=True)
    st.write(sorting)
    
#********************************************************************************************************************

#User tab    
def user():
    st.markdown("**Details for User**")
    Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

    # Group by 'States' and 'Years' and calculate the sum of 'Transaction_count'
    state_transaction_user = Aggre_user.groupby('States')['Transaction_count'].sum().reset_index()

    # Plotting the bar graph using Plotly Express
    fig2 = px.bar(state_transaction_user, x='States', y='Transaction_count',
                    labels={'Transaction_count': 'Total Transaction count', 'States': 'State'})
    fig2.update_layout(title='Total Transaction count by State')
    st.plotly_chart(fig2)

    c1, c2 = st.columns(2)
    with c1:
        selected_year = st.selectbox('Select Year', Aggre_user['Years'].unique())
    with c2:
        Quarter = st.selectbox('Select Quarter', Aggre_user['Quarter'].unique())

    # Filter DataFrame based on selected year and quarter
    filtered_df = Aggre_user[(Aggre_user['Years'] == selected_year) & (Aggre_user['Quarter'] == Quarter)]

    # Group by 'States' and calculate the sum of 'Transaction_count' for each state
    transactions_sum_by_state = filtered_df.groupby('States')['Transaction_count'].sum().reset_index()

    # Fetch GeoJSON data from URL
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = response.json()
    states_name_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    states_name_tra.sort()

    # Create choropleth map
    fig_india_3 = px.choropleth(transactions_sum_by_state, geojson=data1, featureidkey="properties.ST_NM", 
                                locations="States", color="Transaction_count", 
                                color_continuous_scale="Sunsetdark",
                                range_color=(filtered_df["Transaction_count"].min(), filtered_df["Transaction_count"].max()),
                                hover_name="States", title=f"{selected_year} TRANSACTION count",
                                width=600, height=600)
    fig_india_3.update_geos(fitbounds="locations",visible=False)

    # Display the map in Streamlit
    st.plotly_chart(fig_india_3)

    # Plotting the bar graph using Plotly Express
    fig1 = px.bar(transactions_sum_by_state, x='States', y='Transaction_count',
                    labels={'Transaction_count': f'Total Transaction Count', 'States': 'State'})
    fig1.update_layout(title=f'Total Transaction count by State in {selected_year} - {Quarter}')
    st.plotly_chart(fig1)
    
    # Place the select boxes outside the column layout
    selected_tab = st.selectbox("Top Transactions", ["States", "Districts", "Postal Codes"])

    if selected_tab == "States":
        st.markdown("**Transaction Count by State and Brand**")
        Aggre_user = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))
        filter_df = Aggre_user[(Aggre_user['Years'] == selected_year) & (Aggre_user['Quarter'] == Quarter)]

        # Group by 'States' and 'Brands' and calculate the sum of 'Transaction_count' for each state and brand
        state_brand_transaction_sum = filter_df.groupby(['States', 'Brands'])['Transaction_count'].sum().reset_index()

        st.write(state_brand_transaction_sum)
        
    elif selected_tab == "Districts":
        st.markdown("**All Districts**")
        # Add code to display top 10 districts
        Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))
        filter_df = Map_user[(Map_user['Years'] == selected_year) & (Map_user['Quarter'] == Quarter)]

        district_transaction_sum = filter_df.groupby(['Districts','RegisteredUser'])['AppOpens'].sum().reset_index()
        sort_df = district_transaction_sum.sort_values(by='AppOpens', ascending=False)
        sort_df.set_index('Districts', inplace=True)
        st.write(sort_df)
        
    elif selected_tab == "Postal Codes":
        st.markdown("**Top 10 Postal Codes**")
        Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))
        filter_df_pincode = Top_user[(Top_user['Years'] == selected_year) & (Top_user['Quarter'] == Quarter)]
        pincode_registerd_sum = filter_df_pincode.groupby('Pincodes')['RegisteredUser'].sum().reset_index()
        sort_df = pincode_registerd_sum.sort_values(by='RegisteredUser', ascending=False)
        sort_df.set_index('Pincodes', inplace=True)

        # Display the top 10 pincodes DataFrame
        st.write(sort_df)
    


#Streamlit Code
# st.set_page_config(layout="wide")
# Title
st.title("PhonePe Plus DATA VISUALIZATION AND EXPLORATION")
st.write("")

# Create a dropdown menu in the sidebar
option = st.sidebar.selectbox(
    'Choose an option',
    ('Home', 'Insurance', 'Transactions', 'Users'))

# Display details based on the selected option
if option == 'Home':
    st.write('Details for Home')
    st.write('This is some information about Home.')

elif option == 'Insurance':
    insurance()
    
elif option == 'Transactions':
    Transactions()
  

elif option == 'Users':
    user()
   



  
  
