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

from fastapi import FastAPI, File, UploadFile
from google.cloud import vision

app = FastAPI()

@app.post('/detect/')
async def detect_cars(uploaded_file: UploadFile):
    path = f"img/{uploaded_file.filename}"
    response = {}
    
    content = None
    with open(path, "wb") as out_file:
        content = uploaded_file.file.read()
        out_file.write(content)

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    # Object detection
    objects = client.object_localization(image=image).localized_object_annotations
    car_objects = [obj for obj in objects if obj.name.lower() in ['car', 'vehicle']]
    print(f"Number of cars found: {len(car_objects)}")
    response['cars'] = {}
    for idx, car in enumerate(car_objects):
        # Assuming you only want to include cars in the response
        response['cars'][f"{car.name}_{idx}"] = f"{car.score:0.2f}" 
        print(f"{car.name} (confidence: {car.score:0.2f})")
        
    return response
