"""
This Streamlit application is designed for visualizing the analysis of car records over time. 
It connects to a MySQL database to retrieve car information, including timestamps of recorded data, 
and allows users to filter records within a specified date range. The application provides interactive
 elements for selecting start and end dates, and for choosing the frequency of data aggregation.

Key functionalities include:
- Interactive date range selection for filtering car records.
- Connection to a MySQL database to fetch car records.
- Aggregation of car data into specified time intervals (e.g., hourly, daily, weekly, monthly, yearly).
- Visualization of aggregated data using Plotly for a dynamic and interactive experience.

Upon selection of the date range and aggregation frequency by the user, the application fetches and 
processes the relevant car records from the database, aggregates the data based on the specified frequency,
 and visualizes the trends over time through a line chart.

Usage:
1. The user selects a start and end date for the analysis period.
2. The user selects the desired frequency for data aggregation (e.g., daily, weekly).
3. The application fetches and filters car records from the MySQL database based on the specified date range.
4. Aggregated data is visualized in a Plotly line chart, showing the count of car records over the selected period.

This application demonstrates the integration of Streamlit with data processing libraries like Pandas and Plotly, 
along with database operations using MySQL Connector. It provides a simple yet powerful tool for analyzing and 
visualizing time-series data from car records.

Note: Ensure the MySQL database is accessible and the credentials in the `connect_to_db` function are 
correctly set before running the application.

Python requirements:
install requirements.txt
"""


import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import mysql.connector

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="34.170.42.122",
        user="james",
        password="james6780!!",
        database="james"
    )

# Assuming get_car_info() fetches all records without filtering by date
def get_car_info():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT carID, recorded_datetime FROM carInfo
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# Function to aggregate car data into different time intervals
def aggregate_data(df, freq='D'):
    df['recorded_datetime'] = pd.to_datetime(df['recorded_datetime'])
    df.set_index('recorded_datetime', inplace=True)
    aggregated_df = df.resample(freq).size().reset_index(name='counts')
    return aggregated_df

# Modified main function to include date range selection and DataFrame filtering
def main():
    st.title('Car Record Analysis')

    # User inputs for date range
    start_date = st.date_input('Start date', value=pd.to_datetime('2024-04-11'))
    end_date = st.date_input('End date', value=pd.to_datetime('2024-04-30'))

    if start_date > end_date:
        st.error('Error: End date must be after start date.')
    else:
        # Data retrieval
        car_info = get_car_info()
        df = pd.DataFrame(car_info)
        
        # Convert 'recorded_datetime' to datetime
        df['recorded_datetime'] = pd.to_datetime(df['recorded_datetime'])

        # Filter DataFrame based on selected date range
        filtered_df = df[(df['recorded_datetime'] >= pd.to_datetime(start_date)) & 
                         (df['recorded_datetime'] <= pd.to_datetime(end_date))]

        # Optionally, let users choose the aggregation frequency
        freq_selection = st.selectbox('Select frequency for analysis', options=['H', 'D', 'W', 'M', 'Y'], index=1)
        
        # Data aggregation
        aggregated_data = aggregate_data(filtered_df, freq=freq_selection)
        st.write('Aggregated Data:', aggregated_data)
        
        # Visualization
        fig = px.line(aggregated_data, x='recorded_datetime', y='counts', title='Aggregated Car Records')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
