/*!
 * @file DFRobot_ADXL345.h
 * @brief This is an library for ADXL345 Triaxial Acceleration Sensor
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author      PengKaixing(kaixing.peng@dfrobot.com)
 * @version  V2.0.0
 * @date  2022-02-22
 * @url https://github.com/DFRobot/DFRobot_ADXL345
 */
#include "DFRobot_ADXL345.h"

void DFRobot_ADXL345::powerOn(void)
{
  uint8_t data = 0;
  writeData(ADXL345_POWER_CTL, &data,1);
  data = 16;
  writeData(ADXL345_POWER_CTL, &data,1);
  data = 8;
  writeData(ADXL345_POWER_CTL, &data,1);
}

void DFRobot_ADXL345::readAccel(int* xyz)
{
  readAccel(xyz, xyz + 1, xyz + 2);
}

void DFRobot_ADXL345::readAccel(int *x, int *y, int *z)
{
  uint8_t _buff[6];
  readData(ADXL345_DATAX0, _buff,TO_READ);
  *x = (((int)_buff[1]) << 8) | _buff[0];
  *y = (((int)_buff[3]) << 8) | _buff[2];
  *z = (((int)_buff[5]) << 8) | _buff[4];
}

void DFRobot_ADXL345::setTapThreshold(int tapThreshold)
{
  tapThreshold = min(max(tapThreshold, 0), 255);
  uint8_t _b = (uint8_t)tapThreshold;
  writeData(ADXL345_THRESH_TAP, &_b,1);
}

int DFRobot_ADXL345::getTapThreshold(void)
{
  uint8_t _b;
  int status =readData(ADXL345_THRESH_TAP, &_b, 1);
  return int (_b);
}

void DFRobot_ADXL345::setTapDuration(int tapDuration)
{
  tapDuration = min(max(tapDuration,0),255);
  uint8_t _b = (uint8_t)tapDuration;
  writeData(ADXL345_DUR, &_b,1);
}

int DFRobot_ADXL345::getTapDuration(void)
{
  uint8_t _b;
  readData(ADXL345_DUR, &_b,1);
  return (int)_b;
}

void DFRobot_ADXL345::setDoubleTapLatency(int floatTapLatency)
{
  uint8_t _b = (uint8_t)floatTapLatency;
  writeData(ADXL345_LATENT, &_b,1);
}

int DFRobot_ADXL345::getDoubleTapLatency(void)
{
  uint8_t _b;
  readData(ADXL345_LATENT, &_b,1);
  return int (_b);
}

void DFRobot_ADXL345::setDoubleTapWindow(int floatTapWindow)
{
  floatTapWindow = min(max(floatTapWindow,0),255);
  uint8_t _b = (uint8_t)floatTapWindow;
  writeData(ADXL345_WINDOW, &_b,1);
}

int DFRobot_ADXL345::getDoubleTapWindow(void)
{
  uint8_t _b;
  readData(ADXL345_WINDOW,&_b,1);
  Serial.println(_b);
  return (int)_b;
}

void DFRobot_ADXL345::setActivityThreshold(int activityThreshold)
{
  activityThreshold = min(max(activityThreshold,0),255);
  uint8_t _b = (uint8_t)activityThreshold;
  writeData(ADXL345_THRESH_ACT, &_b,1);
}

int DFRobot_ADXL345::getActivityThreshold(void)
{
  uint8_t _b;
  readData(ADXL345_THRESH_ACT, &_b, 1);
  return (int)_b;
}

void DFRobot_ADXL345::setInactivityThreshold(int inactivityThreshold)
{
  inactivityThreshold = min(max(inactivityThreshold,0),255);
  uint8_t _b = (uint8_t)inactivityThreshold;
  writeData(ADXL345_THRESH_INACT, &_b, 1);
}

int DFRobot_ADXL345::getInactivityThreshold(void)
{
  uint8_t _b;
  readData(ADXL345_THRESH_INACT, &_b, 1);
  return (int)_b;
}

void DFRobot_ADXL345::setTimeInactivity(int timeInactivity)
{
  timeInactivity = min(max(timeInactivity,0),255);
  uint8_t _b = (uint8_t)timeInactivity;
  writeData(ADXL345_TIME_INACT, &_b, 1);
}

int DFRobot_ADXL345::getTimeInactivity(void)
{
  uint8_t _b;
  readData(ADXL345_TIME_INACT, &_b, 1);
  return (int)_b;
}

void DFRobot_ADXL345::setFreeFallThreshold(int freeFallthreshold)
{
  freeFallthreshold = min(max(freeFallthreshold, 0), 255);
  uint8_t _b = (uint8_t)freeFallthreshold;
  writeData(ADXL345_THRESH_FF, &_b, 1);
}

