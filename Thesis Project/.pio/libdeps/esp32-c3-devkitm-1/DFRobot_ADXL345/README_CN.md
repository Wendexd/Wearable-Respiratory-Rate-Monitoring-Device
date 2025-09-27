# DFRobot_ADXL345

- [English Version](./README.md)

这款ADXL345三轴加速度采用ADXL345芯片，具有体积小，功耗低的特点，13位数字精度分辨能够测量超过±16g的加速度变换。信号输出为16位数字输出，可以通过SPI与I2C接口实现信号采集。ADXL345适用于倾斜角度测量，能够进行静态重力加速度检测。同时也适用于运动状态的追踪，测量运动或冲击过程造成的瞬时加速度。其高分辨率(4mg/LSB)使之能够感应变化小于1°的倾斜角度。 DFrobot的ADXL345三轴加速度计还内置一款LDO模块让你的加速度计能够工作于3.3~6v的工作电压之下。同时传感器提供了几个特殊的功能。能够在静态或动态情况下检测是否有运动或停止出现，另外能够感知单轴的加速度值是否超出用户的设定值。检测单击/双击。如果该设备正在下降，能进行自由落体感应检测。这些功能能够被映射到两个中断输出引脚上。在低功耗模式是用户能够基于ADXL345动作感应，进行电源管理，同时只损耗极低的功耗。 

![正反面svg效果图](./resources/images/SEN0032.png)

## 产品链接(https://www.dfrobot.com.cn/goods-297.html)

  SKU: SEN0032

## 目录

