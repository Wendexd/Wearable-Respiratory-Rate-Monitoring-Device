import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv1 = pd.read_csv("Session1.csv")

# Plot accelerometer data with manual on secondary axis
fig, ax1 = plt.subplots()
ax1.plot(csv1['Time']/1000, csv1['ax'], label='ax')
ax1.plot(csv1['Time']/1000, csv1['ay'], label='ay')
ax1.plot(csv1['Time']/1000, csv1['az'], label='az')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Acceleration (g)')
ax1.legend(loc='upper left')
plt.xlim(0, 61)

ax2 = ax1.twinx()
ax2.plot(csv1['Time']/1000, csv1['manual'], color='blue', label='Manual')
ax2.set_ylabel('Manual Signal (0 = Exhalation, 1 = Inhalation)')
ax2.legend(loc='upper right')

plt.title('Accelerometer Data and Manual Breathing Signal')
plt.tight_layout()
plt.show()

# Plot heart rate with manual on secondary axis
fig, ax1 = plt.subplots()
ax1.plot(csv1['Time']/1000, csv1['heart'], color='red', label='Heart Rate')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Heart Rate Activity (ADC Value)')
ax1.legend(loc='upper left')
plt.xlim(0, 61)

ax2 = ax1.twinx()
ax2.plot(csv1['Time']/1000, csv1['manual'], color='blue', label='Manual')
ax2.set_ylabel('Manual Signal (0 = Exhalation, 1 = Inhalation)')
ax2.legend(loc='upper right')

plt.title('Heart Rate and Manual Breathing Signal')
plt.tight_layout()
plt.show()