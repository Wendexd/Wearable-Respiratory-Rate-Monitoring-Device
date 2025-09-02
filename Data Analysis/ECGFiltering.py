import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# 1. Load your data
csv1 = pd.read_csv("Session1.csv")
t = csv1['Time'] / 1000.0  # convert ms to seconds if needed
fs = 50                 # sampling frequency in Hz

# 2. Design a 4th-order Butterworth low-pass filter at 1 Hz
cutoff = 1               # cutoff frequency in Hz
nyq = 0.5 * fs             # Nyquist frequency
normal_cutoff = cutoff / nyq
b, a = butter(N=4, Wn=normal_cutoff, btype='low', analog=False)

# 3. Apply zero-phase filtering to your ECG (“heart”) signal
ecg = csv1['heart'].values
ecg_filt = filtfilt(b, a, ecg)

# 4. Plot raw vs. filtered ECG alongside manual breathing
fig, ax1 = plt.subplots()
ax1.plot(t, ecg_filt, color='red', label=f'Filtered ECG (≤{cutoff} Hz)')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('ECG ADC Value (0-1023)')
ax1.set_ylim(200,400)
ax1.legend(loc='upper left')
plt.xlim(5, 61)

ax2 = ax1.twinx()
ax2.plot(t, csv1['manual'], color='blue', label='Manual')
ax2.set_ylabel('Manual Signal (0=Exhalation, 1=Inhalation)')
ax2.legend(loc='upper right')

plt.title('Heart Activity (Low-Pass ≤1 Hz) and Manual Breathing Signal')
plt.tight_layout()
plt.show()
