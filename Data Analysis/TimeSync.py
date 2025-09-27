import serial
import threading
import time
import csv
import keyboard

# Configuration
PORT_ESP32 = 'COM10' 
PORT_MANUAL = 'COM4'
BAUDRATE = 115200
OUTPUT_FILE = 'timesync_data.csv'
LAPTOP_MODE = True # When this is true, ESP32 + Laptop spacebar for manual readings.
RECORDING_FREQUENCY = 50 # Hz
RECORDING_PERIOD = 1 / RECORDING_FREQUENCY
 
# Shared buffer
dataBuffer = []
lock = threading.Lock()

running  = True

def read_serial(port, label):
    ser = serial.Serial(port, BAUDRATE, timeout=1)

    while running:
        try :
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue
            timestamp = time.time()
            with lock:
                dataBuffer.append((timestamp, label, line))
            time.sleep(RECORDING_PERIOD)                
        except Exception as e:
            print(f"Error reading from {label}: {e}")
            break
    ser.close()
    
def read_spacebar(label = "Manual"):
    """Simulate manual breathing input from the spacebar (1 = inhaling, 0 = exhaling )"""
    while running:
        try:
            timestamp = time.time()
            if keyboard.is_pressed("space"):
                value = 1
            else:
                value = 0
            with lock:
                dataBuffer.append((timestamp, label, value))
            time.sleep(RECORDING_PERIOD)                
        except Exception as e:
            print(f"Error reading spacebar: {e}")
            break
        
# Set up  the threads 
threads = []
thread_esp32 = threading.Thread(target=read_serial, args=(PORT_ESP32, 'ESP32'))
threads.append(thread_esp32)

if LAPTOP_MODE:
    thread_manual = threading.Thread(target=read_spacebar, args=('Manual',))
else: 
    thread_manual = threading.Thread(target=read_serial, args=(PORT_MANUAL, 'Manual'))

threads.append(thread_manual)


# Start all the threads

for thread in threads:
    thread.start()
    
print("Recording... Crtl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    running = False
    for thread in threads:
        thread.join()

# Write to CSV
with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Source', 'Data'])
    with lock:
        writer.writerows(dataBuffer)

print(f"Saved {len(dataBuffer)} records to {OUTPUT_FILE}")