int DFRobot_ADXL345::getFreeFallThreshold(void)
{
  uint8_t _b;
  readData(ADXL345_THRESH_FF, &_b, 1);
  return (int)_b;
}

void DFRobot_ADXL345::setFreeFallDuration(int freeFallDuration)
{
  freeFallDuration = min(max(freeFallDuration, 0), 255);
  uint8_t _b = (uint8_t)freeFallDuration;
  writeData(ADXL345_TIME_FF, &_b, 1);
}

int DFRobot_ADXL345::getFreeFallDuration(void)
{
  uint8_t _b;
  readData(ADXL345_TIME_FF, &_b, 1);
  return (int)_b;
}

bool DFRobot_ADXL345::getRegisterBit(uint8_t regAdress, int bitPos)
{
  uint8_t _b;
  readData(regAdress,&_b,1);
  return ((_b >> bitPos) & 1);
}

void DFRobot_ADXL345::setRegisterBit(uint8_t regAdress, int bitPos, bool state)
{
  uint8_t _b;
  int status = readData(regAdress, &_b,1);
  if (state)
  {
    _b |= (1 << bitPos); // forces nth bit of _b to be 1.  all other bits left alone.
  }
  else
  {
    _b &= ~(1 << bitPos); // forces nth bit of _b to be 0.  all other bits left alone.
  }
  writeData(regAdress, &_b,1);
  readData(regAdress, &_b,1);
}

bool DFRobot_ADXL345::isActivityXEnabled(void)
{
  return getRegisterBit(ADXL345_ACT_INACT_CTL, 6);
}

bool DFRobot_ADXL345::isActivityYEnabled(void)
{
  return getRegisterBit(ADXL345_ACT_INACT_CTL, 5);
}

bool DFRobot_ADXL345::isActivityZEnabled(void)
{
  return getRegisterBit(ADXL345_ACT_INACT_CTL, 4);
}

bool DFRobot_ADXL345::isInactivityXEnabled(void)
{
  return getRegisterBit(ADXL345_ACT_INACT_CTL, 2);
}

bool DFRobot_ADXL345::isInactivityYEnabled(void)
{
  return getRegisterBit(ADXL345_ACT_INACT_CTL, 1);
}

bool DFRobot_ADXL345::isInactivityZEnabled(void)
{
  return getRegisterBit(ADXL345_ACT_INACT_CTL, 0);
}

bool DFRobot_ADXL345::isTapDetectionOnX(void)
{
  return getRegisterBit(ADXL345_TAP_AXES, 2);
}

void DFRobot_ADXL345::setTapDetectionOnX(bool state)
{
  setRegisterBit(ADXL345_TAP_AXES, 2, state);
}

bool DFRobot_ADXL345::isTapDetectionOnY(void)
{
  return getRegisterBit(ADXL345_TAP_AXES, 2);
}

void DFRobot_ADXL345::setTapDetectionOnY(bool state)
{
  setRegisterBit(ADXL345_TAP_AXES, 2, state);
}

bool DFRobot_ADXL345::isTapDetectionOnZ(void)
{
  return getRegisterBit(ADXL345_TAP_AXES, 2);
}

void DFRobot_ADXL345::setTapDetectionOnZ(bool state)
{
  setRegisterBit(ADXL345_TAP_AXES, 2, state);
}

void DFRobot_ADXL345::setActivityX(bool state)
{
  setRegisterBit(ADXL345_ACT_INACT_CTL, 6, state);
}

void DFRobot_ADXL345::setActivityY(bool state)
{
  setRegisterBit(ADXL345_ACT_INACT_CTL, 5, state);
}

void DFRobot_ADXL345::setActivityZ(bool state)
{
  setRegisterBit(ADXL345_ACT_INACT_CTL, 4, state);
}

void DFRobot_ADXL345::setInactivityX(bool state)
{
  setRegisterBit(ADXL345_ACT_INACT_CTL, 2, state);
}

void DFRobot_ADXL345::setInactivityY(bool state)
{
  setRegisterBit(ADXL345_ACT_INACT_CTL, 1, state);
}

void DFRobot_ADXL345::setInactivityZ(bool state)
{
  setRegisterBit(ADXL345_ACT_INACT_CTL, 0, state);
}

bool DFRobot_ADXL345::isActivitySourceOnX(void)
{
  return getRegisterBit(ADXL345_ACT_TAP_STATUS, 6);
}

bool DFRobot_ADXL345::isActivitySourceOnY(void)
{
  return getRegisterBit(ADXL345_ACT_TAP_STATUS, 5);
}

bool DFRobot_ADXL345::isActivitySourceOnZ(void)
{
  return getRegisterBit(ADXL345_ACT_TAP_STATUS, 4);
}

bool DFRobot_ADXL345::isTapSourceOnX(void)
{
  return getRegisterBit(ADXL345_ACT_TAP_STATUS, 2);
}

