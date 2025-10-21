import UtilityFunctions as UF
import numpy as np
from scipy.signal import find_peaks, welch

def AccelTilt(ax, ay, az, epsilon=1e-8):
    """Compute tilt angle (radians) from vertical for each sample."""
    norm = np.sqrt(ax**2 + ay**2 + az**2) + epsilon
    axNorm = ax / norm
    ayNorm = ay / norm
    azNorm = az / norm
    roll = np.arctan2(ayNorm, azNorm)
    pitch = np.arctan2(-axNorm, np.sqrt(ayNorm**2 + azNorm**2) + epsilon)
    return roll, pitch

def GetIMUSignal(df, mode="z"):
    mode = mode.lower()
    ax = df["ax"].to_numpy(dtype=float)
    ay = df["ay"].to_numpy(dtype=float)
    az = df["az"].to_numpy(dtype=float)

    if mode == "tilt":
        roll, pitch = AccelTilt(ax, ay, az) # Not finished
    elif mode == "acceltilt":
        roll, pitch = AccelTilt(ax, ay, az)
        resp = pitch # Use pitch as respiration signal
    elif mode == "z":
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