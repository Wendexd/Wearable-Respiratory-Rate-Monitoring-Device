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
float MAG_RAW[3];


void setup() {
  Serial.begin(115200);
  Wire.begin(8, 9);
  pinMode(HEART_ACTIVITY_PIN, INPUT_PULLUP);
  Serial.println("Scanning...");
  for (byte addr = 1; addr < 127; addr++) {
    // Serial.printf(("Checking address 0x%02X ... "), addr);
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Found device at 0x");
      Serial.println(addr, HEX);
    }
  }

  Wire.beginTransmission(0x68);
  Wire.write(0x00);  // WHO_AM_I register
  Wire.endTransmission();
  Wire.requestFrom(0x68, 1);
  if (Wire.available()) {
    Serial.print("WHO_AM_I: ");
    Serial.println(Wire.read(), HEX);
  }

  // Serial.println("Checking sensors one by one...");

  // if (!ADXL345.begin()) {
  //   Serial.println("ADXL345 init failed");
  // } else {
  //   Serial.println("ADXL345 init OK");
  // }
  
  // // Gyro isn't working so skip for now.
  // if (!Gyro.begin()) {
  //   Serial.println("ITG3200 init failed");
  // } else {
  //   Serial.println("ITG3200 init OK");
  // }
  
  // if (!Compass.begin()) {
  //   Serial.println("QMC5883 init failed");
  // } else {
  //   Serial.println("QMC5883 init OK");
  // }
  
  // if (!Bmp.begin()) {
  //   Serial.println("BMP280 init failed");
  // } else {
  //   Serial.println("BMP280 init OK");
  // }
  
  
  // Serial.println("Powering on ADXL345");
  // ADXL345.powerOn();
  // FreeTunIMU doesn't work as gyro isn't working for some reason.
  if (!FreeTenIMU.begin()) {
    Serial.println("FreeTenIMU init failed");
  }
  else {
    Serial.println("FreeTenIMU init success");
  }
}

void loop() {
  // Read accelerometer
  ADXL345.readAccel(ACC_RAW);
  float ax = (int16_t)ACC_RAW[0] * 0.004; // Convert to g
  float ay = (int16_t)ACC_RAW[1] * 0.004;
  float az = (int16_t)ACC_RAW[2] * 0.004;

  sEulAnalog_t sEul = FreeTenIMU.getEul();
  int heartActivity = analogRead(HEART_ACTIVITY_PIN);
  Gyro.readGyro(MAG_RAW);

  // Print accelerometer data in csv format
  Serial.printf("%.3f,%.3f,%.3f,", ax, ay, az);
  // Print gyro data in csv format
  Serial.printf("%.3f,%.3f,%.3f,", MAG_RAW[0], MAG_RAW[1], MAG_RAW[2]);
  // Print roll, pitch, heading in csv format
  Serial.printf("%.3f,%.3f,%.3f,", sEul.roll, sEul.pitch, sEul.head);
  // Print heart activity
  Serial.println(heartActivity);

}

