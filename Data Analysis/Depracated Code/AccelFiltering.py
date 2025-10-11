import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# 1. Load your data
csv1 = pd.read_csv("Session1.csv")
t = csv1['Time'] / 1000.0    # convert ms to seconds if needed
fs = 50.0                    # sampling frequency in Hz

# 2. Design a 4th-order Butterworth low-pass filter at 1 Hz
cutoff = 2                 # cutoff frequency in Hz
nyq = 0.5 * fs               # Nyquist frequency
normal_cutoff = cutoff / nyq
b, a = butter(N=4, Wn=normal_cutoff, btype='low', analog=False)

# 3. Apply zero-phase filtering to ECG (“heart”) signal

# 4. Apply the same filter to each accelerometer axis
ax = csv1['ax'].values
ay = csv1['ay'].values
az = csv1['az'].values
manual = csv1['manual'].values if 'manual' in csv1.columns else None
has_manual = manual is not None

# ax_filt = filtfilt(b, a, ax)
# ay_filt = filtfilt(b, a, ay)
# az_filt = filtfilt(b, a, az)

# # 5. Plot raw vs. filtered accelerometer data with manual on a secondary axis
# fig, ax1 = plt.subplots()
# ax1.plot(t, ax_filt, color='blue',    label=f'ax (≤{cutoff} Hz)')
# ax1.plot(t, ay_filt, color='orange',  label=f'ay (≤{cutoff} Hz)')
# ax1.plot(t, az_filt, color='green',   label=f'az (≤{cutoff} Hz)')

# ax1.set_xlabel('Time (s)')
# ax1.set_ylabel('Acceleration (g)')
# plt.xlim(0, 61)
# ax1.legend(loc='upper left')

# ax2 = ax1.twinx()
# ax2.plot(t, csv1['manual'], color='blue', label='Manual')
# ax2.set_ylabel('Manual Signal (0=Exhale,1=Inhale)')
# ax2.legend(loc='upper right')

# plt.title(f'Accelerometer (Filtered ≤{cutoff} Hz) and Manual Breathing Signal')
# plt.tight_layout()
# plt.show()

def bandpass_filter(data, fs, low=0.15, high=0.40, order=4):
    nyq = 0.5 * fs
    b, a = butter(N=order, Wn=[low / nyq, high / nyq], btype='band')
    return filtfilt(b, a, data)

sig_filt = bandpass_filter(az, fs, low=0.15, high=0.40)  # Use az as the chosen axis


def rr_from_autocorr(x, fs, min_bpm=6, max_bpm=30):
    # Search lags 2–10 s by default (6–30 bpm)
    n = len(x)
    if n < fs * 5:  # need enough data
        return 0.0
    ac = np.correlate(x, x, mode='full')[n-1:]
    lags = np.arange(ac.size)/fs
    min_lag = int((60/max_bpm)*fs)
    max_lag = int((60/min_bpm)*fs)
    if max_lag <= min_lag or max_lag >= len(ac):
        return 0.0
    seg = ac[min_lag:max_lag]
    peak_idx = np.argmax(seg)
    best_lag = (min_lag + peak_idx) / fs
    return 60.0 / best_lag if best_lag > 0 else 0.0

def rr_from_fft(x, fs, f_low=0.15, f_high=0.40):
    n = len(x)
    if n == 0:
        return 0.0
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(n, 1/fs)
    mask = (freqs >= f_low) & (freqs <= f_high)
    if not np.any(mask):
        return 0.0
    f_peak = freqs[mask][np.argmax(np.abs(X[mask]))]
    return f_peak * 60.0

ac_bpm = rr_from_autocorr(sig_filt, fs, min_bpm=6, max_bpm=30)
fft_bpm = rr_from_fft(sig_filt, fs, f_low=0.15, f_high=0.40)

# Accept plausible values and average
valid = []
if 8 < ac_bpm < 26: valid.append(ac_bpm)
if 8 < fft_bpm < 26: valid.append(fft_bpm)
final_bpm = np.mean(valid) if valid else 0.0

# --- 6) Optional peaks for visual sanity-check ---
peaks, _ = find_peaks(sig_filt, distance=int(fs*60/30))  # min distance ~ fastest 30 bpm
peak_times = t[:len(sig_filt)][peaks] if len(t) >= len(sig_filt) else peaks/fs

# --- 7) Plot ---
plt.figure(figsize=(11,7))

# Raw signal (top)
plt.subplot(3,1,1)
plt.plot(t, az, label='Abdomen raw (chosen axis)')
plt.title('Raw Abdomen Acceleration')
plt.xlabel('Time (s)')
plt.ylabel('g')
plt.xlim(t[0], t[0]+60)
plt.legend()

# (middle subplot left intentionally unused in your script)
plt.subplot(3,1,2)
plt.axis('off')

# Filtered + peaks + manual overlay (bottom)
ax = plt.subplot(3,1,3)
line_resp, = ax.plot(t[:len(sig_filt)], sig_filt, label='Filtered respiration (0.15–0.40 Hz)')
if len(peak_times) > 0:
    line_peaks, = ax.plot(peak_times, sig_filt[peaks], 'o', ms=4, label='Detected peaks')

ax.set_title(f'Estimated RR: {final_bpm:.1f} bpm  (AC={ac_bpm:.1f}, FFT={fft_bpm:.1f})')
ax.set_xlabel('Time (s)')
ax.set_ylabel('a.u.')
ax.set_xlim(t[0], t[0]+60)

# Overlay manual signal on a secondary y-axis (no rescaling needed)
if has_manual:
    ax_manual = ax.twinx()
    line_manual, = ax_manual.plot(t[:len(sig_filt)],
                                  manual[:len(sig_filt)],
                                  linestyle='--', alpha=0.7, label='Manual (0/1)')
    ax_manual.set_ylabel('Manual (0/1)')
    # Merge legends from both axes
    handles_left, labels_left = ax.get_legend_handles_labels()
    handles_right, labels_right = ax_manual.get_legend_handles_labels()
    ax.legend(handles_left + handles_right, labels_left + labels_right, loc='upper right')
else:
    ax.legend(loc='upper right')

plt.tight_layout()
plt.show()