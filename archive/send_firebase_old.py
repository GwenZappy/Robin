import subprocess
import RPi.GPIO as GPIO
import time
from datetime import datetime
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin
cred = credentials.Certificate("robin-3d81f-firebase-adminsdk-vzsly-04e666e175.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://robin-3d81f-default-rtdb.firebaseio.com'  # Your Realtime Database URL
})

# Setup GPIO for button and LED
button_pin = 2  # Update this pin according to your setup
led_pin = 17    # Update this pin according to your setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)

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

# Function to load TensorFlow Lite model
def load_tflite_model():
    interpreter = tflite.Interpreter(model_path="ei-robin-transfer-learning-tensorflow-lite-float32-model.lite")
    interpreter.allocate_tensors()
    return interpreter

# Function to preprocess the image for the model
def preprocess_image(image_path, input_size = (96,96)):
    with Image.open(image_path) as img:
        img = img.resize(input_size, Image.Resampling.LANCZOS)
        img = img.convert('RGB')
        # Convert image to numpy array and normalize to float32 in range [0, 1]
        input_data = np.array(img, dtype=np.float32) / 255.0
    # Add a batch dimension
    return np.expand_dims(input_data, axis=0)


# Function to run inference on the image
def run_inference(interpreter, image_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], image_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

# Define class labels for interpretation of the model results
class_labels = ['Compost Plate', 'No Plate', 'Trash Plate', 'Uncertain']

# Define a confidence threshold
CONFIDENCE_THRESHOLD = 0.7  # This means 70%

# Function to interpret and process inference results
def interpret_results(output_data):
    probabilities = np.squeeze(output_data)
    predicted_class_index = np.argmax(probabilities)
    confidence = probabilities[predicted_class_index]

    # Check if the confidence meets the threshold
    if confidence < CONFIDENCE_THRESHOLD:
        # If below threshold, classify as "Uncertain"
        predicted_label = 'Uncertain'
    else:
        # If above threshold, use the model's prediction
        predicted_label = class_labels[predicted_class_index]

    print(f"Predicted: {predicted_label} with confidence {confidence:.2f}")
    return predicted_label, confidence

# Function to upload result to Firebase Realtime Database
def upload_result_to_firebase(predicted_label):
    result = {
        'predicted_label': predicted_label,
        #'confidence': confidence,
        #'timestamp': datetime.now().isoformat()
    }
    db.reference('predictions').push(result)
    print("Uploaded result to Firebase")

if __name__ == "__main__":
    print("Ready to capture images. Press the button.")
    interpreter = load_tflite_model()

    try:
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False and debounce(button_pin):
                GPIO.output(led_pin, GPIO.HIGH)  # Turn on LED

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d_%H-%M-%S")
                output_directory = "/home/gwenzhang/Documents/photos/"
                output_file = f"{output_directory}photo_{timestamp}.jpg"

                capture_image(output_file)
                preprocessed_image = preprocess_image(output_file, (96, 96))  # Example input size
                results = run_inference(interpreter, preprocessed_image)
                predicted_label = interpret_results(results)

                # Upload result to Firebase
                upload_result_to_firebase(predicted_label)

                GPIO.output(led_pin, GPIO.LOW)  # Turn off LED
                time.sleep(2)  # Wait for 2 seconds between captures

    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()