* [概述](#概述)
* [库安装](#库安装)
* [方法](#方法)
* [兼容性](#兼容性y)
* [历史](#历史)
* [创作者](#创作者)

## 概述

这个库提供了一个获取三轴原始数据的例程以及一个各种事件触发中断的例程

## 库安装

使用此库前，请首先下载库文件，将其粘贴到\Arduino\libraries目录中，然后打开examples文件夹并在该文件夹中运行演示。

## 方法

```C++

  /**
   * @fn begin
   * @return bool类型，表示返回初始化的状态
   * @retval true 初始化成功
   * @retval false 初始化失败
   */
  bool begin(void);

  /**
   * @fn powerOn
   * @brief 使能ADXL345模块
   */
  void powerOn(void);

  /**
   * @fn readAccel(int *xyz)
   * @brief 获取加速度
   * @param xyx 存储x轴,y轴,z轴数据
   */
  void readAccel(int *xyz);

  /**
   * @fn setTapThreshold
   * @brief 设置敲击触发阈值
   * @param tapThreshold 阈值
   */
  void setTapThreshold(int tapThreshold);

  /**
   * @fn getTapThreshold
   * @brief 获取敲击触发阈值
   * @return int类型 返回敲击触发阈值
   */
  int getTapThreshold(void);

  /**
   * @fn setTapDuration
   * @brief 设置敲击持续时间
   * @param tapDuration 持续时间
   */
  void setTapDuration(int tapDuration);

  /**
   * @fn getTapDuration
   * @brief 获取敲击持续时间
   * @return int类型 表示持续时间
   */
  int getTapDuration(void);

  /**
   * @fn setDoubleTapLatency
   * @brief 设置双击延迟时间
   * @param floatTapLatency 延迟时间
   */
  void setDoubleTapLatency(int floatTapLatency);

  /**
   * @fn getDoubleTapLatency
   * @brief 获取双击延迟时间
   * @return int类型 表示延迟时间
   */
  int getDoubleTapLatency(void);

  /**
   * @fn setDoubleTapWindow
   * @brief 设置双击窗
   * @param floatTapWindow 双击窗
   */
  void setDoubleTapWindow(int floatTapWindow);

  /**
   * @fn getDoubleTapWindow
   * @brief 获取双击窗
   * @return int类型 表示点击窗
   */
  int getDoubleTapWindow(void);

  /**
   * @fn setActivityThreshold
   * @brief 设置活动阈值
   * @param activityThreshold 活动阈值
   */
  void setActivityThreshold(int activityThreshold);

  /**
   * @fn getActivityThreshold
   * @brief 获取活动阈值
   * @return int类型 表示活动阈值
   */
  int getActivityThreshold(void);

  /**
   * @fn setInactivityThreshold
   * @brief 设置缺乏运动阈值
   * @param inactivityThreshold 缺乏运动阈值
   */
  void setInactivityThreshold(int inactivityThreshold);

  /**
   * @fn getInactivityThreshold
   * @brief 获取缺乏运动阈值
   * @return int类型 表示缺乏运动阈值
   */
  int getInactivityThreshold(void);

  /**
   * @fn setTimeInactivity
   * @brief 设置不活动时间
   * @param timeInactivity 不活动时间
   */
  void setTimeInactivity(int timeInactivity);

  /**
   * @fn getTimeInactivity
   * @brief 获取不活动时间
   * @return int类型 表示不活动时间
   */
  int getTimeInactivity(void);

  /**
   * @fn setFreeFallThreshold
   * @brief 设置自由落体阈值
   * @param timeInactivity 自由落体阈值
   */
  void setFreeFallThreshold(int freeFallthreshold);

  /**
   * @fn getFreeFallThreshold
   * @brief 获取自由落体阈值
   * @return int 自由落体阈值
   */
  int getFreeFallThreshold(void);

  /**
   * @fn setFreeFallDuration
   * @brief 设置自由落体持续时间
   * @param timeInactivity 自由落体持续时间
   */
  void setFreeFallDuration(int freeFallDuration);

  /**
   * @fn getFreeFallThreshold
   * @brief 获取自由落体持续时间
   * @return int类型 表示自由落体持续时间
   */
  int getFreeFallDuration(void);

  /**
   * @fn isActivityXEnabled
   * @brief 是否启用活动X轴
   * @return bool类型，表示是否启用活动X轴
   * @retval true 启用
   * @retval false 不启用
   */
  bool isActivityXEnabled(void);

  /**
   * @fn isActivityYEnabled
   * @brief 是否启用活动Y轴
   * @return bool类型，表示是否启用活动Y轴
   * @retval true 启用
   * @retval false 不启用
   */
  bool isActivityYEnabled(void);

  /**
   * @fn isActivityZEnabled
   * @brief 是否启用活动Z轴
   * @return bool类型，表示是否启用活动Z轴
   * @retval true 启用
   * @retval false 不启用
   */
  bool isActivityZEnabled(void);

  /**
   * @fn isInactivityXEnabled
   * @brief 是否启用不活动X
   * @return bool类型，表示是否启用不活动X
   * @retval true 启用
   * @retval false 不启用
   */
  bool isInactivityXEnabled(void);

  /**
   * @fn isInactivityYEnabled
   * @brief 是否启用不活动Y
   * @return bool类型，表示是否启用不活动Y
   * @retval true 启用
   * @retval false 不启用
   */
  bool isInactivityYEnabled(void);

  /**
   * @fn isInactivityZEnabled
   * @brief 是否启用不活动Z
   * @return 是否启用不活动Z
   * @retval true 启用
   * @retval false 不启用
   */
  bool isInactivityZEnabled(void);

  /**
   * @fn isTapDetectionOnX
   * @brief 是否在X上点击检测
   * @return  bool类型，表示是否点击
   * @retval  1 点击
   * @retval  0 不点击
   */
  bool isTapDetectionOnX(void);

  /**
   * @fn setTapDetectionOnX
   * @brief 设置在X上点击检测
   * @param state 状态
   * @n           1 点击
   * @n           0 不点击
   */
  void setTapDetectionOnX(bool state);

  /**
   * @fn isTapDetectionOnY
   * @brief 是否在Y上点击检测
   * @return  bool类型，表示是否点击
   * @retval  1 点击
   * @retval  0 不点击
   */
  bool isTapDetectionOnY(void);

  /**
   * @fn setTapDetectionOnY
   * @brief 设置在Y上点击检测
   * @param state 状态
   * @n           1 点击
   * @n           0 不点击
   */
  void setTapDetectionOnY(bool state);

  /**
   * @fn isTapDetectionOnZ
   * @brief 是否在Z上点击检测
   * @return  bool类型，表示是否点击
   * @retval  1 点击
   * @retval  0 不点击
   */
  bool isTapDetectionOnZ(void);

  /**
   * @fn setTapDetectionOnZ
   * @brief 设置在Z上点击检测
   * @param state 状态
   * @n           1 点击
   * @n           0 不点击
   */
  void setTapDetectionOnZ(bool state);

  /**
   * @fn setActivityX
   * @brief 设置X活动
   * @param state 活动状态
   * @n           1 活动
   * @n           0 不活动
   */
  void setActivityX(bool state);

  /**
   * @fn setActivityY
   * @brief 设置Y活动
   * @param state 活动状态
   * @n           1 活动
   * @n           0 不活动
   */
  void setActivityY(bool state);

  /**
   * @fn setActivityZ
   * @brief 设置Z活动
   * @param state 活动状态
   * @n           1 活动
   * @n           0 不活动
   */
  void setActivityZ(bool state);

  /**
   * @fn setInactivityX
   * @brief 设置X轴不活动
   * @param state 活动状态
   * @n           0 活动
   * @n           1 不活动
   */
  void setInactivityX(bool state);

  /**
   * @fn setInactivityY
   * @brief 设置Y轴不活动
   * @param state 活动状态
   * @n           0 活动
   * @n           1 不活动
   */
  void setInactivityY(bool state);

  /**
   * @fn setInactivityZ
   * @brief 设置Z轴不活动
   * @param state 活动状态
   * @n           0 活动
   * @n           1 不活动
   */
  void setInactivityZ(bool state);

  /**
   * @fn isActivitySourceOnX
   * @brief 活动源在X上吗
   * @return  是否在X上
   * @retval  1 在
   * @retval  0 不在
   */
  bool isActivitySourceOnX(void);

  /**
   * @fn isActivitySourceOnY
   * @brief 活动源在Y上吗
   * @return  bool类型，表示是否在Y上
   * @retval  1 在
   * @retval  0 不在
   */
  bool isActivitySourceOnY(void);

  /**
   * @fn isActivitySourceOnZ
   * @brief 活动源在Z上吗
   * @return  bool类型，表示是否在Z上
   * @retval  1 在
   * @retval  0 不在
   */
  bool isActivitySourceOnZ(void);

  /**
   * @fn isTapSourceOnX
   * @brief 点击源是否在X上
   * @return  bool类型，表示点击源是否在X上
   * @retval  1 在
   * @retval  0 不在
   */
  bool isTapSourceOnX(void);

  /**
   * @fn isTapSourceOnY
   * @brief 点击源是否在Y上
   * @return  bool类型，表示点击源是否在Y上
   * @retval  1 在
   * @retval  0 不在
   */
  bool isTapSourceOnY(void);

  /**
   * @fn isTapSourceOnZ
   * @brief 点击源是否在Z上
   * @return  bool类型，表示点击源是否在Z上
   * @retval  1 在
   * @retval  0 不在
   */
  bool isTapSourceOnZ(void);

  /**
   * @fn isAsleep
   * @brief 点击源是否休眠
   * @return  bool类型，表示休眠状态
   * @retval  1 休眠
   * @retval  0 不休眠
   */
  bool isAsleep(void);

  /**
   * @fn isLowPower
   * @brief 是否处于低功耗模式
   * @return  bool类型，表示模式
   * @retval  0 正常模式
   * @retval  1 低功耗模式
   */
  bool isLowPower(void);

  /**
   * @fn setLowPower
   * @brief 设置低功耗模式
   * @param state 功耗模式
   * @n           0 正常模式
   * @n           1 低功耗模式
   */
  void setLowPower(bool state);

  /**
   * @fn getRate
   * @brief 获取采集速率
   * @return  float类型，表示采集速率
   */
  float getRate(void);

  /**
   * @fn setRate
   * @brief 设置采集速率
   * @param rate 采集速率
   */
  void setRate(float rate);

  /**
   * @fn setBwcode
   * @brief 设置数据速率和功率模式
   * @param bw_code 速率和功率
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
   * @brief 获取数据速率和功率模式
   * @return  uint8_t类型
   */
  uint8_t getBwcode(void);

  /**
   * @fn getInterruptSource(void)
   * @brief 获取中断源
   * @return  uint8_t类型,表示中断源
   */
  uint8_t getInterruptSource(void);

  /**
   * @fn getInterruptSource(uint8_t interruptBit)
   * @brief 获取是否开启中断源
   * @param   interruptBit 中断位
   * @return  bool类型,表示是否开启中断源
   * @retval  true 中断
   * @retval  false 不中断
   */
  bool getInterruptSource(uint8_t interruptBit);

  /**
   * @fn getInterruptMapping
   * @brief 获取中断映射图
   * @param   interruptBit 中断位
   * @return  bool类型，表示获取是否成功
   * @retval  true 成功
   * @retval  false 失败
   */
  bool getInterruptMapping(uint8_t interruptBit);

  /**
   * @fn setInterruptMapping
   * @brief 设置中断映射图
   * @param   interruptBit 中断位
   * @param   interruptPin 中断引脚
   */
  void setInterruptMapping(uint8_t interruptBit, bool interruptPin);

  /**
   * @fn isInterruptEnabled
   * @brief 中断是否使能
   * @param   interruptBit 中断位
   * @return  bool类型，表示中断是否使能
   * @retval  true 使能
   * @retval  false 没使能
   */
  bool isInterruptEnabled(uint8_t interruptBit);

  /**
   * @fn setInterrupt
   * @brief 设置中断是否使能
   * @param   interruptBit 中断位
   * @param   state 状态
   * @n       true  使能
   * @n       false 不使能     
   */
  void setInterrupt(uint8_t interruptBit, bool state);

  /**
   * @fn getRangeSetting
   * @brief 获取范围设置项
   * @param   rangeSetting 用来存储范围设置项
   */
  void getRangeSetting(uint8_t *rangeSetting);

  /**
   * @fn setRangeSetting
   * @brief 设置范围设置项
   * @param   val 设置项
   */
  void setRangeSetting(int val);

  /**
   * @fn getInterruptLevelBit
   * @brief 获取INT_INVERT位的状态
   * @return  bool类型，INT_INVERT位状态
   */
  bool getInterruptLevelBit(void);

  /**
   * @fn setInterruptLevelBit
   * @brief 设置INT_INVERT位的状态
   * @param interruptLevelBit INT_INVERT位状态
   */
  void setInterruptLevelBit(bool interruptLevelBit);

  /**
   * @fn getFullResBit
   * @brief 获取FULL_RES位的状态
   * @return  bool类型，FULL_RES位的状态
   */
  bool getFullResBit(void);

  /**
   * @fn setFullResBit
   * @brief 设置FULL_RES位的状态
   * @param fullResBit FULL_RES位的状态
   */
  void setFullResBit(bool fullResBit);

  /**
   * @fn getJustifyBit
   * @brief 获取对齐位的状态
   * @return  bool类型，对齐位的状态
   */
  bool getJustifyBit(void);

  /**
   * @fn setJustifyBit
   * @brief 设置对齐位的状态
   * @param justifyBit 对齐位的状态
   */
  void setJustifyBit(bool justifyBit);

  /**
   * @fn RPCalculate
   * @brief 获取三轴加速度的数据，按照R-xyz旋转顺序时的Roll及Pitch角
   * @param data_buf  三轴加速度实际数据
   */
  void RPCalculate(int*data_buf);

  /**
   * @fn triggered
   * @brief 检测中断触发源
   * @param interrupts 获取到的中断源寄存器的数值
   * @param mask 需要检测的目标掩码
   */
  bool triggered(byte interrupts, int mask);

  /**
   * @fn inactivityInt
   * @brief 设置是否开启中断
   * @param status 获取到的中断源寄存器的数值
   */
  void inactivityInt(bool status);

  /**
   * @fn activityInt
   * @brief 设置是否开启中断
   * @param status 获取到的中断源寄存器的数值
   */
  void activityInt(bool status);

  /**
   * @fn freeFallInt
   * @brief 设置自由落体事件是否开启中断
   * @param status 获取到的中断源寄存器的数值
   */
  void freeFallInt(bool status);

  /**
   * @fn doubleTapInt
   * @brief 设置双击事件是否开启中断
   * @param status 获取到的中断源寄存器的数值
   */
  void doubleTapInt(bool status);

  /**
   * @fn singleTapInt
   * @brief 设置单击事件是否开启中断
   * @param status 获取到的中断源寄存器的数值
   */
  void singleTapInt(bool status);
  
```  

## 兼容性

主板               | 通过  | 未通过   | 未测试   | 备注
------------------ | :----------: | :----------: | :---------: | -----
Arduino uno        |      √       |              |             | 
Mega2560        |      √       |              |             | 
Leonardo        |      √       |              |             | 
ESP32           |      √       |              |             | 
ESP8266           |      √       |              |             | 
Micro:bit           |      √       |              |             | 

## 历史

- 2022/2/25 - 2.0.0 版本

## 创作者

Written by Peng Kaixing(kaixing.peng@dfrobot.com), 2020. (Welcome to our [website](https://www.dfrobot.com/))
