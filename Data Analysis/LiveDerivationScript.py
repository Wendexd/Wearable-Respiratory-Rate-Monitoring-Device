import serial
import numpy as np
from math import isfinite
import LiveDerivationClass as LDC
import UtilityFunctions as UF
import IMUDerivedRR as IMU
import keyboard

def ParseESP32Line(line):

    parts = line.strip().split(",")
    if len(parts) < 2:
        print("Incomplete Line Received")
        return None # Malformed line
    
    try:
        timestamp = float(parts[0])
    except ValueError:
        print("Value Error in timestamp")
        return None
    
    kind = parts[1].upper()

    def f(x):
        return float(x) if x != "" else np.nan
    
    if kind == "IMU":
        if len(parts) < 11:
            print("Incomplete IMU line")
            return None
        ax, ay, az = f(parts[2]), f(parts[3]), f(parts[4])
        gx, gy, gz = f(parts[5]), f(parts[6]), f(parts[7])
        roll = f(parts[8])
        pitch = f(parts[9])
        yaw = f(parts[10])  # yaw/head
        ecg = None
    elif kind == "ECG":
        if len(parts) < 11:
            print("Incomplete ECG line")
            return None
        ax, ay, az = np.nan, np.nan, np.nan
        gx, gy, gz = np.nan, np.nan, np.nan
        roll = np.nan
        pitch = np.nan
        yaw = np.nan
        ecg = parts[10] # Messed up the csv, this should have been at index 11 but oh well
    else:
        print(f"Unknown data type in line {kind}")
        return None # Malformed line

    return {
        "timestamp": timestamp,
        "type": kind, 
        "ax": ax,
        "ay": ay,
        "az": az,
        "gx": gx,
        "gy": gy,
        "gz": gz,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "ecg": ecg
    }

    

def RunLiveRR(port, baudrate=115200, fsIMU=50, fsECG=500, window=30, hop=1):
    """
    Connect to ESP32 serial port and derive live respiratory rate
    """
    ser = serial.Serial(port, baudrate, timeout=0.5)
    liveDeriv = LDC.LiveDerivation(fsIMU, fsECG, slidingWindow=window, hopInterval=hop)

    # Running time origin
    t0 = None

    print("Live RR: streaming... (Ctrl+C to stop)")
    try:
        while True:
            line = ser.readline().decode('utf-8', errors="ignore").strip()
            if not line:
                print("No data received...")
                continue
            
            data = ParseESP32Line(line)
            if data is None:
                continue

            if t0 is None:
                t0 = data["timestamp"]
            
            if data["type"] == "IMU":
                ax, ay, az = data["ax"], data["ay"], data["az"]
                devicePitch = data["pitch"]
                _, accelPitch = IMU.AccelTilt(np.array([ax]), np.array([ay]), np.array([az]))
                accelPitch = accelPitch[0]
                rrEstimate = liveDeriv.Update(data["az"], devicePitch, accelPitch, keyboard.is_pressed("space"))

                if rrEstimate is not None and isfinite(rrEstimate["z"]["RR"]):
                    z = rrEstimate["z"]["RR"]
                    pitch = rrEstimate["pitch"]["RR"]
                    accelPitch = rrEstimate["accelPitch"]["RR"]
                    manualBrpm = rrEstimate["manualBrpm"]
                    def fmt(x):
                        return f"{x:.2f}" if isfinite(x) and x != 0 else "N/A"
                    print(f"RR Estimates (brpm) - Z: {fmt(z)}, Pitch: {fmt(pitch)}, AccelPitch: {fmt(accelPitch)}, Manual: {fmt(manualBrpm)}")
    except KeyboardInterrupt:
        print("\nStopping")

    finally:
        ser.close()


if __name__ == "__main__":
    RunLiveRR("COM4") # Don't forget to set port correctly
