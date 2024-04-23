from datetime import datetime, timedelta
import random

# Car brands and models
car_brands = ["Toyota", "Ford", "Chevrolet", "Honda", "Mercedes", "BMW", "Audi", "Volkswagen", "Porsche", "Lexus"]
car_models = ["Camry", "F-150", "Impala", "Civic", "C-Class", "3 Series", "A4", "Golf", "911", "RX"]

# Date range
start_date = datetime(2023, 4, 1)
end_date = datetime(2023, 7, 31)
delta = end_date - start_date

# Generate 1000 random dates within the specified range
dates = [(start_date + timedelta(days=random.randint(0, delta.days))).strftime('%Y-%m-%d') for _ in range(1000)]

# Generate 1000 car and date combinations
cars_with_dates = [f"{random.choice(car_brands)} {random.choice(car_models)}, {date}\n" for date in dates]

# File path
file_path = "cars.txt"
# Write to a file
with open(file_path, "w") as file:
    file.writelines(cars_with_dates)
