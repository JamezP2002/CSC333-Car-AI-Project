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

# This will store the bounding boxes from the previous API call
# Consider using a more persistent solution for production
previous_boxes = set()

def is_similar_box(box1, box2, threshold=0.01):
    """Check if two bounding boxes are similar within a given threshold."""
    return all(abs(b1 - b2) < threshold for b1, b2 in zip(box1, box2))

def get_non_duplicate_boxes(new_boxes, previous_boxes, threshold=0.01):
    """Filter out new boxes that are similar to any of the previous boxes."""
    non_duplicates = []
    for new_box in new_boxes:
        if not any(is_similar_box(new_box, prev_box, threshold) for prev_box in previous_boxes):
            non_duplicates.append(new_box)
    return non_duplicates

@app.post('/detectCar/')
async def detect_cars(uploaded_file: UploadFile):
    global previous_boxes
    new_boxes = []
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

    # Preparing new bounding boxes
    for idx, car in enumerate(car_objects):
        vertices = [(vertex.x, vertex.y) for vertex in car.bounding_poly.normalized_vertices]
        if vertices:
            x_min = min(vertex[0] for vertex in vertices)
            y_min = min(vertex[1] for vertex in vertices)
            x_max = max(vertex[0] for vertex in vertices)
            y_max = max(vertex[1] for vertex in vertices)
            new_boxes.append((x_min, y_min, x_max, y_max))

    # Filter out duplicates using similarity check
    non_duplicate_boxes = get_non_duplicate_boxes(new_boxes, previous_boxes)
    previous_boxes.update(non_duplicate_boxes)  # Update previous_boxes with non-duplicates

    # Connect to MySQL database
    db = mysql.connector.connect(
        host="34.170.42.122",
        user="james", 
        password="james6780!!",  
        database="james"
    )
    cursor = db.cursor()

    # Processing non-duplicate boxes
    for idx, box in enumerate(non_duplicate_boxes):
        car_info = {
            "score": "Detected",  # Example value, adjust as necessary
            "box": box
        }
        response['cars'][f"car_{idx}"] = car_info
        print(f"Car {idx} (box: {box})")
        
        # Insert the detection into the MySQL database
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO carInfo (recorded_datetime) VALUES (%s)"
        values = (now,)
        cursor.execute(sql, values)
        db.commit()

    # Close MySQL connection
    cursor.close()
    db.close()

    # Optionally, remove the saved file after processing
    os.remove(path)
    
    return response