bool DFRobot_ADXL345::isTapSourceOnY(void)
{
  return getRegisterBit(ADXL345_ACT_TAP_STATUS, 1);
}

bool DFRobot_ADXL345::isTapSourceOnZ(void)
{
  return getRegisterBit(ADXL345_ACT_TAP_STATUS, 0);
}

bool DFRobot_ADXL345::isAsleep(void)
{
  return getRegisterBit(ADXL345_ACT_TAP_STATUS, 3);
}

bool DFRobot_ADXL345::isLowPower(void)
{
  return getRegisterBit(ADXL345_BW_RATE, 4);
}

void DFRobot_ADXL345::setLowPower(bool state)
{
  setRegisterBit(ADXL345_BW_RATE, 4, state);
}

float DFRobot_ADXL345::getRate(void)
{
  uint8_t _b;
  readData(ADXL345_BW_RATE, &_b, 1);
  _b &= 0x0f;
  return (pow(2, ((int)_b) - 6)) * 6.25;
}

void DFRobot_ADXL345::setRate(float rate)
{
  uint8_t _b, _s;
  int v = (int)(rate / 6.25);
  int r = 0;
  while (v >>= 1)
  {
    r++;
  }
  if (r <= 9)
  {
    readData(ADXL345_BW_RATE, &_b, 1);
    _s = (uint8_t)(r + 6) | (_b & 0xf0);
    writeData(ADXL345_BW_RATE, &_s, 1);
  }
}

void DFRobot_ADXL345::setBwcode(uint8_t bw_code)
{
  if ((bw_code < ADXL345_BW_3) || (bw_code > ADXL345_BW_1600))
  {
    status = false;
    error_code = ADXL345_BAD_ARG;
  }
  else
  {
    writeData(ADXL345_BW_RATE, &bw_code,1);
  }
}

uint8_t DFRobot_ADXL345::getBwcode(void)
{
  uint8_t bw_code;
  readData(ADXL345_BW_RATE,&bw_code,1);
  return bw_code;
}

uint8_t DFRobot_ADXL345::getInterruptSource(void)
{
  uint8_t _b;
  readData(ADXL345_INT_SOURCE, &_b,1);
  return _b;
}

bool DFRobot_ADXL345::getInterruptMapping(uint8_t interruptBit)
{
  return getRegisterBit(ADXL345_INT_MAP, interruptBit);
}

void DFRobot_ADXL345::setInterruptMapping(uint8_t interruptBit, bool interruptPin)
{
  setRegisterBit(ADXL345_INT_MAP, interruptBit, interruptPin);
}

bool DFRobot_ADXL345::isInterruptEnabled(uint8_t interruptBit)
{
  return getRegisterBit(ADXL345_INT_ENABLE, interruptBit);
}

void DFRobot_ADXL345::setInterrupt(uint8_t interruptBit, bool state)
{
  setRegisterBit(ADXL345_INT_ENABLE, interruptBit, state);
}

void DFRobot_ADXL345::singleTapInt(bool status)
{
  if (status)
  {
    setInterrupt(ADXL345_INT_SINGLE_TAP_BIT, 1);
  }
  else
  {
    setInterrupt(ADXL345_INT_SINGLE_TAP_BIT, 0);
  }
}
void DFRobot_ADXL345::doubleTapInt(bool status)
{
  if (status)
  {
    setInterrupt(ADXL345_INT_DOUBLE_TAP_BIT, 1);
  }
  else
  {
    setInterrupt(ADXL345_INT_DOUBLE_TAP_BIT, 0);
  }
}
void DFRobot_ADXL345::freeFallInt(bool status)
{
  if (status)
  {
    setInterrupt(ADXL345_INT_FREE_FALL_BIT, 1);
  }
  else
  {
    setInterrupt(ADXL345_INT_FREE_FALL_BIT, 0);
  }
}
void DFRobot_ADXL345::activityInt(bool status)
{
  if (status)
  {
    setInterrupt(ADXL345_INT_ACTIVITY_BIT, 1);
  }
  else
  {
    setInterrupt(ADXL345_INT_ACTIVITY_BIT, 0);
  }
}

void DFRobot_ADXL345::inactivityInt(bool status)
{
  if (status)
  {
    setInterrupt(ADXL345_INT_INACTIVITY_BIT, 1);
  }
  else
  {
    setInterrupt(ADXL345_INT_INACTIVITY_BIT, 0);
  }
}

void DFRobot_ADXL345::setRangeSetting(int val)
{
  uint8_t _s, _b;
  switch (val)
  {
    case 2:
      _s = B00000000;
      break;
    case 4:
      _s = B00000001;
      break;
    case 8:
      _s = B00000010;
      break;
    case 16:
      _s = B00000011;
      break;
    default:
      _s = B00000000;
  }
  readData(ADXL345_DATA_FORMAT, &_b,1);
  _s |= (_b & B11101100);
  writeData(ADXL345_DATA_FORMAT, &_s,1);
}

