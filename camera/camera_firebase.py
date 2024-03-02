import subprocess
import RPi.GPIO as GPIO
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, storage

# Setup GPIO for button
button_pin = 2  # Update this pin according to your setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to capture image
def capture_image(output_file):
    try:
        result = subprocess.run(["libcamera-still", "-o", output_file], check=True)
        if result.returncode == 0:
            print(f"Image successfully captured and saved as {output_file}")
        else:
            print("Failed to capture image.")
    except subprocess.CalledProcessError as e:
        print(f"Error capturing image: {e}")

# Function to debounce button
def debounce(pin):
    time.sleep(0.05)
    return GPIO.input(pin) == GPIO.LOW

# Function to upload image to Firebase Storage
def upload_to_firebase(image_path):
    bucket = storage.bucket()
    blob = bucket.blob("photos/" + image_path.split("/")[-1])  # Save in "photos" directory
    try:
        blob.upload_from_filename(image_path)
        print("Image uploaded to Firebase Storage successfully")
    except Exception as e:
        print(f"Failed to upload image to Firebase Storage: {e}")

if __name__ == "__main__":
    print("Ready to capture images. Press the button.")
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("robin-3d81f-firebase-adminsdk-vzsly-04e666e175.json")
    firebase_admin.initialize_app(cred, {
        "storageBucket": "robin-3d81f.appspot.com"
    })
    
    try:
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False and debounce(button_pin):  # Button is pressed
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_directory = "/home/gwenzhang/Documents/photos/"  # Ensure this directory exists
                output_file = f"{output_directory}photo_{timestamp}.jpg"
                capture_image(output_file)
                upload_to_firebase(output_file)  # Upload to Firebase after capturing
                time.sleep(2)  # Wait for 2 seconds between captures
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()
