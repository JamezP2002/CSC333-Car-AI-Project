import requests
import sys
from PIL import Image, ImageDraw
from picamera2 import Picamera2
from datetime import datetime
import time

# Replace with the external IP address of your VM where FastAPI is running
base_URI = 'http://your_vm_ip_address:port/'
# Make sure to replace 'http://your_vm_ip_address:port/' with your actual VM IP address and the port your FastAPI app is running on

def detect_and_draw_cars(filename):
    # 'uploaded_file' is the field expected on the FastAPI side
    with open(filename, 'rb') as f:
        files = {'uploaded_file': f}

        # Detect cars in the captured image
        response = requests.post(base_URI + 'detect/', files=files)  # Adjusted endpoint to match the FastAPI service

        # Make sure the request was successful
        if response.status_code != 200:
            print("Error during car detection:", response.text)
            return

        # Assuming the modified API returns 'cars' with bounding box details
        cars_response = response.json().get('cars', {})
        if not cars_response:
            print("No cars detected.")
            return

        # Draw boxes around the cars
        image = Image.open(filename)
        drawing = ImageDraw.Draw(image)

        for car, details in cars_response.items():
            # Assuming the bounding box is returned as a dictionary with 'box' key
            # containing the coordinates in a [x1, y1, x2, y2] format
            bounding_box = details.get('box', [])
            if bounding_box:
                drawing.rectangle(bounding_box, outline="red")

        save_filename = "cars_detected.jpg"
        image.save(save_filename)

        print("Cars detected, boxes drawn, and saved to", save_filename)

while True:
    # Only capture a new image if no filename was provided as an argument
    if len(sys.argv) < 2:
        # Capture an image
        print("Capturing a new image...")
        picam2 = Picamera2()
        filename = f'capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        picam2.start_and_capture_file(filename)
        picam2.stop()
        print(f"Image captured and saved as {filename}")
    
    detect_and_draw_cars(filename)
    
    # Sleep for 20 seconds before the next loop iteration
    print("Waiting for 20 seconds...")
    time.sleep(20)
