import UtilityFunctions as UF
import numpy as np
from scipy.signal import find_peaks, welch

def GetRespSignal(df, mode="z"):
    mode = mode.lower()
    if mode == "z":
        return df["az"].to_numpy(), "Z-axis (g)"
    elif mode == "mag":
        mag = UF.ComputeMagnitude(df["ax"].to_numpy(), df["ay"].to_numpy(), df["az"].to_numpy())
        return mag, "Accel Magnitude (g)"
    else:
        raise ValueError('mode must be "z" or "mag"')
    
def EstimateRRTime(peaks, time):
    # Breaths per minute from peak intervals
    if len(peaks) < 2:
        return None
    intervals = np.diff(time[peaks])  # in seconds
    avgBreathInterval = np.mean(intervals)
    return 60.0 / avgBreathInterval if avgBreathInterval > 0 else None

def EstimateRRFreq(signal, samplingFreq, window=30, low=0.05, high=0.8):
    f, Pxx = welch(signal, samplingFreq, nperseg=int(window*samplingFreq))
    mask = (f >= low) & (f <= high)
    domFreq = f[mask][np.argmax(Pxx[mask])]
    return domFreq * 60.0  # convert to breaths per minute