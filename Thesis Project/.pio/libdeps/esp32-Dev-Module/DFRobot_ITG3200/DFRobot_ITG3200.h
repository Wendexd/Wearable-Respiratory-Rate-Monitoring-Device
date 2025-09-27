/*!
 * @file DFRobot_ITG3200.h
 * @brief A gyro sensor library
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author PengKaixing(kaixing.peng@dfrobot.com)
 * @version  V2.0.0
 * @date  2022-2-28
 * @url https://github.com/DFRobot/DFRobot_ITG3200
 */

#ifndef ITG3200_h
#define ITG3200_h
#include <Arduino.h>
#include <Wire.h>

// 50ms from gyro startup + 20ms register r/w startup
#define GYROSTART_UP_DELAY 70 

/* ---- Registers ---- */
#define WHO_AM_I 0x00   // RW   SETUP: I2C address
#define SMPLRT_DIV 0x15 // RW   SETUP: Sample Rate Divider
#define DLPF_FS 0x16    // RW   SETUP: Digital Low Pass Filter/ Full Scale range
#define INT_CFG 0x17    // RW   Interrupt: Configuration
#define INT_STATUS 0x1A // R	Interrupt: Status
#define TEMP_OUT 0x1B   // R	SENSOR: Temperature 2bytes
#define GYRO_XOUT 0x1D  // R	SENSOR: Gyro X 2bytes
#define GYRO_YOUT 0x1F  // R	SENSOR: Gyro Y 2bytes
#define GYRO_ZOUT 0x21  // R	SENSOR: Gyro Z 2bytes
#define PWR_MGM 0x3E    // RW	Power Management

/* ---- bit maps ---- */
#define DLPFFS_FS_SEL 0x18           // 00011000
#define DLPFFS_DLPF_CFG 0x07         // 00000111
#define INTCFG_ACTL 0x80             // 10000000
#define INTCFG_OPEN 0x40             // 01000000
#define INTCFG_LATCH_INT_EN 0x20     // 00100000
#define INTCFG_INT_ANYRD_2CLEAR 0x10 // 00010000
#define INTCFG_ITG_RDY_EN 0x04       // 00000100
#define INTCFG_RAW_RDY_EN 0x01       // 00000001
#define INTSTATUS_ITG_RDY 0x04       // 00000100
#define INTSTATUS_RAW_DATA_RDY 0x01  // 00000001
#define PWRMGM_HRESET 0x80           // 10000000
#define PWRMGM_SLEEP 0x40            // 01000000
#define PWRMGM_STBY_XG 0x20          // 00100000
#define PWRMGM_STBY_YG 0x10          // 00010000
#define PWRMGM_STBY_ZG 0x08          // 00001000
#define PWRMGM_CLK_SEL 0x07          // 00000111

/************************************/
/*    REGISTERS PARAMETERS    */
/************************************/
// Sample Rate Divider
#define NOSRDIVIDER 0 // default    FsampleHz=SampleRateHz/(divider+1)
// Gyro Full Scale Range
#define RANGE2000 3 // default
// Digital Low Pass Filter BandWidth and SampleRate
#define BW256_SR8 0 // default    256Khz BW and 8Khz SR
#define BW188_SR1 1
#define BW098_SR1 2
#define BW042_SR1 3
#define BW020_SR1 4
#define BW010_SR1 5
#define BW005_SR1 6
// Interrupt Active logic lvl
#define ACTIVE_ONHIGH 0 // default
#define ACTIVE_ONLOW 1
// Interrupt drive type
#define PUSH_PULL 0 // default
#define OPEN_DRAIN 1
// Interrupt Latch mode
#define PULSE_50US 0 // default
#define UNTIL_INT_CLEARED 1
// Interrupt Latch clear method
#define READ_STATUSREG 0 // default
#define READ_ANYREG 1
// Power management
#define NORMAL 0 // default
#define STANDBY 1
// Clock Source - user parameters
#define INTERNALOSC 0 // default
#define PLL_XGYRO_REF 1
#define PLL_YGYRO_REF 2
#define PLL_ZGYRO_REF 3
#define PLL_EXTERNAL32 4 // 32.768 kHz
#define PLL_EXTERNAL19 5 // 19.2 Mhz

