import serial
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Serial Config
PORT = "COM3"     
BAUD = 115200


# Buffer for live plot (Last N samples)
N = 1500 # 30s @ 50Hz
t_buf = deque(maxlen=N)
ax_buf = deque(maxlen=N)
ay_buf = deque(maxlen=N)
az_buf = deque(maxlen=N)

ser = serial.Serial(PORT, BAUD, timeout=1)

# Setup plot 
plt.ion()
fig, ax = plt.subplots()
line_ax, = ax.plot([], [], label="ax (g)")
line_ay, = ax.plot([], [], label="ay (g)")
line_az, = ax.plot([], [], label="az (g)")
ax.legend()
ax.set_xlabel("Sample")
ax.set_ylabel("Acceleration (g)")

while True:
    try:
        line = ser.readline().decode("utf-8").strip()
        if not line or line.startswith("t_ms"):  # skip header
            continue
        parts = line.split(",")
        if len(parts) < 4:
            continue

        # unpack fields you care about
        t_ms = float(parts[0])
        ax_g = float(parts[1])
        ay_g = float(parts[2])
        az_g = float(parts[3])

        # append to buffers
        t_buf.append(t_ms)
        ax_buf.append(ax_g)
        ay_buf.append(ay_g)
        az_buf.append(az_g)

        # update plot
        line_ax.set_data(range(len(ax_buf)), ax_buf)
        line_ay.set_data(range(len(ay_buf)), ay_buf)
        line_az.set_data(range(len(az_buf)), az_buf)
        ax.relim(); ax.autoscale_view()
        plt.pause(0.001)

    except KeyboardInterrupt:
        break

ser.close()
