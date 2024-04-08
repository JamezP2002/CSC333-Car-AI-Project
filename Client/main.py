import requests
import sys
from PIL import Image, ImageDraw

# Replace with the external IP address of your VM where FastAPI is running
base_URI = 'http://your_vm_ip_address:port/'
# Make sure to replace 'http://your_vm_ip_address:port/' with your actual VM IP address and the port your FastAPI app is running on

if len(sys.argv) < 2:
    print("Please provide a filename as an argument.")
    sys.exit(1)

filename = sys.argv[1]

# 'uploaded_file' is the field expected on the FastAPI side
files = {'uploaded_file': open(filename, 'rb')}

# Detect cars in the captured image
response = requests.post(base_URI + 'detect/', files=files)  # Adjusted endpoint to match the FastAPI service

# Make sure the request was successful
if response.status_code != 200:
    print("Error during car detection:", response.text)
    sys.exit(1)

# Assuming the modified API returns 'cars' with bounding box details
cars_response = response.json().get('cars', {})
if not cars_response:
    print("No cars detected.")
    sys.exit(0)

# Draw boxes around the cars
image = Image.open(filename)
drawing = ImageDraw.Draw(image)

for car, details in cars_response.items():
    # Assuming the bounding box is returned as a dictionary with 'box' key
    # containing the coordinates in a [x1, y1, x2, y2] format
    bounding_box = details.get('box', [])
    if bounding_box:
        drawing.rectangle(bounding_box, outline="red")

image.save("cars_detected.jpg")

print("Cars detected, boxes drawn, and saved to cars_detected.jpg.")