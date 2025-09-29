import serial
import threading
import time
import csv
import keyboard
from datetime import datetime
from pathlib import Path

# Configuration
PORT_ESP32 = 'COM4' 
PORT_MANUAL = 'COM4'
BAUDRATE = 115200
OUTPUT_FILE = 'timesync_data.csv'
LAPTOP_MODE = True # When this is true, ESP32 + Laptop spacebar for manual readings.
RECORDING_FREQUENCY = 50 # Hz
RECORDING_PERIOD = 1 / RECORDING_FREQUENCY
FOLDER_PATH = Path("Recording Sessions")
 
# Shared buffer
dataBuffer = []
lock = threading.Lock()

running  = True

def initSerial(port, baudrate):
    """Initialize and return a serial connection."""
    try :
        return serial.Serial(port, baudrate, timeout=0.1)
    except Exception as e:
        print(f"Error opening serial port {port}: {e}")
        exit(1)

def readESP32(ser, log_file="esp32_log.txt"):
    """Read one line from ESP32 serial port."""
    line = ser.readline().decode('utf-8').strip()
    if not line:
        return ""
    
    parts = line.split(",")
    if len(parts) != 10:  # EXPECTED number of values from ESP32
        # Log malformed lines for debugging
        with open(log_file, "a") as f:
            f.write(f"{time.time()}: {line}\n")
        print(f"[WARN] Skipping malformed ESP32 line ({len(parts)} fields): {line}")
        return ""
    
    return line


def readManual(manualSerial = None):
    """Read manual breathing input (spacebar pressed = 1, else 0)."""
    if LAPTOP_MODE:
        return 1 if keyboard.is_pressed("space") else 0
    
    if manualSerial and manualSerial.in_waiting > 0:
        line = manualSerial.readline().decode('utf-8').strip()
        return 1 if line else 0



def recordData(output_file=OUTPUT_FILE, freq=RECORDING_FREQUENCY):
    """Main loop to record ESP32 + manual data."""
    ser = initSerial(PORT_ESP32, BAUDRATE)
    data_buffer = []
    period = 1 / freq

    print("Recording... Press Ctrl+C to stop.")

    try:
        while True:
            timestamp = time.time()
            esp_data = readESP32(ser)
            manual_data = readManual()

            # Save row
            if esp_data:  # Only save if we got valid ESP32 data
                data_buffer.append((timestamp, esp_data, manual_data))
            time.sleep(period)

    except KeyboardInterrupt:
        print("\nStopping recording...")
    finally:
        ser.close()

    write_csv(output_file, data_buffer)
    print(f"Saved {len(data_buffer)} records to {output_file}")


def write_csv(filename, data):
    """Write buffered data to CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'ESP32_Data', 'Manual'])
        writer.writerows(data)


if __name__ == "__main__":
    # Get current date and time
    now = datetime.now()

    FOLDER_PATH.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

    # Format it into a string
    fileName = now.strftime("recording_%Y%m%d_%H%M%S.csv")
    filePath = FOLDER_PATH / fileName
    recordData(filePath)