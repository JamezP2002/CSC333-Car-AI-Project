import mysql.connector

try:
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
            print(f"Inserting {values} into the database")

            # Execute the SQL query
            cursor.execute(sql, values)
            db.commit()

except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
finally:
    if db.is_connected():

        # Query the database to retrieve all records from the table
        selectALL = "SELECT * FROM carInfo"
        cursor.execute(selectALL)
        records = cursor.fetchall()
        print("Printing all records from the table")
        for record in records:
            print(record)
        
        # clean up
        cursor.close()
        db.close()
        print("MySQL worked! Connection is closed")