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
#include <DFRobot_FreeTenIMU.h>
#include <Wire.h>



DFRobot_BMP280_IIC bmp(&Wire, DFRobot_BMP280_IIC::eSdoLow);
DFRobot_ADXL345_I2C ADXL345(&Wire,0x53);
DFRobot_ITG3200 gyro(&Wire, 0x68);
DFRobot_QMC5883 compass(&Wire, /*I2C addr*/VCM5883L_ADDRESS);
DFRobot_FreeTenIMU FreeTenIMU(&ADXL345,&gyro,&compass,&bmp);

void setup() {
  Serial.begin(9600);
  Wire.begin(SDA, SCL);
  Wire.setClock(400000);   // optional: 400 kHz fast mode
  delay(10);

  if (FreeTenIMU.begin() == false) {
    Serial.println("IMU Initalisation Failed");
  } else {
    Serial.println("IMU Initalisation Succeeded");
  }

  //set the resolution to 12 bits (0-4095)
  analogReadResolution(12);
}

void loop() {
  // read the analog / millivolts value for pin 2:
  int analogValue = analogRead(2);
  
  // print out the values you read:
  Serial.printf("ADC analog value = %d\n", analogValue);
  
  sEulAnalog_t   sEul;
  sEul = FreeTenIMU.getEul();
  Serial.print("pitch:");
  Serial.print(sEul.pitch, 3);
  Serial.print(" ");
  Serial.print("roll:");
  Serial.print(sEul.roll, 3);
  Serial.print(" ");
  Serial.print("yaw:");
  Serial.print(sEul.head, 3);
  Serial.println(" ");
  delay(80);
}