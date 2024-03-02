import subprocess
import RPi.GPIO as GPIO
import time
from datetime import datetime

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

# Improved debounce handling
def debounce(pin):
    # Wait for the button press to be stable for 0.05 seconds
    time.sleep(0.05)
    return GPIO.input(pin) == GPIO.LOW

if __name__ == "__main__":
    print("Ready to capture images. Press the button.")
    try:
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False and debounce(button_pin):  # Button is pressed
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_directory = "/home/gwenzhang/Documents/photos/"  # Ensure this directory exists
                output_file = f"{output_directory}photo_{timestamp}.jpg"
                capture_image(output_file)
                # Wait a bit after capturing to prevent accidental multiple captures
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()
