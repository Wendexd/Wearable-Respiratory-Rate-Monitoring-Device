/*!
 * @file DFRobot_ITG3200.cpp
 * @brief A gyro sensor library
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author PengKaixing(kaixing.peng@dfrobot.com)
 * @version  V2.0.0
 * @date  2022-2-28
 * @url https://github.com/DFRobot/DFRobot_ITG3200
 */

#include "DFRobot_ITG3200.h"
uint8_t w_data;

DFRobot_ITG3200::DFRobot_ITG3200(TwoWire *pWire, uint8_t I2C_addr)
{
  this->_pWire = pWire;
  this->_I2C_addr = I2C_addr;
  setGains(1.0, 1.0, 1.0);
  setOffsets(0.0, 0.0, 0.0);
  setRevpolarity(0, 0, 0);
}

void DFRobot_ITG3200::setGains(float _Xgain, float _Ygain, float _Zgain)
{
  gains[0] = _Xgain;
  gains[1] = _Ygain;
  gains[2] = _Zgain;
}

void DFRobot_ITG3200::setOffsets(int _Xoffset, int _Yoffset, int _Zoffset)
{
  offsets[0] = _Xoffset;
  offsets[1] = _Yoffset;
  offsets[2] = _Zoffset;
}

void DFRobot_ITG3200::setRevpolarity(bool _Xpol, bool _Ypol, bool _Zpol)
{
  polarities[0] = _Xpol ? -1 : 1;
  polarities[1] = _Ypol ? -1 : 1;
  polarities[2] = _Zpol ? -1 : 1;
}

bool DFRobot_ITG3200::begin(uint8_t _SRateDiv, uint8_t _Range, uint8_t _filterBW, uint8_t _ClockSrc, bool _ITGReady, bool _INTRawDataReady)
{
  _pWire->begin();
  setSamplerateDiv(_SRateDiv);
  setFSrange(_Range);
  setFilterBW(_filterBW);
  setClocksource(_ClockSrc);
  setItgready(_ITGReady);
  setRawdataReady(_INTRawDataReady);
  delay(GYROSTART_UP_DELAY);
}

void DFRobot_ITG3200::setFSrange(uint8_t _Range)
{
  readData(DLPF_FS, &_buff[0],1);
  w_data = ((_buff[0] & ~DLPFFS_FS_SEL) | (_Range << 3));
  writeData(DLPF_FS, &w_data,1);
}

uint8_t DFRobot_ITG3200::getFilterBW(void)
{
  readData(DLPF_FS, &_buff[0],1);
  return (_buff[0] & DLPFFS_DLPF_CFG);
}

void DFRobot_ITG3200::setFilterBW(uint8_t _BW)
{
  readData(DLPF_FS,&_buff[0],1);
  w_data = ((_buff[0] & ~DLPFFS_DLPF_CFG) | _BW);
  writeData(DLPF_FS, &w_data,1);
}

void DFRobot_ITG3200::setSamplerateDiv(uint8_t _SampleRate)
{
  writeData(SMPLRT_DIV, &_SampleRate,1);
}

uint8_t DFRobot_ITG3200::getSamplerateDiv(void)
{
  readData(SMPLRT_DIV,&_buff[0],1);
  return _buff[0];
}

uint8_t DFRobot_ITG3200::getFSrange(void)
{
  readData(DLPF_FS, &_buff[0],1);
  return ((_buff[0] & DLPFFS_FS_SEL) >> 3);
}

void DFRobot_ITG3200::setIntlogicLvl(bool _State)
{
  readData(INT_CFG,&_buff[0],1);
  w_data = ((_buff[0] & ~INTCFG_ACTL) | (_State << 7));
  writeData(INT_CFG, &w_data, 1);
}

bool DFRobot_ITG3200::isIntactiveOnlow(void)
{
  readData(INT_CFG, &_buff[0], 1);
  return ((_buff[0] & INTCFG_ACTL) >> 7);
}