class DFRobot_ITG3200{
  public:
    DFRobot_ITG3200(TwoWire *pWire = &Wire, uint8_t I2C_addr = 0x68);

    /**
     * @fn begin
     * @param _SRateDiv Sample rate divider
     * @param _Range Gyro Full Scale Range
     * @param _filterBW Digital Low Pass Filter BandWidth and SampleRate
     * @param _ClockSrc Clock Source - user parameters
     * @param _ITGReady Enable interrupt register
     * @param _INTRawDataReady Enable data ready register
     * @return bool type, indicate returning init status
     * @retval true Init succeeded
     * @retval false Init failed
     */
    bool begin(uint8_t _SRateDiv = NOSRDIVIDER, uint8_t _Range = RANGE2000, uint8_t _filterBW = BW256_SR8, uint8_t _ClockSrc = PLL_XGYRO_REF, bool _ITGReady = true, bool _INTRawDataReady = true);

    /**
     * @fn setSamplerateDiv
     * @brief Set the gyroscope sampling rate
     * @param _SampleRate
     * @n     Sample rate divider: 0 to 255
     * @n     calculate:Fsample = Finternal / (_SampleRate+1)
     * @n     Finternal is 1kHz or 8kHz
     */
    void setSamplerateDiv(uint8_t _SampleRate);

    /**
     * @fn getSamplerateDiv
     * @brief Get the gyroscope sampling rate
     * @return uint8_t
     */
    uint8_t getSamplerateDiv(void);

    /**
     * @fn setIntlogicLvl
     * @brief Interrupt Configuration
     * @param bool
     * @n ACTIVE_ONHIGH Interrupt active on high
     * @n ACTIVE_ONLOW Interrupt active on low
     */
    void setIntlogicLvl(bool _State);

    /**
     * @fn isIntactiveOnlow
     * @brief whether the module is at low level when an interrupt is triggered
     * @return bool
     * @retval true Interrupt active on high
     * @retval false Interrupt active on low
     */
    bool isIntactiveOnlow(void);

    /**
     * @fn setIntdriveType
     * @brief Set interrupt pin status
     * @param _State pin status
     * @n OPEN_DRAIN Open drain output
     * @n PUSH_PULL Push pull output
     */
    void setIntdriveType(bool _State);

    /**
     * @fn isIntopenDrain
     * @brief Whether the interrupt pin is open drain output
     * @return bool
     * @retval true yes
     * @retval false no
     */
    bool isIntopenDrain(void);

    /**
     * @fn setItgready
     * @brief If enable interrupt when device is ready (PLL ready after changing clock source)
     * @param _State
     * @n     true   enable
     * @n     false  disable
     */
    void setItgready(bool _State);

    /**
     * @fn isItgreadyOn
     * @brief if the interrupt switch has been turned on
     * @return true yes
     * @return false no
     */
    bool isItgreadyOn(void);

    /**
     * @fn isItgready
     * @brief whether to enable or disable interrupt
     * @return bool
     * @retval true enable
     * @retval false disable
     */
    bool isItgready(void);

    /**
     * @fn isRawdataReady
     * @brief whether the raw data is ready
     * @return bool
     * @retval true yes
     * @retval false no
     */
    bool isRawdataReady(void);

    /**
     * @fn readTemp
     * @brief Get board temp
     * @param _Temp save the temp
     */
    void readTemp(float *_Temp);

    /**
     * @fn zeroCalibrate
     * @brief assuming gyroscope is stationary (updates XYZ offsets)
     * @param totSamples
     * @param sampleDelayMS
     */
    void zeroCalibrate(unsigned int totSamples, unsigned int sampleDelayMS);

    /**
     * @fn readGyro(float *_GyroX, float *_GyroY, float *_GyroZ)
     * @brief read deg/sec calibrated & ScaleFactor
     * @param _GyroX
     * @param _GyroY
     * @param _GyroZ
     */
    void readGyro(float *_GyroX, float *_GyroY, float *_GyroZ);

