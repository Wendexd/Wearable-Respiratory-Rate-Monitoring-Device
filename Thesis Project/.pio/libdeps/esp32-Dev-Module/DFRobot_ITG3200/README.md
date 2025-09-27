# DFRobot_ITG3200

- [中文版](./README_CN.md)

The 10 DOF(degrees of the freedom) IMU sensor is a compact and low-cost IMU from DFRobot. It integrates ADXL345 accelerometer, QMC5883L magnetometer, ITG3200 gyro, BMP280 barometric sensor and temperature sensor. This sensor embeds a low noise LDO regulator for supplying a wide range of power input, and works well with a 3V-5V power supply. Certainly, it is compatible with the Arduino board.

![正反面svg效果图](./resources/images/SEN0140.png)

## Product Link (https://www.dfrobot.com/product-818.html)

    SKU: SEN0140

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

This library provides a routine for the ITG3200 gyro to get the data on X, Y, and Z axis.

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++

    /**
     * @fn begin
     * @param _SRateDiv Sample rate divider
     * @param _Range Gyro Full Scale Range
     * @param _filterBW Digital Low Pass Filter BandWidth and SampleRate
     * @param _ClockSrc Clock Source - user parameters
     * @param _ITGReady enable interrupt register
     * @param _INTRawDataReady enable data ready register
     * @return bool type, indicate returning init status
     * @retval true init succeeded
     * @retval false init failed
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
     * @n ACTIVE_ONHIGH interrupt active on high
     * @n ACTIVE_ONLOW interrupt active on low
     */
    void setIntlogicLvl(bool _State);

    /**
     * @fn isIntactiveOnlow
     * @brief whether the module is at low level when an interrupt is triggered
     * @return bool
     * @retval true interrupt active on high
     * @retval false interrupt active on low
     */
    bool isIntactiveOnlow(void);

    /**
     * @fn setIntdriveType
     * @brief set interrupt pin status
     * @param _State pin status
     * @n OPEN_DRAIN open drain output
     * @n PUSH_PULL push pull output
     */
    void setIntdriveType(bool _State);

    /**
     * @fn isIntopenDrain
     * @brief whether the interrupt pin is open drain output
     * @return bool
     * @retval true yes
     * @retval false no
     */
    bool isIntopenDrain(void);

    /**
     * @fn setItgready
     * @brief if enable interrupt when device is ready (PLL ready after changing clock source)
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
     * @brief whether the raw data has been ready
     * @return bool
     * @retval true yes 
     * @retval false no
     */
    bool isRawdataReady(void);

    /**
     * @fn readTemp
     * @brief Get board temp
     * @param _Temp Save the temp
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
     * @brief Set power mode
     * @param _State mode select
     * @n     NORMAL
     * @n     STANDBY
     */
    void setPowermode(bool _State);

    /**
     * @fn isXgyroStandby
     * @brief whether the data on the X-axis of the gyro is ready 
     * @return bool
     * @retval true it is 
     * @retval false it isn't
     */
    bool isXgyroStandby(void);

    /**
     * @fn isYgyroStandby
     * @brief whether the data on the Y-axis of the gyro is ready
     * @return bool
     * @retval true it is
     * @retval false it isn't
     */
    bool isYgyroStandby(void);

    /**
     * @fn isZgyroStandby
     * @brief whether the data on the Z-axis of the gyro is ready
     * @return bool
     * @retval true it is
     * @retval false it isn't
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
     * @brief get gyroscope range
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

```

## Compatibility

MCU               | Work Well  | Work Wrong   | Untested   | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino uno        |      √       |              |             | 
Mega2560        |      √       |              |             | 
Leonardo        |      √       |              |             | 
ESP32           |      √       |              |             | 
ESP8266           |      √       |              |             | 
Micro:bit           |      √       |              |             | 

## History

- 2022/3/2 - 2.0.0 Version

## Credits

Written by Peng Kaixing(kaixing.peng@dfrobot.com), 2020. (Welcome to our [website](https://www.dfrobot.com/))
