# DFRobot_ITG3200

- [English Version](./README.md)

DFrobot的高集成度低成本的10自由度传感器,集合了ADXL345加速度计、QMC5883L磁罗盘、ITG3205陀螺仪以及BMP280气压传感器和温度传感器。内置了低噪声的低压线性稳压器，还扩展了电源电压输入范围，支持3V-5V电源电压。同时，10自由度IMU也可以直接和Arduino控制板兼容。

![正反面svg效果图](./resources/images/SEN0140.png)

## 产品链接(https://www.dfrobot.com.cn/goods-640.html)

    SKU: SEN0140

## 目录

* [概述](#概述)
* [库安装](#库安装)
* [方法](#方法)
* [兼容性](#兼容性y)
* [历史](#历史)
* [创作者](#创作者)

## 概述

这个库提供了ITG3200陀螺仪获取X,Y,Z三轴的数据的库和例程

## 库安装

使用此库前，请首先下载库文件，将其粘贴到\Arduino\libraries目录中，然后打开examples文件夹并在该文件夹中运行演示。

## 方法

```C++

    /**
     * @fn begin
     * @param _SRateDiv 采样率分频器
     * @param _Range 陀螺全量程
     * @param _filterBW 数字低通滤波器带宽和采样率  
     * @param _ClockSrc 时钟源-用户参数
     * @param _ITGReady 使能中断寄存器
     * @param _INTRawDataReady 使能数据准备寄存器
     * @return bool类型，表示返回初始化的状态
     * @retval true 初始化成功
     * @retval false 初始化失败
     */
    bool begin(uint8_t _SRateDiv = NOSRDIVIDER, uint8_t _Range = RANGE2000, uint8_t _filterBW = BW256_SR8, uint8_t _ClockSrc = PLL_XGYRO_REF, bool _ITGReady = true, bool _INTRawDataReady = true);

    /**
     * @fn setSamplerateDiv
     * @brief 设置陀螺仪采样速率
     * @param _SampleRate
     * @n     采样率分频器: 0 to 255
     * @n     计算:Fsample = Finternal / (_SampleRate+1)
     * @n     Finternal is 1kHz or 8kHz
     */
    void setSamplerateDiv(uint8_t _SampleRate);

    /**
     * @fn getSamplerateDiv
     * @brief 得到陀螺仪采样率
     * @return uint8_t
     */
    uint8_t getSamplerateDiv(void);

    /**
     * @fn setIntlogicLvl
     * @brief 中断配置
     * @param bool
     * @n ACTIVE_ONHIGH 中断高电平有效
     * @n ACTIVE_ONLOW 中断低电平有效
     */
    void setIntlogicLvl(bool _State);

    /**
     * @fn isIntactiveOnlow
     * @brief 模块是否是中断触发时为低电平
     * @return bool
     * @retval true 中断高电平有效
     * @retval false 中断低电平有效
     */
    bool isIntactiveOnlow(void);

    /**
     * @fn setIntdriveType
     * @brief 设置中断引脚的状态
     * @param _State 引脚的状态
     * @n OPEN_DRAIN 开漏输出
     * @n PUSH_PULL 推挽输出
     */
    void setIntdriveType(bool _State);

    /**
     * @fn isIntopenDrain
     * @brief 中断引脚是否是开漏输出
     * @return bool
     * @retval true 是
     * @retval false 否
     */
    bool isIntopenDrain(void);

    /**
     * @fn setItgready
     * @brief 当设备准备好时，使能中断  
     * @param _State
     * @n     true   打开
     * @n     false  关闭
     */
    void setItgready(bool _State);

    /**
     * @fn isItgreadyOn
     * @brief 如果中断开关已打开
     * @return true yes
     * @return false no
     */
    bool isItgreadyOn(void);

    /**
     * @fn isItgready
     * @brief 中断是否使能
     * @return bool
     * @retval true 使能
     * @retval false 不使能
     */
    bool isItgready(void);

    /**
     * @fn isRawdataReady
     * @brief 原始数据是否准备好
     * @return bool
     * @retval true 已经准备好
     * @retval false 没有准备好
     */
    bool isRawdataReady(void);

    /**
     * @fn readTemp
     * @brief 获取板子温度
     * @param _Temp 存储温度
     */
    void readTemp(float *_Temp);

    /**
     * @fn zeroCalibrate
     * @brief 假设陀螺仪是固定的(更新XYZ偏移量)  
     * @param totSamples
     * @param sampleDelayMS
     */
    void zeroCalibrate(unsigned int totSamples, unsigned int sampleDelayMS);

    /**
     * @fn readGyro(float *_GyroX, float *_GyroY, float *_GyroZ)
     * @brief 读deg/sec校准和比例因子
     * @param _GyroX
     * @param _GyroY
     * @param _GyroZ
     */
    void readGyro(float *_GyroX, float *_GyroY, float *_GyroZ);

    /**
     * @fn readGyro(float *_GyroXYZ)
     * @brief 读deg/sec校准和比例因子
     * @param _GyroXYZ
     */
    void readGyro(float *_GyroXYZ);          

    /**
     * @fn reset
     * @brief 复位后，所有寄存器都有默认值
     */
    void reset(void);

    /**
     * @fn isLowpower
     * @brief 查看传感器是否处于低功耗模式
     * @return bool
     * @retval true 是
     * @retval false 否
     */
    bool isLowpower(void);

    /**
     * @fn setPowerMode
     * @brief 设置功耗模式
     * @param _State 模式选择
     * @n     NORMAL
     * @n     STANDBY
     */
    void setPowermode(bool _State);

    /**
     * @fn isXgyroStandby
     * @brief 陀螺仪X方向上的数据是否已经准备好
     * @return bool
     * @retval true 准备好了
     * @retval false 没准备好
     */
    bool isXgyroStandby(void);

    /**
     * @fn isYgyroStandby
     * @brief 陀螺仪Y方向上的数据是否已经准备好
     * @return bool
     * @retval true 准备好了
     * @retval false 没准备好
     */
    bool isYgyroStandby(void);

    /**
     * @fn isZgyroStandby
     * @brief 陀螺仪Z方向上的数据是否已经准备好
     * @return bool
     * @retval true 没准备好
     * @retval false 没准备好
     */
    bool isZgyroStandby(void);

    /**
     * @fn setXgyroStandby
     * @brief 设置X方向待机模式，待机模式将不会获取X方向的数据
     * @param _Status
     * @n     NORMAL 使能
     * @n     STANDBY 不使能
     */
    void setXgyroStandby(bool _Status);

    /**
     * @fn setYgyroStandby
     * @brief 设置Y方向待机模式，待机模式将不会获取X方向的数据
     * @param _Status
     * @n     NORMAL 使能
     * @n     STANDBY 不使能
     */
    void setYgyroStandby(bool _Status);

    /**
     * @fn setZgyroStandby
     * @brief 设置Z方向待机模式，待机模式将不会获取X方向的数据
     * @param _Status
     * @n     NORMAL 使能
     * @n     STANDBY 不使能
     */
    void setZgyroStandby(bool _Status);

    /**
     * @fn setFilterBW
     * @brief 设置滤波器带宽
     * @param _BW 带宽
     */
    void setFilterBW(uint8_t _BW);

    /**
     * @fn getFilterBW
     * @brief 获取滤波器带宽
     * @return uint8_t
     */
    uint8_t getFilterBW(void);

    /**
     * @fn getFSrange
     * @brief 获取陀螺仪量程
     * @return uint8_t
     */
    uint8_t getFSrange(void);

    /**
     * @fn isLatchuntilCleared
     * @brief 如果闩锁模式是闩锁，直到中断被清除  
     * @return true 插销直到中断被清除
     * @return false 50us 脉冲
     */
    bool isLatchuntilCleared(void);

    /**
     * @fn isAnyregClrmode
     * @brief 如果锁存清除方法是任何寄存器读取
     * @return true 任何寄存器读
     * @return false 状态寄存器只读
     */
    bool isAnyregClrmode(void);

    /**
     * @fn getClocksource
     * @brief 获取时钟源
     * @return uint8_t
     */
    uint8_t getClocksource(void);

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

- 2022/3/2 - 2.0.0 版本

## 创作者

Written by Peng Kaixing(kaixing.peng@dfrobot.com), 2020. (Welcome to our [website](https://www.dfrobot.com/))