void DFRobot_ITG3200::setIntdriveType(bool _State)
{
  readData(INT_CFG,&_buff[0],1);
  w_data = ((_buff[0] & ~INTCFG_OPEN) | _State << 6);
  writeData(INT_CFG, &w_data, 1);
}

bool DFRobot_ITG3200::isIntopenDrain(void)
{
  readData(INT_CFG, &_buff[0],1);
  return ((_buff[0] & INTCFG_LATCH_INT_EN) >> 5);
}

bool DFRobot_ITG3200::isLatchuntilCleared(void)
{
  readData(INT_CFG, &_buff[0],1);
  return ((_buff[0] & INTCFG_LATCH_INT_EN) >> 5);
}

bool DFRobot_ITG3200::isAnyregClrmode(void)
{
  readData(INT_CFG, &_buff[0], 1);
  return ((_buff[0] & INTCFG_INT_ANYRD_2CLEAR) >> 4);
}

void DFRobot_ITG3200::setItgready(bool _State)
{
  readData(INT_CFG, &_buff[0],1);
  w_data = ((_buff[0] & ~INTCFG_ITG_RDY_EN) | _State << 2);
  writeData(INT_CFG, &w_data,1);
}

bool DFRobot_ITG3200::isItgreadyOn(void)
{
  readData(INT_CFG, &_buff[0], 1);
  return ((_buff[0] & INTCFG_ITG_RDY_EN) >> 2);
}

void DFRobot_ITG3200::setRawdataReady(bool _State)
{
  readData(INT_CFG, &_buff[0],1);
  w_data = ((_buff[0] & ~INTCFG_RAW_RDY_EN) | _State);
  writeData(INT_CFG, &w_data,1);
}

bool DFRobot_ITG3200::isRawdataReadyon(void)
{
  readData(INT_CFG, &_buff[0],1);
  return (_buff[0] & INTCFG_RAW_RDY_EN);
}

bool DFRobot_ITG3200::isItgready(void)
{
  readData(INT_STATUS, &_buff[0],1);
  return ((_buff[0] & INTSTATUS_ITG_RDY) >> 2);
}

bool DFRobot_ITG3200::isRawdataReady(void)
{
  readData(INT_STATUS, &_buff[0], 1);
  return (_buff[0] & INTSTATUS_RAW_DATA_RDY);
}

void DFRobot_ITG3200::readTemp(float *_Temp)
{
  readData(TEMP_OUT, _buff, 2);
  *_Temp = 35 + (((_buff[0] << 8) | _buff[1]) + 13200) / 280.0;
}

void DFRobot_ITG3200::readGyroraw(int *_GyroX, int *_GyroY, int *_GyroZ)
{
  readData(GYRO_XOUT, _buff, 6);
  *_GyroX = ((_buff[0] << 8) | _buff[1]);
  *_GyroY = ((_buff[2] << 8) | _buff[3]);
  *_GyroZ = ((_buff[4] << 8) | _buff[5]);
}

void DFRobot_ITG3200::readGyroraw(int *_GyroXYZ)
{
  readGyroraw(_GyroXYZ, _GyroXYZ + 1, _GyroXYZ + 2);
}

void DFRobot_ITG3200::zeroCalibrate(unsigned int totSamples, unsigned int sampleDelayMS)
{
  int xyz[3];
  float tmpOffsets[] = {0, 0, 0};
  for (int i = 0; i < totSamples; i++)
  {
    delay(sampleDelayMS);
    readGyroraw(xyz);
    tmpOffsets[0] += xyz[0];
    tmpOffsets[1] += xyz[1];
    tmpOffsets[2] += xyz[2];
  }
  setOffsets(-tmpOffsets[0] / totSamples, -tmpOffsets[1] / totSamples, -tmpOffsets[2] / totSamples);
}

