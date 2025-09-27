/*!
 * @file getGyroscopedata.ino
 * @brief This is a test routine that can be used to obtain gyro data
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author PengKaixing(kaixing.peng@dfrobot.com)
 * @version  V2.0.0
 * @date  2022-2-28
 * @url https://github.com/DFRobot/DFRobot_ITG3200
 */

#include <DFRobot_ITG3200.h>

#define I2C_ADDR 0x68
DFRobot_ITG3200 gyro = DFRobot_ITG3200(&Wire, I2C_ADDR);
float xyz[3], temperature;

void setup(void)
{
  Serial.begin(9600);
  gyro.begin();
  gyro.reset();
  /**
   * @brief set gyro sampling rate
   * @n     Sampling rate = 1kHz / (7 + 1) = 125Hz
   */
  // gyro.setSamplerateDiv(/*Sample rate divider*/7);
  /**
   * @brief get gyro sampling rate
   */
  // gyro.getSamplerateDiv();

  /**
   * @brief set the interrupt pin level when an interrupt is triggered
   */
  // gyro.setIntlogicLvl(false);
  /**
   * @brief Check if the interrupt pin is at low level when an interrupt is triggered
   */
  // gyro.isIntactiveOnlow();

  /**
   * @brief set interrupt pin status
   * @n     OPEN_DRAIN
   * @n     PUSH_PULL 
   */
  // gyro.setIntdriveType(OPEN_DRAIN);
  /**
   * @brief whether the interrupt pin is open drain output
   */
  // gyro.isIntopenDrain();

  Serial.print("zeroCalibrating...");
  gyro.zeroCalibrate(2500, 2);
  Serial.println("done.");
  showall();
  delay(5000);
}

void loop(void)
{
  while (gyro.isRawdataReady())
  {
    gyro.readGyro(xyz);
    Serial.print("X:");
    Serial.print(xyz[0]);
    Serial.print("  Y:");
    Serial.print(xyz[1]);
    Serial.print("  Z:");
    Serial.println(xyz[2]);
  }
}

void showall(void)
{
  Serial.println("Current ITG3200 settings");
  Serial.println("==========================================================");
  Serial.print("Sample rate divider (Hz)        = ");
  if (gyro.getFilterBW() == BW256_SR8)
    Serial.println(8000 / (gyro.getSamplerateDiv() + 1), DEC);
  else
    Serial.println(1000 / (gyro.getSamplerateDiv() + 1), DEC);
  Serial.print("full scale range                = ");
  if (gyro.getFSrange() == RANGE2000)
    Serial.println("+-2000 deg/sec");
  else
    Serial.println("reserved");
  Serial.print("low pass filter BW              = ");
  switch (gyro.getFilterBW())
  {
    case BW256_SR8:
      Serial.println("256Hz LowPassFilter BW/ 8Khz Sample Rate");
      break;
    case BW188_SR1:
      Serial.println("188Hz LowPassFilter BW/ 1Khz Sample Rate");
      break;
    case BW098_SR1:
      Serial.println("98Hz LowPassFilter BW/ 1Khz Sample Rate");
      break;
    case BW042_SR1:
      Serial.println("42Hz LowPassFilter BW/ 1Khz Sample Rate");
      break;
    case BW020_SR1:
      Serial.println("20Hz LowPassFilter BW/ 1Khz Sample Rate");
      break;
    case BW010_SR1:
      Serial.println("10Hz LowPassFilter BW/ 1Khz Sample Rate");
      break;
    case BW005_SR1:
      Serial.println("5Hz LowPassFilter BW/ 1Khz Sample Rate");
      break;
  }
  Serial.print("Logic level for INT output pin  = ");
  if (gyro.isIntactiveOnlow())
    Serial.println("Active on Low");
  else
    Serial.println("Active on High");

  Serial.print("INT drive type                  = ");
  if (gyro.isIntopenDrain())
    Serial.println("Open Drain");
  else
    Serial.println("Push-Pull");

  Serial.print("INT latch mode                  = ");
  if (gyro.isLatchuntilCleared())
    Serial.println("Latch until interrupt is cleared");
  else
    Serial.println("50us pulse");

  Serial.print("INT latch clear mode            = ");
  if (gyro.isAnyregClrmode())
    Serial.println("Any register read");
  else
    Serial.println("Status register read only");

  Serial.print("ITGReady trigger status         = ");
  if (gyro.isItgreadyOn())
    Serial.println("High/Set");
  else
    Serial.println("Low/Clear");

  Serial.print("RawDataReady trigger status     = ");
  if (gyro.isRawdataReady())
    Serial.println("High/Set");
  else
    Serial.println("Low/Clear");

  Serial.print("Temperature (Celsius)           = ");
  gyro.readTemp(&temperature);
  Serial.println(temperature);

  Serial.print("Power mode                      = ");
  gyro.setPowermode(NORMAL);
  if (gyro.isLowpower() == STANDBY)
    Serial.println("Low power (sleep)");
  else
    Serial.println("Normal");

  Serial.print("Xgyro status                    = ");
  if (gyro.isXgyroStandby() == NORMAL)
    Serial.println("Normal");
  else
    Serial.println("StandBy");

  Serial.print("Ygyro status                    = ");
  if (gyro.isYgyroStandby() == NORMAL)
    Serial.println("Normal");
  else
    Serial.println("StandBy");

  Serial.print("Zgyro status                    = ");
  if (gyro.isZgyroStandby() == NORMAL)
    Serial.println("Normal");
  else
    Serial.println("StandBy");
    
  Serial.print("Clock source                    = ");
  switch (gyro.getClocksource())
  {
    case INTERNALOSC:
      Serial.println("Internal oscillator");
      break;
    case PLL_XGYRO_REF:
      Serial.println("PLL with X Gyro reference");
      break;
    case PLL_YGYRO_REF:
      Serial.println("PLL with Y Gyro reference");
      break;
    case PLL_ZGYRO_REF:
      Serial.println("PLL with Z Gyro reference");
      break;
    case PLL_EXTERNAL32:
      Serial.println("PLL with external 32.768kHz reference");
      break;
    case PLL_EXTERNAL19:
      Serial.println("PLL with external 19.2MHz reference");
      break;
  }
  Serial.print("X offset (raw)                  = ");
  Serial.println(gyro.offsets[0]);
  Serial.print("Y offset (raw)                  = ");
  Serial.println(gyro.offsets[1]);
  Serial.print("Z offset (raw)                  = ");
  Serial.println(gyro.offsets[2]);
}