    /**
     * @fn readGyro(float *_GyroXYZ)
     * @brief read deg/sec calibrated & ScaleFactor
     * @param _GyroXYZ
     */
    void readGyro(float *_GyroXYZ);          

    /**
     * @fn reset
     * @brief after reset all registers have default values
     */
    void reset(void);

    /**
     * @fn isLowpower
     * @brief Check if the sensor is in low power mode
     * @return bool
     * @retval true yes
     * @retval false no
     */
    bool isLowpower(void);

    /**
     * @fn setPowerMode
     * @brief set power mode
     * @param _State mode select
     * @n     NORMAL
     * @n     STANDBY
     */
    void setPowermode(bool _State);

    /**
     * @fn isXgyroStandby
     * @brief whether the data on the X-axis of the gyro is ready
     * @return bool
     * @retval true yes
     * @retval false no
     */
    bool isXgyroStandby(void);

    /**
     * @fn isYgyroStandby
     * @brief whether the data on the Y-axis of the gyro is ready
     * @return bool
     * @retval true yes
     * @retval false no
     */
    bool isYgyroStandby(void);

    /**
     * @fn isZgyroStandby
     * @brief whether the data on the Z-axis of the gyro is ready
     * @return bool
     * @retval true yes
     * @retval false no
     */
    bool isZgyroStandby(void);

    /**
     * @fn setXgyroStandby
     * @brief set X-axis standby mode, the data on the X-axis will not be obtained in standby mode
     * @param _Status
     * @n     NORMAL enable
     * @n     STANDBY disable
     */
    void setXgyroStandby(bool _Status);

    /**
     * @fn setYgyroStandby
     * @brief set Y-axis standby mode, the data on the Y-axis will not be obtained in standby mode
     * @param _Status
     * @n     NORMAL enable
     * @n     STANDBY disable
     */
    void setYgyroStandby(bool _Status);

    /**
     * @fn setZgyroStandby
     * @brief set Z-axis standby mode, the data on the Z-axis will not be obtained in standby mode
     * @param _Status
     * @n     NORMAL enable
     * @n     STANDBY disable
     */
    void setZgyroStandby(bool _Status);

    /**
     * @fn setFilterBW
     * @brief set filter bandwidth
     * @param _BW bandwidth
     */
    void setFilterBW(uint8_t _BW);

    /**
     * @fn getFilterBW
     * @brief get filter bandwidth
     * @return uint8_t
     */
    uint8_t getFilterBW(void);

    /**
     * @fn getFSrange
     * @brief get gyro range
     * @return uint8_t
     */
    uint8_t getFSrange(void);

    /**
     * @fn isLatchuntilCleared
     * @brief if Latch mode is latch until interrupt is cleared
     * @return true latch until interrupt is cleared
     * @return false 50us pulse
     */
    bool isLatchuntilCleared(void);

    /**
     * @fn isAnyregClrmode
     * @brief if Latch clear method is any register read
     * @return true any register read
     * @return false status register read only
     */
    bool isAnyregClrmode(void);

    /**
     * @fn getClocksource
     * @brief Get clock source
     * @return uint8_t
     */
    uint8_t getClocksource(void);
    float gains[3];
    int offsets[3];
    float polarities[3];
  private:
    void setClocksource(uint8_t _CLKsource);
    void setFSrange(uint8_t _Range);
    void readGyrorawCal(int *_GyroX, int *_GyroY, int *_GyroZ);
    void readGyrorawCal(int *_GyroXYZ);
    void readGyroraw(int *_GyroX, int *_GyroY, int *_GyroZ);
    void readGyroraw(int *_GyroXYZ);
    void setGains(float _Xgain, float _Ygain, float _Zgain);
    void setRevpolarity(bool _Xpol, bool _Ypol, bool _Zpol);
    void setOffsets(int _Xoffset, int _Yoffset, int _Zoffset);
    void setRawdataReady(bool _State);
    bool isRawdataReadyon(void);
    void writeData(uint8_t reg, void *pdata, uint8_t len);
    int16_t readData(uint8_t reg, uint8_t *data, uint8_t len);
    TwoWire *_pWire;
    uint8_t _I2C_addr;
    uint8_t _buff[6];
};
#endif
