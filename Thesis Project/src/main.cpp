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

const uint8_t BUTTON_PIN = A3;
const uint8_t HEART_ACTIVITY_PIN = A0;
// Debounce parameters
const unsigned long DEBOUNCE_DELAY = 50;  // ms

DFRobot_BMP280_IIC bmp(&Wire, DFRobot_BMP280_IIC::eSdoLow);
DFRobot_ADXL345_I2C ADXL345(&Wire,0x53);
DFRobot_ITG3200 gyro(&Wire, 0x68);
DFRobot_QMC5883 compass(&Wire, /*I2C addr*/VCM5883L_ADDRESS);
DFRobot_FreeTenIMU FreeTenIMU(&ADXL345,&gyro,&compass,&bmp);

// State for debounce
bool     lastPhysicalState = HIGH;  // what the pin actually read last time
bool     debouncedState   = HIGH;  // the “real” button state after debounce
unsigned long lastChangeTime = 0;  // when physical state last changed

void setup() {
  Serial.begin(115200);
  FreeTenIMU.begin();
  pinMode(BUTTON_PIN, INPUT);
}

void loop() {
  sEulAnalog_t   sEul;
  unsigned long t = millis();
  // 1) Read the button (LOW = pressed, HIGH = released)
  // bool currentReading = (digitalRead(BUTTON_PIN) == LOW);

  //   // 2) If it’s different from last time, reset the timer
  // if (currentReading != lastPhysicalState) {
  //   lastChangeTime = millis();
  //   lastPhysicalState = currentReading;
  // }

  // // 3) If it’s been stable longer than the debounce delay…
  // if ((millis() - lastChangeTime) > DEBOUNCE_DELAY) {
  //   // …and if it’s actually changed the debounced state, update it
  //   if (currentReading != debouncedState) {
  //     debouncedState = currentReading;
  //   }
  // }

  bool pressed = (digitalRead(BUTTON_PIN) == HIGH);

  int heartActivity = analogRead(HEART_ACTIVITY_PIN);
  int accRaw[3];
  ADXL345.readAccel(accRaw);
  float x_g = accRaw[0] * 0.004;
  float y_g = accRaw[1] * 0.004;
  float z_g = accRaw[2] * 0.004;
  sEul = FreeTenIMU.getEul();
  float gyro_dps[3];
  gyro.readGyro(gyro_dps);
  // Serial.print("Accel (counts): ");
  // Serial.print("X="); Serial.print(x_g);
  // Serial.print("  Y="); Serial.print(y_g);
  // Serial.print("  Z="); Serial.print(z_g);
  // gyro.readGyro(gyro_dps); 
  // Serial.print("\tGyro (°/s): X="); Serial.print(gyro_dps[0], 2);
  // Serial.print(" Y=");          Serial.print(gyro_dps[1], 2);
  // Serial.print(" Z=");          Serial.print(gyro_dps[2], 2);
  // Serial.print("\tpitch:");
  // Serial.print(sEul.pitch, 3);
  // Serial.print(" ");
  // Serial.print("roll:");
  // Serial.print(sEul.roll, 3);
  // Serial.print(" ");
  // Serial.print("yaw:");
  // Serial.print(sEul.head, 3);
  // Serial.print(" ");
  // Serial.print("\t Button: ");
  // Serial.print(pressed);
  // Serial.print("\t Heart Activity = ");
  // Serial.println(heartActivity);

  // CSV Print
  Serial.print(t);             Serial.print(',');
  Serial.print(x_g, 3);         Serial.print(',');
  Serial.print(y_g, 3);         Serial.print(',');
  Serial.print(z_g, 3);         Serial.print(',');
  Serial.print(gyro_dps[0], 2);         Serial.print(',');
  Serial.print(gyro_dps[1], 2);         Serial.print(',');
  Serial.print(gyro_dps[2], 2);         Serial.print(',');
  Serial.print(sEul.pitch, 3);      Serial.print(',');
  Serial.print(sEul.roll,  3);      Serial.print(',');
  Serial.print(sEul.head,   3);      Serial.print(',');
  Serial.print(pressed?1:0);   Serial.print(',');
  Serial.println(heartActivity);
  delay(10);
}