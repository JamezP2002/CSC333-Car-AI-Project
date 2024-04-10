'''
API method can be accessed using curl:

curl -X 'POST' \
  'http://VM_EXTERNAL_IP:8080/detect/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@IMAGE_FILE.jpg;type=image/jpeg'


Google sample test code for vision API:
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/vision/snippets/detect/detect.py

GCP requirement:
Before running, go to the Google Vision API menu in the GCP console
and enable the API

Python requirements (create a Python virtual environment):
google-cloud-vision==3.4.2, fastapi, uvicorn, python-multipart
'''

from fastapi import FastAPI, UploadFile
from google.cloud import vision
import os
from datetime import datetime
import mysql.connector

app = FastAPI()

@app.post('/detect/')
async def detect_cars(uploaded_file: UploadFile):
    path = f"img/{uploaded_file.filename}"
    response = {}

    if not os.path.exists('img/'):
        os.makedirs('img/')
    
    content = None
    with open(path, "wb") as out_file:
        content = await uploaded_file.read()
        out_file.write(content)

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    # Object detection
    objects = client.object_localization(image=image).localized_object_annotations
    car_objects = [obj for obj in objects if obj.name.lower() in ['car', 'vehicle']]
    print(f"Number of cars found: {len(car_objects)}")
    response['cars'] = {}

    # Connect to MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",  # Update with your MySQL user
        password="your_mysql_password",  # Update with your MySQL password
        database="your_database_name"  # Update with your database name
    )
    cursor = db.cursor()

    for idx, car in enumerate(car_objects):
        vertices = [(vertex.x, vertex.y) for vertex in car.bounding_poly.normalized_vertices]
        if vertices:
            x_min = min(vertex[0] for vertex in vertices)
            y_min = min(vertex[1] for vertex in vertices)
            x_max = max(vertex[0] for vertex in vertices)
            y_max = max(vertex[1] for vertex in vertices)
            bounding_box = [x_min, y_min, x_max, y_max]
        else:
            bounding_box = []
        
        car_info = {
            "score": f"{car.score:0.2f}",
            "box": bounding_box
        }
        response['cars'][f"car_{idx}"] = car_info
        print(f"Car {idx} (confidence: {car.score:0.2f}, box: {bounding_box})")
        
        # Insert the car index and the current date-time into the MySQL database
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO carInfo (date) VALUES (%s)"
        values = (now)
        cursor.execute(sql, values)
        db.commit()

    # Close MySQL connection
    cursor.close()
    db.close()

    # Optionally, remove the saved file after processing
    os.remove(path)
    
    return response

