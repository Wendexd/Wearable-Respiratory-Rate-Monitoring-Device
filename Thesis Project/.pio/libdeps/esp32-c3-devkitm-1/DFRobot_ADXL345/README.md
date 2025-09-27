# DFRobot_ADXL345

- [中文版](./README_CN.md)

The ADXL345 is a small, thin, low-power, 3-axis accelerometer with a high resolution (13-bit) measurement at up to ±16 g. Digital output data is formatted as 16-bit twos complement and is accessible through either an SPI (3- or 4-wire) or I2C digital interface. The ADXL345 is well suited to measures the static acceleration of gravity in tilt-sensing applications, as well as dynamic acceleration resulting from motion or shock. Its high resolution (4mg/LSB) enables measurement of inclination changes less than 1°. Besides, the ADXL345 3-axis accelerometer from DFrobot has a built-in LDO module that allows operating under 3.3 to 6V. And several special sensing functions are provided. Activity and inactivity sensing detect the presence or lack of motion and if the acceleration on any axis exceeds a user-set level. Tap sensing detects single and double taps. Free-fall sensing detects if the device is falling. These functions can be mapped individually to either of two interrupt output pins. Low power modes enable intelligent motion-based power management with threshold sensing and active acceleration measurement at extremely low power dissipation.

![正反面svg效果图](./resources/images/SEN0032.png)

## Product Link (https://www.dfrobot.com/product-383.html)

  SKU: SEN0032

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