void DFRobot_ITG3200::readGyrorawCal(int *_GyroX, int *_GyroY, int *_GyroZ)
{
  readGyroraw(_GyroX, _GyroY, _GyroZ);
  *_GyroX += offsets[0];
  *_GyroY += offsets[1];
  *_GyroZ += offsets[2];
}

void DFRobot_ITG3200::readGyrorawCal(int *_GyroXYZ)
{
  readGyrorawCal(_GyroXYZ, _GyroXYZ + 1, _GyroXYZ + 2);
}

void DFRobot_ITG3200::readGyro(float *_GyroX, float *_GyroY, float *_GyroZ)
{
  int x, y, z;
  readGyrorawCal(&x, &y, &z); 
  *_GyroX = x / 14.375 * polarities[0] * gains[0];
  *_GyroY = y / 14.375 * polarities[1] * gains[1];
  *_GyroZ = z / 14.375 * polarities[2] * gains[2];
}

void DFRobot_ITG3200::readGyro(float *_GyroXYZ)
{
  readGyro(_GyroXYZ, _GyroXYZ + 1, _GyroXYZ + 2);
}

void DFRobot_ITG3200::reset(void)
{
  w_data = PWRMGM_HRESET;
  writeData(PWR_MGM, &w_data,1);
  delay(GYROSTART_UP_DELAY); 
}

bool DFRobot_ITG3200::isLowpower(void)
{
  readData(PWR_MGM, &_buff[0],1);
  return (_buff[0] & PWRMGM_SLEEP) >> 6;
}

void DFRobot_ITG3200::setPowermode(bool _State)
{
  readData(PWR_MGM, &_buff[0], 1);
  w_data = ((_buff[0] & ~PWRMGM_SLEEP) | _State << 6);
  writeData(PWR_MGM, &w_data,1);
}

bool DFRobot_ITG3200::isXgyroStandby(void)
{
  readData(PWR_MGM, &_buff[0],1);
  return (_buff[0] & PWRMGM_STBY_XG) >> 5;
}

bool DFRobot_ITG3200::isYgyroStandby(void)
{
  readData(PWR_MGM, &_buff[0],1);
  return (_buff[0] & PWRMGM_STBY_YG) >> 4;
}

bool DFRobot_ITG3200::isZgyroStandby(void)
{
  readData(PWR_MGM, &_buff[0],1);
  return (_buff[0] & PWRMGM_STBY_ZG) >> 3;
}

void DFRobot_ITG3200::setXgyroStandby(bool _Status)
{
  readData(PWR_MGM, &_buff[0],1);
  w_data = ((_buff[0] & PWRMGM_STBY_XG) | _Status << 5);
  writeData(PWR_MGM, &w_data, 1);
}

void DFRobot_ITG3200::setYgyroStandby(bool _Status)
{
  readData(PWR_MGM, &_buff[0],1);
  w_data = ((_buff[0] & PWRMGM_STBY_YG) | _Status << 4);
  writeData(PWR_MGM, &w_data, 1);
}

void DFRobot_ITG3200::setZgyroStandby(bool _Status)
{
  readData(PWR_MGM, &_buff[0],1);
  w_data = ((_buff[0] & PWRMGM_STBY_ZG) | _Status << 3);
  writeData(PWR_MGM, &w_data, 1);
}

void DFRobot_ITG3200::setClocksource(uint8_t _CLKsource)
{
  readData(PWR_MGM,&_buff[0],1);
  w_data = ((_buff[0] & ~PWRMGM_CLK_SEL) | _CLKsource);
  writeData(PWR_MGM, &w_data, 1);
}

uint8_t DFRobot_ITG3200::getClocksource(void)
{
  readData(PWR_MGM, &_buff[0],1);
  return (_buff[0] & PWRMGM_CLK_SEL);
}

void DFRobot_ITG3200::writeData(uint8_t reg, void *pdata, uint8_t len)
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

int16_t DFRobot_ITG3200::readData(uint8_t reg, uint8_t *data, uint8_t len)
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
