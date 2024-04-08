import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testDB"
    )

# Function to get car information for a specific year and month
def get_car_info(year, month):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT * FROM carInfo
    WHERE YEAR(date) = %s AND MONTH(date) = %s
    """
    cursor.execute(query, (year, month))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# Streamlit app
def main():
    st.title("Car Information Visualization")

    # User inputs for year and month
    year = st.number_input("Enter the year", min_value=2000, max_value=2100, value=2023, step=1)
    month = st.number_input("Enter the month", min_value=1, max_value=12, value=4, step=1)

    # Get car info from the database based on user input
    car_info = get_car_info(year, month)

    if car_info:
        df = pd.DataFrame(car_info)
        df['date'] = pd.to_datetime(df['date'])

        # Generate a simple count of cars per day
        df_count = df.groupby(df['date'].dt.date).size().reset_index(name='counts')

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(df_count['date'], df_count['counts'], marker='o', linestyle='-')
        plt.title(f'Car Records for {year}-{month:02d}')
        plt.xlabel('Date')
        plt.ylabel('Number of Cars')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("No car information found for the selected period.")

if __name__ == "__main__":
    main()