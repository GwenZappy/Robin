#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Stepper.h>
#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>

// Define pin numbers
const int BUTTON_PIN = D10;
const int STEPPER_PIN1 = D2;
const int STEPPER_PIN2 = D3;
const int STEPPER_PIN3 = D1;
const int STEPPER_PIN4 = D0;
const int NEOPIXEL_PIN = D6;

// Firebase initialization
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// Wi-Fi credentials
//const char* ssid = "UW MPSK";
//const char* password = "@$j#j46V_,";

// Wi-Fi credentials
const char* ssid = "D322wifi";
const char* password = "D322808118";

// Stepper motor setup
#define STEPS 315 // Adjust this to your stepper's specific step count
Stepper myStepper(STEPS, STEPPER_PIN1, STEPPER_PIN2, STEPPER_PIN3, STEPPER_PIN4); // Initialize stepper with pins
const int positionA = STEPS / 3; // Compost
const int positionB = STEPS / 3 * 2; // Neutral
const int positionC = STEPS; // Trash, assuming a full rotation or adjust accordingly
int currentPosition = positionB; // Assume starting at Neutral position

// NeoPixel setup
#define NUM_PIXELS 4 // Define the number of NeoPixels
Adafruit_NeoPixel pixels(NUM_PIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

// Track previous predicted label
String previousPredictedLabel = "";

// Debounce variables
const long debounceDelay = 200; // the debounce time; increase if the output flickers
volatile long lastDebounceTime = 0; // the last time the output pin was toggled

void buttonInterruptHandler() {
  long currentTime = millis();
  // If interrupts come faster than debounceDelay, assume it's a bounce and ignore
  if ((currentTime - lastDebounceTime) > debounceDelay) {
    // Update the lastDebounceTime with the current time
    lastDebounceTime = currentTime;

    // Button action here
    Serial.println("Button pressed. Entering deep sleep mode.");
    esp_deep_sleep_start();
  }
}

void controlDevices(String predictedLabel) {
  // Control the NeoPixel based on the predicted label
  if (predictedLabel == "Compost Plate") {
    pixels.setPixelColor(0, pixels.Color(0, 255, 0)); // Green
  } else if (predictedLabel == "Trash Plate") {
    pixels.setPixelColor(0, pixels.Color(0, 0, 255)); // Blue
  } else if (predictedLabel == "Uncertain Plate") {
    pixels.setPixelColor(0, pixels.Color(125, 100, 100)); // White
    Serial.println("LED color set to white for Uncertain Plate");
  } else {
    pixels.setPixelColor(0, pixels.Color(125, 100, 100)); // White (default color)
    Serial.println("LED color set to white (default)");
  }
  pixels.show();

  // Control the stepper motor based on the predicted label
  int targetPosition;
  if (predictedLabel == "Compost Plate") {
    targetPosition = positionA; // Move to position A (Compost)
  } else if (predictedLabel == "Trash Plate") {
    targetPosition = positionC; // Move to position C (Trash)
  } else {
    targetPosition = positionB; // Move to position B (Neutral or Uncertain)
  }

  // Calculate steps to target position and move
  int stepsToTarget = targetPosition - currentPosition;
  myStepper.step(stepsToTarget);
  currentPosition = targetPosition; // Update the current position

  // Debug output to Serial Monitor
  Serial.print("Moving to ");
  Serial.println(predictedLabel);

  delay(2000); // Delay to simulate time between movements
}

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected with IP: ");
  Serial.println(WiFi.localIP());

  // Set up Firebase with your project details
  config.api_key = "AIzaSyCjn26aDe-OWu_9jFWxY9ZtTxvHa5QGiLs";
  config.database_url = "https://robin-3d81f-default-rtdb.firebaseio.com";
  // Authenticate with email and password
  auth.user.email = "test@example.com";
  auth.user.password = "123456";

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // Initialize the stepper motor
  myStepper.setSpeed(100); // Set the speed

  // Initialize the NeoPixel
  pixels.begin();
  pixels.setPixelColor(0, pixels.Color(125, 100, 100)); // Set to Uncertain color
  pixels.show();

  // Initialize BUTTON_PIN as an input with an internal pull-up resistor
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Attach interrupt for the button with debounce handler
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonInterruptHandler, FALLING);

  // Move the stepper motor to the "Uncertain" position
  myStepper.step(positionB - currentPosition);
  currentPosition = positionB;
}

void loop() {
  if (Firebase.ready() && WiFi.status() == WL_CONNECTED) {
    // Get the latest predicted label
    if (Firebase.getString(fbdo, "/latestPrediction")) {
      String predictedLabel = fbdo.stringData();
      // Check if the new predicted label is different from the previous one
      if (predictedLabel != previousPredictedLabel) {
        previousPredictedLabel = predictedLabel;
        Serial.print("Latest predicted label: ");
        Serial.println(predictedLabel);

        // Control devices based on the predicted label
        controlDevices(predictedLabel);
      }
    } else {
      Serial.println("Failed to get data from Firebase");
    }
  } else {
    Serial.println("Firebase not ready or Wi-Fi not connected.");
  }
  delay(1000); // Wait for a second before next attempt
}
