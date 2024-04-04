import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="testDB"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Read the car and date information from a text file and insert into the database
with open("cars.txt", "r") as file:
    for line in file:
        car, recorded_date = line.strip().split(", ")
        # Prepare the SQL query to insert the car information and date
        sql = "INSERT INTO carInfo (car_name, date) VALUES (%s, %s)"
        values = (car, recorded_date)
        # Execute the SQL query
        cursor.execute(sql, values)

# Commit the changes to the database
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
