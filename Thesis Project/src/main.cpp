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

#define ECG_HZ 500 // ECG sampling rate
#define IMU_HZ 50  // IMU sampling rate
#define ECG_PERIOD_US (1000000 / ECG_HZ)
#define IMU_PERIOD_MS (1000 / IMU_HZ)


const uint8_t HEART_ACTIVITY_PIN = GPIO_NUM_0;
// Debounce parameters

DFRobot_BMP280_IIC Bmp(&Wire, DFRobot_BMP280_IIC::eSdoHigh); // Scan showed address 0x77
DFRobot_ADXL345_I2C ADXL345(&Wire,0x53);
DFRobot_ITG3200 Gyro(&Wire, 0x68);
DFRobot_QMC5883 Compass(&Wire, VCM5883L_ADDRESS); // Scan showed address 0x0C
DFRobot_FreeTenIMU FreeTenIMU(&ADXL345,&Gyro,&Compass,&Bmp);

// State for debounce
bool     lastPhysicalState = HIGH;  // what the pin actually read last time
bool     debouncedState   = HIGH;  // the “real” button state after debounce
unsigned long lastChangeTime = 0;  // when physical state last changed

unsigned long lastImuMs = 0;
uint32_t nextEcgSampleUs = 0;

// Data storage
int ACC_RAW[3];
float MAG_RAW[3];
// HeartSpeed heartSpeed(HEART_ACTIVITY_PIN);  NVM this only works on AVR platforms
volatile int g_lastBpm = 0;

static inline void PrintCsvPrefix(uint32_t timeUs, const char* src) {
  Serial.print(timeUs);
  Serial.print(",");
  Serial.print(src);
  Serial.print(",");
}

void mycb(uint8_t rawData, int value) {
  // Library calls this either raw or bpm depending on mode
  // We're using bpm mode, so rawData == 0, value = bpm
  if (!rawData) {
    g_lastBpm = value;
  }
}

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

  if (!FreeTenIMU.begin()) {
    Serial.println("FreeTenIMU init failed");
  }
  else {
    Serial.println("FreeTenIMU init success");
  }
  ADXL345.setRangeSetting(2); // Set the range to +/-2g
  ADXL345.setFullResBit(true); // Set to full resolution mode, 3.9mg/LSB

  // Heart rate sensor
  // heartSpeed.setCB(mycb);
  // heartSpeed.begin();
}

void loop() {
  // ECG @ 500 Hz 

  uint32_t nowUs = micros();
  if ((int32_t)(nowUs - nextEcgSampleUs) >= 0) {
    nextEcgSampleUs += ECG_PERIOD_US;

    int ecgRaw = analogRead(HEART_ACTIVITY_PIN); // 0..4095 on ESP32

    // timestamp, source=ECG, IMU fields empty, ecg_raw, hr_bpm blank
    PrintCsvPrefix(nowUs, "ECG");
    // 10 IMU/orientation fields: ax..head (leave empty)
    Serial.print(",,,,,,,,"); // 9 commas for 9 empty fields
    Serial.println(ecgRaw);      // ecg_raw
  }

  // IMU @ 50 Hz 

  uint32_t nowMs = millis();
  if (nowMs - lastImuMs >= IMU_PERIOD_MS) {
    lastImuMs = nowMs;

    // Read IMU
    // Read accelerometer
    ADXL345.readAccel(ACC_RAW);
    float ax = (int16_t)ACC_RAW[0] * 0.0039; // Convert to g
    float ay = (int16_t)ACC_RAW[1] * 0.0039;
    float az = (int16_t)ACC_RAW[2] * 0.0039;

    sEulAnalog_t sEul = FreeTenIMU.getEul();
    Gyro.readGyro(MAG_RAW);

    // timestamp, source=IMU
    uint32_t timeUs = micros();
    PrintCsvPrefix(timeUs, "IMU");
    // ax,ay,az
    Serial.printf("%.3f,%.3f,%.3f,", ax, ay, az);
    // gx,gy,gz
    Serial.printf("%.3f,%.3f,%.3f,", MAG_RAW[0], MAG_RAW[1], MAG_RAW[2]);
    // roll,pitch,head
    Serial.printf("%.3f,%.3f,%.3f", sEul.roll, sEul.pitch, sEul.head);
    Serial.println();
  }
}

