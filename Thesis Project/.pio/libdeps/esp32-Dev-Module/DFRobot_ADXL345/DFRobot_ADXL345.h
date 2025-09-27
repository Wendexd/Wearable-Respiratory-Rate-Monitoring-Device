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
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>

/* -- ADXL345 addresses --*/
// ADXL345 address when SDO is connected to HIGH
#define ADXL345_ADDR_ALT_HIGH 0x1D
// ADXL345 address when SDO is connected to LOW
#define ADXL345_ADDR_ALT_LOW  0x53 
#define TO_READ 6
/* -- register --*/
#define ADXL345_DEVID 0x00
#define ADXL345_RESERVED1 0x01
#define ADXL345_THRESH_TAP 0x1d
#define ADXL345_OFSX 0x1e
#define ADXL345_OFSY 0x1f
#define ADXL345_OFSZ 0x20
#define ADXL345_DUR 0x21
#define ADXL345_LATENT 0x22
#define ADXL345_WINDOW 0x23
#define ADXL345_THRESH_ACT 0x24
#define ADXL345_THRESH_INACT 0x25
#define ADXL345_TIME_INACT 0x26
#define ADXL345_ACT_INACT_CTL 0x27
#define ADXL345_THRESH_FF 0x28
#define ADXL345_TIME_FF 0x29
#define ADXL345_TAP_AXES 0x2a
#define ADXL345_ACT_TAP_STATUS 0x2b
#define ADXL345_BW_RATE 0x2c
#define ADXL345_POWER_CTL 0x2d
#define ADXL345_INT_ENABLE 0x2e
#define ADXL345_INT_MAP 0x2f
#define ADXL345_INT_SOURCE 0x30
#define ADXL345_DATA_FORMAT 0x31
#define ADXL345_DATAX0 0x32
#define ADXL345_DATAX1 0x33
#define ADXL345_DATAY0 0x34
#define ADXL345_DATAY1 0x35
#define ADXL345_DATAZ0 0x36
#define ADXL345_DATAZ1 0x37
#define ADXL345_FIFO_CTL 0x38
#define ADXL345_FIFO_STATUS 0x39
/* -- data rate --*/
#define ADXL345_BW_1600 0xF // 1111
#define ADXL345_BW_800 0xE  // 1110
#define ADXL345_BW_400 0xD  // 1101
#define ADXL345_BW_200 0xC  // 1100
#define ADXL345_BW_100 0xB  // 1011
#define ADXL345_BW_50 0xA   // 1010
#define ADXL345_BW_25 0x9   // 1001
#define ADXL345_BW_12 0x8   // 1000
#define ADXL345_BW_6 0x7    // 0111
#define ADXL345_BW_3 0x6    // 0110
/* -- interrupt PIN--*/
#define ADXL345_INT1_PIN 0x00
#define ADXL345_INT2_PIN 0x01
/* -- interrupt BIT--*/
#define ADXL345_INT_DATA_READY_BIT 0x07
#define ADXL345_INT_SINGLE_TAP_BIT 0x06
#define ADXL345_INT_DOUBLE_TAP_BIT 0x05
#define ADXL345_INT_ACTIVITY_BIT 0x04
#define ADXL345_INT_INACTIVITY_BIT 0x03
#define ADXL345_INT_FREE_FALL_BIT 0x02
#define ADXL345_INT_WATERMARK_BIT 0x01
#define ADXL345_INT_OVERRUNY_BIT 0x00
/* -- interrupts mask--*/
#define ADXL345_DATA_READY 0x07
#define ADXL345_SINGLE_TAP 0x06
#define ADXL345_DOUBLE_TAP 0x05
#define ADXL345_ACTIVITY 0x04
#define ADXL345_INACTIVITY 0x03
#define ADXL345_FREE_FALL 0x02
#define ADXL345_WATERMARK 0x01
#define ADXL345_OVERRUNY 0x00

// initial state
#define ADXL345_NO_ERROR 0
// problem reading accel
#define ADXL345_READ_ERROR 1
// bad method argument
#define ADXL345_BAD_ARG 2    

class DFRobot_ADXL345
{
  public:
    /**
    * @struct sRP_t
    * @brief Roll & Pitch are the angles which rotate by the axis X and y
    */
    typedef struct
    {
      double roll;
      double pitch;
    }sRP_t;

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
     * @param xyx store the data on x-, y- and z-axis
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
     * @return  bool type, indicates whether to do tap detection on Z-axis
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
     * @return  bool type, indicates whether tap source is in sleep mode
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
     * @param state  power mode
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
     * @brief if interrupt is enabled
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
     * @param status   The obtained value of interrupt source register
     */
    void doubleTapInt(bool status);

    /**
     * @fn singleTapInt
     * @brief set whether to enable single tap interrupt
     * @param status  The obtained value of interrupt source register
     */
    void singleTapInt(bool status);

    sRP_t RP;   
    bool status;     // set when error occurs
    uint8_t error_code; // Initial state
    float gains[3];  // counts to Gs
  private:
    uint8_t _buff[6];
    void readAccel(int *x, int *y, int *z);
    virtual void writeData(uint8_t reg, void *pdata, uint8_t len)=0;
    virtual int16_t readData(uint8_t reg, uint8_t *data, uint8_t len)=0;
    void setRegisterBit(uint8_t regAdress, int bitPos, bool state);
    bool getRegisterBit(uint8_t regAdress, int bitPos);
};

class DFRobot_ADXL345_I2C:public DFRobot_ADXL345
{
  public:
    DFRobot_ADXL345_I2C(TwoWire *pWire = &Wire, uint8_t I2C_addr = 0x53);
    bool begin(void);
    void writeData(uint8_t reg, void *pdata, uint8_t len);
    int16_t readData(uint8_t reg, uint8_t *data, uint8_t len);
  private:
    TwoWire* _pWire;
    uint8_t _I2C_addr;
};

class DFRobot_ADXL345_SPI : public DFRobot_ADXL345
{
  public:
    DFRobot_ADXL345_SPI(SPIClass *spi = &SPI, uint8_t csPin = 10);
    bool begin(void);
  protected:
    void writeData(uint8_t reg, void *pdata, uint8_t len);
    int16_t readData(uint8_t reg, uint8_t *data, uint8_t len);
  private:
    SPIClass *_pSpi;
    uint8_t _csPin;
};
