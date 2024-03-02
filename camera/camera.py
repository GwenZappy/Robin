import subprocess
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Setup GPIO
button_pin = 2
GPIO.setwarnings(False)  # Disable warnings
GPIO.cleanup()  # Clean up any previous GPIO configurations
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set button pin as input with pull-up resistor

# Define the directory where photos will be saved
photo_directory = "/home/gwenzhang/Documents/photos"
# Ensure this directory exists or create it before running the script

# Function to capture image using libcamera-still command
def capture_image(output_file):
    subprocess.run(["libcamera-still", "-o", output_file])

if __name__ == "__main__":
    print("Ready to capture images. Press the button.")

    try:
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False:  # Button is pressed
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_file = f"{photo_directory}photo_{timestamp}.jpg"
                capture_image(output_file)
                print(f"Image captured and saved as {output_file}")
                
                # Add a short delay to debounce and avoid multiple captures
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
