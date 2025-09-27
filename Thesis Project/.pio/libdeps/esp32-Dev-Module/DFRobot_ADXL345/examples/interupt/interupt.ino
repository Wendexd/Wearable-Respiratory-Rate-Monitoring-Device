/*!
 * @interupt.ino
 * @brief The sensor will send an interrupt signal when triggered by events like single tap, double tap, free-falling, etc.
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author      PengKaixing(kaixing.peng@dfrobot.com)
 * @version  V2.0.0
 * @date  2022-02-22
 * @url https://github.com/DFRobot/DFRobot_ADXL345
 */
 
#include "DFRobot_ADXL345.h"

#define cs_pin 10

DFRobot_ADXL345_I2C ADXL345(&Wire,0x53);
/**
 * Note that the ICSP pin need to be connected when using leonardo as the main controller.
 */
// DFRobot_ADXL345_SPI ADXL345(&SPI, cs_pin);

void setup(){
  // Start the serial terminal
  Serial.begin(9600);         
  ADXL345.begin();      
  
  // Power on the ADXL345
  ADXL345.powerOn();  
                     
  /**
   * Give the range settings
   * Accepted values are 2g, 4g, 8g or 16g
   * Higher Values = Wider Measurement Range
   * Lower Values = Greater Sensitivity
   */
  ADXL345.setRangeSetting(16);
  
  /**
   * Configure the device to be in 4 wire SPI mode when set to '0' or 3 wire SPI mode when set to 1
   * Default: Set to 1
   * SPI pins on the ATMega328: 11, 12 and 13 as reference in SPI Library
   */        
  //ADXL345.setSpiBit(0);                   
   
  // Set to activate movement detection in the axes (1 == ON, 0 == OFF)
  ADXL345.setActivityX(1);      
  // ADXL345.isActivityXEnabled();
  ADXL345.setActivityY(0);
  // ADXL345.isActivityYEnabled();
  ADXL345.setActivityZ(0);
  // ADXL345.isActivityZEnabled();

  /**
   * 62.5mg per increment   
   * Set activity   
   * Inactivity thresholds (0-255)
   */
  ADXL345.setActivityThreshold(75);
  // ADXL345.getActivityThreshold();

  // Set to detect inactivity in all the axes(1 == ON, 0 == OFF)
  ADXL345.setInactivityX(1);
  // ADXL345.isInactivityXEnabled();
  ADXL345.setInactivityY(0);
  // ADXL345.isInactivityYEnabled();
  ADXL345.setInactivityZ(0);
  // ADXL345.isInactivityZEnabled();

  /**
   * 62.5mg per increment
   * Set inactivity
   * Inactivity thresholds (0-255) 
   */
  ADXL345.setInactivityThreshold(75);
  //ADXL345.getInactivityThreshold();

  // How many seconds of no activity is inactive?
  ADXL345.setTimeInactivity(10);
  ADXL345.getTimeInactivity();

  // Detect taps in the directions turned ON(1 == ON, 0 == OFF)
  ADXL345.setTapDetectionOnX(0);
  // ADXL345.isTapDetectionOnX();
  ADXL345.setTapDetectionOnY(0);
  // ADXL345.isTapDetectionOnY();
  ADXL345.setTapDetectionOnZ(1);
  // ADXL345.isTapDetectionOnZ();

  // Set values for what is considered a TAP and what is a DOUBLE TAP (0-255)
  // 62.5 mg per increment
  ADXL345.setTapThreshold(50);
  // Gets the click trigger threshold
  //ADXL345.getTapThreshold();

  // 625 μs per increment          
  ADXL345.setTapDuration(15);
  // ADXL345.getTapDuration();

  // 1.25 ms per increment          
  ADXL345.setDoubleTapLatency(80);
  // ADXL345.getDoubleTapLatency();

  // 1.25 ms per increment    
  ADXL345.setDoubleTapWindow(200);
  // ADXL345.getDoubleTapWindow();

  // Set values for what is considered FREE FALL (0-255)
  // (5 - 9) recommended - 62.5mg per increment
  ADXL345.setFreeFallThreshold(7);
  ADXL345.getFreeFallThreshold();
  // (20 - 70) recommended - 5ms per increment
  ADXL345.setFreeFallDuration(30);       
 
  // Setting all interupts to take place on INT1 pin,default to INT1 pin.
  //ADXL345.setImportantInterruptMapping(1, 1, 1, 1, 1);    
  
  // Turn on Interrupts for each mode (1 == ON, 0 == OFF)
  ADXL345.inactivityInt(1);
  ADXL345.activityInt(1);
  ADXL345.freeFallInt(1);
  ADXL345.doubleTapInt(1);
  ADXL345.singleTapInt(1);
  
//attachInterrupt(digitalPinToInterrupt(interruptPin), ADXL_ISR, RISING);   // Attach Interrupt

}

void loop()
{
  ADXL_ISR();
}

/********************* ISR *********************/
/* Look for Interrupts and Triggered Action    */
void ADXL_ISR(void) 
{
  /**
   * getInterruptSource clears all triggered actions after returning value
   * Do not call again until you need to recheck for triggered actions
   */
  byte interrupts = ADXL345.getInterruptSource();
  
  // Free Fall Detection
  if(ADXL345.triggered(interrupts, ADXL345_FREE_FALL)){
    Serial.println("*** FREE FALL ***");
    //add code here to do when free fall is sensed
  } 
  
  // Inactivity
  if(ADXL345.triggered(interrupts, ADXL345_INACTIVITY)){
    Serial.println("*** INACTIVITY ***");
     //add code here to do when inactivity is sensed
  }
  
  // Activity
  if(ADXL345.triggered(interrupts, ADXL345_ACTIVITY)){
    Serial.println("*** ACTIVITY ***"); 
     //add code here to do when activity is sensed
  }
  
  // Double Tap Detection
  if(ADXL345.triggered(interrupts, ADXL345_DOUBLE_TAP)){
    Serial.println("*** DOUBLE TAP ***");
     //add code here to do when a 2X tap is sensed
  }
  
  // Tap Detection
  if(ADXL345.triggered(interrupts, ADXL345_SINGLE_TAP)){
    Serial.println("*** TAP ***");
     //add code here to do when a tap is sensed
  } 
}