This library provides a routine to get the raw data of the three axes and another to trigger interrupts using various events.

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++

  /**
   * @fn begin
   * @return bool type, indicate returning init status
   * @retval true init succeeded
   * @retval false init failed
   */
  bool begin(void);

  /**
   * @fn powerOn
   * @brief enable ADXL345 module
   */
  void powerOn(void);

  /**
   * @fn readAccel(int *xyz)
   * @brief get acceleration
   * @param xyx store the data on x-axis, y-axis and z-axis
   */
  void readAccel(int *xyz);

  /**
   * @fn setTapThreshold
   * @brief set tap trigger threshold
   * @param tapThreshold threshold
   */
  void setTapThreshold(int tapThreshold);

  /**
   * @fn getTapThreshold
   * @brief get tap trigger threshold
   * @return int type, return tap trigger threshold
   */
  int getTapThreshold(void);

  /**
   * @fn setTapDuration
   * @brief set tap duration
   * @param tapDuration duration
   */
  void setTapDuration(int tapDuration);

  /**
   * @fn getTapDuration
   * @brief get tap duration
   * @return int type, indicates duration 
   */
  int getTapDuration(void);

  /**
   * @fn setDoubleTapLatency
   * @brief set double tap latency
   * @param floatTapLatency latency
   */
  void setDoubleTapLatency(int floatTapLatency);

  /**
   * @fn getDoubleTapLatency
   * @brief get double tap latency
   * @return int type, indicates latency
   */
  int getDoubleTapLatency(void);

  /**
   * @fn setDoubleTapWindow
   * @brief set double tap window
   * @param floatTapWindow double tap window
   */
  void setDoubleTapWindow(int floatTapWindow);

  /**
   * @fn getDoubleTapWindow
   * @brief get double tap window
   * @return int type indicates tap window
   */
  int getDoubleTapWindow(void);

  /**
   * @fn setActivityThreshold
   * @brief set activity threshold
   * @param activityThreshold activity threshold
   */
  void setActivityThreshold(int activityThreshold);

  /**
   * @fn getActivityThreshold
   * @brief get activity threshold
   * @return int type indicates activity threshold
   */
  int getActivityThreshold(void);

  /**
   * @fn setInactivityThreshold
   * @brief set inactivity threshold
   * @param inactivityThreshold inactivity threshold
   */
  void setInactivityThreshold(int inactivityThreshold);

  /**
   * @fn getInactivityThreshold
   * @brief get inactivity threshold
   * @return int type indicates inactivity threshold
   */
  int getInactivityThreshold(void);

  /**
   * @fn setTimeInactivity
   * @brief set inactivity time
   * @param timeInactivity inactivity time
   */
  void setTimeInactivity(int timeInactivity);

  /**
   * @fn getTimeInactivity
   * @brief get inactivity time
   * @return int type indicates inactivity time
   */
  int getTimeInactivity(void);

  /**
   * @fn setFreeFallThreshold
   * @brief set free-fall threshold
   * @param timeInactivity free-fall threshold
   */
  void setFreeFallThreshold(int freeFallthreshold);

  /**
   * @fn getFreeFallThreshold
   * @brief get free-fall threshold
   * @return int free-fall threshold
   */
  int getFreeFallThreshold(void);

  /**
   * @fn setFreeFallDuration
   * @brief set free-fall duration
   * @param timeInactivity free-fall duration
   */
  void setFreeFallDuration(int freeFallDuration);

  /**
   * @fn getFreeFallThreshold
   * @brief get free-fall duration
   * @return int type indicates free-fall duration
   */
  int getFreeFallDuration(void);

  /**
   * @fn isActivityXEnabled
   * @brief whether to enable activity detection on X-axis
   * @return bool type, indicates whether to enable activity detection on X-axis
   * @retval true yes
   * @retval false no
   */
  bool isActivityXEnabled(void);

  /**
   * @fn isActivityYEnabled
   * @brief whether to enable activity detection on Y-axis
   * @return bool type, indicates whether to enable activity detection on Y-axis
   * @retval true yes
   * @retval false no
   */
  bool isActivityYEnabled(void);

  /**
   * @fn isActivityZEnabled
   * @brief whether to enable activity detection on Z-axis
   * @return bool type, indicates whether to enable activity detection on Z-axis
   * @retval true yes
   * @retval false no
   */
  bool isActivityZEnabled(void);

  /**
   * @fn isInactivityXEnabled
   * @brief whether to enable inactivity detection on X-axis
   * @return bool type, indicates whether to enable inactivity detection on X-axis
   * @retval true yes
   * @retval false no
   */
  bool isInactivityXEnabled(void);

  /**
   * @fn isInactivityYEnabled
   * @brief whether to enable inactivity detection on Y-axis
   * @return bool type, indicates whether to enable inactivity detection on Y-axis
   * @retval true yes
   * @retval false no
   */
  bool isInactivityYEnabled(void);

  /**
   * @fn isInactivityZEnabled
   * @brief whether to enable inactivity detection on Z-axis
   * @return whether to enable inactivity detection on Z-axis
   * @retval true yes
   * @retval false no
   */
  bool isInactivityZEnabled(void);

  /**
   * @fn isTapDetectionOnX
   * @brief whether to do tap detection on X-axis
   * @return  bool type, indicates whether to do tap detection on X-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isTapDetectionOnX(void);

  /**
   * @fn setTapDetectionOnX
   * @brief set tap detection on X-axis
   * @param state state
   * @n           1 tap
   * @n           0 no tap
   */
  void setTapDetectionOnX(bool state);

  /**
   * @fn isTapDetectionOnY
   * @brief whether to do tap detection on Y-axis
   * @return  bool type, indicates whether to do tap detection on Y-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isTapDetectionOnY(void);

  /**
   * @fn setTapDetectionOnY
   * @brief set tap detection on Y-axis
   * @param state state
   * @n           1 tap
   * @n           0 no tap
   */
  void setTapDetectionOnY(bool state);

  /**
   * @fn isTapDetectionOnZ
   * @brief whether to do tap detection on Z-axis
   * @return  type, indicates whether to do tap detection on Z-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isTapDetectionOnZ(void);

  /**
   * @fn setTapDetectionOnZ
   * @brief set tap detection on Z-axis
   * @param state state
   * @n           1 tap
   * @n           0 no tap
   */
  void setTapDetectionOnZ(bool state);

  /**
   * @fn setActivityX
   * @brief set activity on X-axis
   * @param state activity status
   * @n           1 activity
   * @n           0 inactivity
   */
  void setActivityX(bool state);

  /**
   * @fn setActivityY
   * @brief set activity on Y-axis
   * @param state activity status
   * @n           1 activity
   * @n           0 inactivity
   */
  void setActivityY(bool state);

  /**
   * @fn setActivityZ
   * @brief set activity on Z-axis
   * @param state activity status
   * @n           1 activity
   * @n           0 inactivity
   */
  void setActivityZ(bool state);

  /**
   * @fn setInactivityX
   * @brief set inactivity on X-axis
   * @param state activity status
   * @n           0 activity
   * @n           1 inactivity
   */
  void setInactivityX(bool state);

  /**
   * @fn setInactivityY
   * @brief set inactivity on Y-axis
   * @param state activity status
   * @n           0 activity
   * @n           1 inactivity
   */
  void setInactivityY(bool state);

  /**
   * @fn setInactivityZ
   * @brief set inactivity on Z-axis
   * @param state activity status
   * @n           0 activity
   * @n           1 inactivity
   */
  void setInactivityZ(bool state);

  /**
   * @fn isActivitySourceOnX
   * @brief whether activity source is on X-axis
   * @return  whether on X-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isActivitySourceOnX(void);

  /**
   * @fn isActivitySourceOnY
   * @brief whether activity source is on Y-axis
   * @return  bool type, indicates whether on Y-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isActivitySourceOnY(void);

  /**
   * @fn isActivitySourceOnZ
   * @brief whether activity source is on Z-axis
   * @return  bool type, indicates whether on Z-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isActivitySourceOnZ(void);

  /**
   * @fn isTapSourceOnX
   * @brief whether tap source is on X-axis
   * @return  bool type, indicates whether tap source is on X-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isTapSourceOnX(void);

  /**
   * @fn isTapSourceOnY
   * @brief whether tap source is on Y-axis
   * @return  bool type, indicates whether tap source is on Y-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isTapSourceOnY(void);

  /**
   * @fn isTapSourceOnZ
   * @brief whether tap source is on Z-axis
   * @return  bool type, indicates whether tap source is on Z-axis
   * @retval  1 yes
   * @retval  0 no
   */
  bool isTapSourceOnZ(void);

  /**
   * @fn isAsleep
   * @brief whether tap source is in sleep mode
   * @return  bool type, indicates whether tap source is in sleep status
   * @retval  1 yes
   * @retval  0 no
   */
  bool isAsleep(void);

  /**
   * @fn isLowPower
   * @brief whether in low power mode
   * @return  bool type, indicates mode
   * @retval  0 normal mode
   * @retval  1 low power mode
   */
  bool isLowPower(void);

  /**
   * @fn setLowPower
   * @brief set low power mode
   * @param state power mode
   * @n           0 normal mode
   * @n           1 low power mode
   */
  void setLowPower(bool state);

  /**
   * @fn getRate
   * @brief get collecting rate
   * @return  float type, indicates collecting rate
   */
  float getRate(void);

  /**
   * @fn setRate
   * @brief set collecting rate
   * @param rate collecting rate
   */
  void setRate(float rate);

  /**
   * @fn setBwcode
   * @brief set data rate and power mode
   * @param bw_code rate and power
   * @n             ADXL345_BW_1600 0xF 
   * @n             ADXL345_BW_800 0xE  
   * @n             ADXL345_BW_400 0xD  
   * @n             ADXL345_BW_200 0xC  
   * @n             ADXL345_BW_100 0xB  
   * @n             ADXL345_BW_50 0xA   
   * @n             ADXL345_BW_25 0x9   
   * @n             ADXL345_BW_12 0x8   
   * @n             ADXL345_BW_6 0x7    
   * @n             ADXL345_BW_3 0x6    
   */
  void setBwcode(uint8_t bw_code);

  /**
   * @fn getBwcode
   * @brief get data rate and power mode
   * @return  uint8_t type
   */
  uint8_t getBwcode(void);

  /**
   * @fn getInterruptSource(void)
   * @brief get interrupt source
   * @return  uint8_t type, indicates interrupt source
   */
  uint8_t getInterruptSource(void);

  /**
   * @fn getInterruptSource(uint8_t interruptBit)
   * @brief get whether to enable interrupt source
   * @param   interruptBit interrupt bit
   * @return  bool type, whether to enable interrupt source
   * @retval  true interrupt
   * @retval  false not interrupt
   */
  bool getInterruptSource(uint8_t interruptBit);

  /**
   * @fn getInterruptMapping
   * @brief get interrupt mapping
   * @param   interruptBit interrupt bit
   * @return  bool type, indicates whether getting successful
   * @retval  true successful
   * @retval  false failed
   */
  bool getInterruptMapping(uint8_t interruptBit);

  /**
   * @fn setInterruptMapping
   * @brief set interrupt mapping
   * @param   interruptBit interrupt bit
   * @param   interruptPin interrupt pin
   */
  void setInterruptMapping(uint8_t interruptBit, bool interruptPin);

  /**
   * @fn isInterruptEnabled
   * @brief If interrupt is enabled 
   * @param   interruptBit interrupt bit
   * @return  bool type, indicates if interrupt is enabled
   * @retval  true yes
   * @retval  false no
   */
  bool isInterruptEnabled(uint8_t interruptBit);

  /**
   * @fn setInterrupt
   * @brief set whether to enable interrupt
   * @param   interruptBit interrupt bit
   * @param   state state
   * @n       true  enable
   * @n       false disable     
   */
  void setInterrupt(uint8_t interruptBit, bool state);

  /**
   * @fn getRangeSetting
   * @brief get range setting
   * @param   rangeSetting for storing range setting
   */
  void getRangeSetting(uint8_t *rangeSetting);

  /**
   * @fn setRangeSetting
   * @brief set range setting
   * @param   val setting
   */
  void setRangeSetting(int val);

  /**
   * @fn getInterruptLevelBit
   * @brief get status of INT_INVERT bit
   * @return  bool type, status of INT_INVERT bit
   */
  bool getInterruptLevelBit(void);

  /**
   * @fn setInterruptLevelBit
   * @brief set status of INT_INVERT bit
   * @param interruptLevelBit status of INT_INVERT bit
   */
  void setInterruptLevelBit(bool interruptLevelBit);

  /**
   * @fn getFullResBit
   * @brief get status of FULL_RES bit
   * @return  bool type, status of FULL_RES bit
   */
  bool getFullResBit(void);

  /**
   * @fn setFullResBit
   * @brief set status of FULL_RES bit
   * @param fullResBit status of FULL_RES bit
   */
  void setFullResBit(bool fullResBit);

  /**
   * @fn getJustifyBit
   * @brief get status of justify bit
   * @return  bool type, status of justify bit
   */
  bool getJustifyBit(void);

  /**
   * @fn setJustifyBit
   * @brief set status of justify bit
   * @param justifyBit status of justify bit
   */
  void setJustifyBit(bool justifyBit);

  /**
   * @fn RPCalculate
   * @brief get the acceleration data on the 3 axes, and calculate the Roll and Pitch angle information when rotating in order of R-xyz according to the data
   * @param data_buf  the actual acceleration data on the 3 axes
   */
  void RPCalculate(int*data_buf);

  /**
   * @fn triggered
   * @brief detect interrupt trigger source
   * @param interrupts  The obtained value of interrupt source register
   * @param mask   The target mask to be detected
   */
  bool triggered(byte interrupts, int mask);

  /**
   * @fn inactivityInt
   * @brief set whether to enable inactivity interrupt
   * @param status  The obtained value of interrupt source register
   */
  void inactivityInt(bool status);

  /**
   * @fn activityInt
   * @brief set whether to enable activity interrupt
   * @param status  The obtained value of interrupt source register
   */
  void activityInt(bool status);

  /**
   * @fn freeFallInt
   * @brief set whether to enable free-fall interrupt
   * @param status  The obtained value of interrupt source register
   */
  void freeFallInt(bool status);

  /**
   * @fn doubleTapInt
   * @brief set whether to enable double tap interrupt
   * @param status  The obtained value of interrupt source register
   */
  void doubleTapInt(bool status);

  /**
   * @fn singleTapInt
   * @brief set whether to enable single tap interrupt
   * @param status  The obtained value of interrupt source register
   */
  void singleTapInt(bool status);
  
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

- 2022/2/25 - 2.0.0 Version

## Credits

Written by Peng Kaixing(kaixing.peng@dfrobot.com), 2020. (Welcome to our [website](https://www.dfrobot.com/))
