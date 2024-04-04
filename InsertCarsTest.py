# Let's generate a .txt file with 100 car models and dates

car_brands = ["Toyota", "Ford", "Chevrolet", "Honda", "Mercedes", "BMW", "Audi", "Volkswagen", "Porsche", "Lexus"]
car_models = ["Camry", "F-150", "Impala", "Civic", "C-Class", "3 Series", "A4", "Golf", "911", "RX"]
dates = [f"2023-04-{str(i).zfill(2)}" for i in range(1, 101)]

# Generate car and date combinations
cars_with_dates = [f"{brand} {model}, {date}\n" for brand, model, date in zip(car_brands * 10, car_models * 10, dates)]

# Write to a file
file_path = "cars.txt"
with open(file_path, "w") as file:
    file.writelines(cars_with_dates)
 
print(f"Generated {file_path} with 100 car models and dates")