#include <Arduino.h>
#include <Wire.h>
#include <HMC5883L.h>
#include <ITG3200.h>
#include <Adafruit_ADXL345_U.h>
#define LED 2
#define SDA_PIN 8
#define SCL_PIN 9

// Declare Sensor Objects
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
ITG3200 gyro;
HMC5883L compass;

// put function declarations here:
int myFunction(int, int);

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);

  Wire.begin(SDA_PIN, SCL_PIN);
  
  // Initialise IMU
  if (!accel.begin()) {
    Serial.println("ERROR: ADXL345 not detected");
    delay(10);

  }
  else {
    accel.setRange(ADXL345_RANGE_16_G);
  }

  gyro.initialize();

  compass = HMC5883L();

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  delay(500);
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}