bool DFRobot_ADXL345::getInterruptLevelBit(void)
{
  return getRegisterBit(ADXL345_DATA_FORMAT, 5);
}

void DFRobot_ADXL345::setInterruptLevelBit(bool interruptLevelBit)
{
  setRegisterBit(ADXL345_DATA_FORMAT, 5, interruptLevelBit);
}

bool DFRobot_ADXL345::getFullResBit(void)
{
  return getRegisterBit(ADXL345_DATA_FORMAT, 3);
}

void DFRobot_ADXL345::setFullResBit(bool fullResBit)
{
  setRegisterBit(ADXL345_DATA_FORMAT, 3, fullResBit);
}

bool DFRobot_ADXL345::getJustifyBit(void)
{
  return getRegisterBit(ADXL345_DATA_FORMAT, 2);
}

void DFRobot_ADXL345::setJustifyBit(bool justifyBit)
{
  setRegisterBit(ADXL345_DATA_FORMAT, 2, justifyBit);
}

void DFRobot_ADXL345::RPCalculate(int*data_buf){
  double x_Buff = float(data_buf[0]);
  double y_Buff = float(data_buf[1]);
  double z_Buff = float(data_buf[2]);
  RP.roll =  atan2(y_Buff , z_Buff) * 57.3;
  RP.pitch = atan2((- x_Buff) , sqrt(y_Buff * y_Buff + z_Buff * z_Buff)) * 57.3;
}

bool DFRobot_ADXL345::triggered(byte interrupts, int mask)
{
  return ((interrupts >> mask) & 1);
}

DFRobot_ADXL345_I2C::DFRobot_ADXL345_I2C(TwoWire *pWire, uint8_t I2C_addr)
{
  this->_pWire = pWire;
  this->_I2C_addr = I2C_addr;
}

bool DFRobot_ADXL345_I2C::begin(void)
{
  _pWire->begin();
  _pWire->beginTransmission(this->_I2C_addr);
  int status = _pWire->endTransmission();
  if (0 == status)
  {
    return true;
  }
  else
  {
    return false;
  }
}

void DFRobot_ADXL345_I2C::writeData(uint8_t reg, void *pdata, uint8_t len)
{
  uint8_t *data = (uint8_t *)pdata;
  _pWire->beginTransmission(this->_I2C_addr);
  _pWire->write(reg);
  for (uint8_t i = 0; i < len; i++)
  {
    _pWire->write(data[i]);
  }
  _pWire->endTransmission();
}

int16_t DFRobot_ADXL345_I2C::readData(uint8_t reg, uint8_t *data, uint8_t len)
{
  int i = 0;
  _pWire->beginTransmission(this->_I2C_addr);
  _pWire->write(reg);
  int status = _pWire->endTransmission();
  if (status != 0)
  {
    return -1;
  }
  _pWire->requestFrom((uint8_t)this->_I2C_addr, (uint8_t)len);
  while (_pWire->available())
  {
    data[i++] = _pWire->read();
  }
  return len;
}

DFRobot_ADXL345_SPI::DFRobot_ADXL345_SPI(SPIClass *pSpi, uint8_t csPin)
{
  _pSpi = pSpi;
  _csPin = csPin;
}

bool DFRobot_ADXL345_SPI::begin(void)
{
  _pSpi->begin();
  _pSpi->setDataMode(SPI_MODE3);
  pinMode(_csPin, OUTPUT);
  digitalWrite(_csPin, HIGH);
  return true;
}

void DFRobot_ADXL345_SPI::writeData(uint8_t reg, void *pdata, uint8_t len)
{
  uint8_t *_pBuf = (uint8_t *)pdata;
  _pSpi->beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE3));
  digitalWrite(_csPin, 0);
  _pSpi->transfer(reg);
  while (len--)
  {
    _pSpi->transfer(*_pBuf);
    _pBuf++;
  }
  digitalWrite(_csPin, 1);
  SPI.endTransaction();
}

int16_t DFRobot_ADXL345_SPI::readData(uint8_t reg, uint8_t *data, uint8_t len)
{
  reg = 0x80 | reg;
  if (len > 1)
  {
    reg = reg | 0x40;
  }
  uint8_t *_pBuf = (uint8_t *)data;
  uint8_t count = 0;
  digitalWrite(_csPin, 0);
  _pSpi->transfer(reg);
  while (len--)
  {
    *_pBuf = SPI.transfer(0x00);
    _pBuf++;
    count++;
  }
  digitalWrite(_csPin, 1);
  return count;
}
