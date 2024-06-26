import http.client
import cv2
import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Retrieve user and password from environment variables
camera_user = os.getenv('CAMERA_USER', 'default_user')
camera_password = os.getenv('CAMERA_PASSWORD', 'default_password')

# Construct the camera URL using the retrieved credentials
def capture_image():
    camera_url = f"rtsp://{camera_user}:{camera_password}@192.168.26.223:554/Streaming/channels/101/"
    cap = cv2.VideoCapture(camera_url)
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'image_{timestamp}.jpg'
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
    else:
        print("Failed to capture image")
    cap.release()

def main():
    conn = http.client.HTTPConnection('192.168.26.242', 80)
    last_capture_time = 0
    capture_delay = 10  # in seconds, twice as time as Arduino's delay (5 sec)

    while True:
        conn.request("GET", "/")
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        
        ### Testing motions
        if 'Motion Detected!' in data:
            print("HIGH")
        else: 
            print("LOW")
        ###
        
        
        current_time = time.time()
        if 'Motion Detected!' in data and (current_time - last_capture_time) > capture_delay:
            print("Motion detected, capturing image...")
            capture_image()
            last_capture_time = current_time  # Update the last capture time

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", str(e))
