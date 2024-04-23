import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import mysql.connector

# Connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="34.170.42.122",
        user="james",
        password="james6780!!",
        database="james"
    )

# get_car_info() fetches all records without filtering by date
def getCarInfo():
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
        car_info = getCarInfo()
        df = pd.DataFrame(car_info)
        
        # Convert 'recorded_datetime' to datetime
        df['recorded_datetime'] = pd.to_datetime(df['recorded_datetime'])

        # Filter DataFrame based on selected date range
        filtered_df = df[(df['recorded_datetime'] >= pd.to_datetime(start_date)) & 
                         (df['recorded_datetime'] <= pd.to_datetime(end_date))]

        # Optionally, let users choose the aggregation frequency
        freq_selection = st.selectbox('Select frequency for analysis', options=['h', 'd', 'w', 'm', 'y'], index=1)
        
        # Data aggregation
        aggregated_data = aggregate_data(filtered_df, freq=freq_selection)
        st.write('Aggregated Data:', aggregated_data)
        
        # Visualization
        fig = px.line(aggregated_data, x='recorded_datetime', y='counts', title='Aggregated Car Records')
        st.plotly_chart(fig)

        # Aggregating and calculating averages
        # Start_date and end_date are correctly defined
        filtered_df = df[(df['recorded_datetime'] >= pd.to_datetime(start_date)) & 
                        (df['recorded_datetime'] <= pd.to_datetime(end_date))]

        # Debug: Check if 'recorded_datetime' column exists
        if 'recorded_datetime' not in filtered_df.columns:
            st.error("Missing 'recorded_datetime' column. Please check data preparation steps.")
            return  # Exit the function early
        
        # Daily Average
        daily_avg = filtered_df.resample('D', on='recorded_datetime').size().mean()
        st.write(f"Daily Average: {daily_avg:.2f} cars")
        
        # Hourly Average - This makes sense only within days, hence first group by date, then by hour
        hourly_avg = filtered_df.groupby(filtered_df['recorded_datetime'].dt.date).resample('H', on='recorded_datetime').size().groupby(level=0).mean().mean()
        st.write(f"Hourly Average: {hourly_avg:.2f} cars")
        
        # Weekly Average
        weekly_avg = filtered_df.resample('W', on='recorded_datetime').size().mean()
        st.write(f"Weekly Average: {weekly_avg:.2f} cars")



if __name__ == "__main__":
    main()
