/*!
* @file imuShow.ino
* @brief Read the elevation, roll and yaw angle of the sensor through I2C interface, and print the read data on serial port
* @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
* @license     The MIT License (MIT)
* @author      PengKaixing(kaixing.peng@dfrobot.com)
* @version  V1.0.0
* @date  2022-3-4
* @url https://github.com/DFRobot/DFRobot_FreeTenIMU
*/

#include <Arduino.h>
#include <DFRobot_FreeTenIMU.h>

// const uint8_t BUTTON_PIN = A3;
const uint8_t HEART_ACTIVITY_PIN = GPIO_NUM_0;
// Debounce parameters
const unsigned long DEBOUNCE_DELAY = 50;  // ms

DFRobot_BMP280_IIC Bmp(&Wire, DFRobot_BMP280_IIC::eSdoHigh); // Scan showed address 0x77
DFRobot_ADXL345_I2C ADXL345(&Wire,0x53);
DFRobot_ITG3200 Gyro(&Wire, 0x68);
DFRobot_QMC5883 Compass(&Wire, VCM5883L_ADDRESS); // Scan showed address 0x0C
DFRobot_FreeTenIMU FreeTenIMU(&ADXL345,&Gyro,&Compass,&Bmp);

// State for debounce
bool     lastPhysicalState = HIGH;  // what the pin actually read last time
bool     debouncedState   = HIGH;  // the “real” button state after debounce
unsigned long lastChangeTime = 0;  // when physical state last changed

int ACC_RAW[3];
int MAG_RAW[3];


void setup() {
  Serial.begin(115200);
  Wire.begin(8, 9);
  Serial.println("Scanning...");
  for (byte addr = 1; addr < 127; addr++) {
    // Serial.printf(("Checking address 0x%02X ... "), addr);
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Found device at 0x");
      Serial.println(addr, HEX);
    }
  }
  Serial.println("Checking sensors one by one...");

  if (!ADXL345.begin()) {
    Serial.println("ADXL345 init failed");
  } else {
    Serial.println("ADXL345 init OK");
    Serial.println("Poering on ADXL345");
    ADXL345.powerOn();
  }

  // Gyro isn't working so skip for now.
  // if (!gyro.begin()) {
  //   Serial.println("ITG3200 init failed");
  // } else {
  //   Serial.println("ITG3200 init OK");
  // }

  if (!Compass.begin()) {
    Serial.println("QMC5883 init failed");
  } else {
    Serial.println("QMC5883 init OK");
  }

  if (!Bmp.begin()) {
    Serial.println("BMP280 init failed");
  } else {
    Serial.println("BMP280 init OK");
  }

  // FreeTunIMU doesn't work as gyro isn't working for some reason.
  // if (!FreeTenIMU.begin()) {
  //   Serial.println("FreeTenIMU init failed");
  // }
  // else {
  //   Serial.println("FreeTenIMU init success");
  // }
}

void loop() {
  // Read accelerometer
  ADXL345.readAccel(ACC_RAW);
  float ax = ACC_RAW[0] * 0.004; // Convert to g
  float ay = ACC_RAW[1] * 0.004;
  float az = ACC_RAW[2] * 0.004;

  // Print accelerometer data in csv format
  Serial.printf("%.3f,%.3f,%.3f\n", ax, ay, az);

}
