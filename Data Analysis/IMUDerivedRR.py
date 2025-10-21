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

    if mode == "pitch":
        return df["pitch"].to_numpy(), "Pitch (rad)"
    elif mode == "accelpitch":
        roll, pitch = AccelTilt(ax, ay, az) # Not finished
        return pitch, "Accel Pitch (rad)"
    elif mode == "z":
        return df["az"].to_numpy(), "Z-axis (g)"
    elif mode == "mag":
        mag = UF.ComputeMagnitude(df["ax"].to_numpy(), df["ay"].to_numpy(), df["az"].to_numpy())
        return mag, "Accel Magnitude (g)"
    else:
        raise ValueError('mode must be "z" or "mag"')
    
def RRFromAutoCorrelation(signal, samplingFreq, minRR=6, maxRR=30):
    """Estimate respiratory rate (breaths per minute) using autocorrelation method."""
    # Auto correlation
    corr = np.correlate(signal, signal, mode='full')
    corr = corr[len(corr)//2:]
    lags = np.arange(len(corr)) / samplingFreq

    # Search between 6 and 30 breaths per minute
    minLag = int(2 * samplingFreq)  # 30 bpm
    maxLag = int(10 * samplingFreq)  # 6 bpm
    validCorr = corr[minLag:maxLag]

    if len(validCorr) == 0:
        acRate = 0
    else: 
        peakIdx, _ = find_peaks(validCorr)
        acLag = (peakIdx + minLag) / samplingFreq
        acRate = 60.0 / acLag[0] if len(acLag) > 0 else 0

    return acRate

def RRFromFFT(signal, samplingFreq):
    """Estimate respiratory rate (breaths per minute) using FFT method."""
    n = len(signal)
    if n < 10:
        return 0, 0, 0

    fft = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, 1/samplingFreq)
    mask = (freqs >= 0.15) & (freqs <= 0.4)  # 9 to 24 bpm

    if not np.any(mask):
        fftRate = 0
    else:
        peakFreq = freqs[mask][np.argmax(np.abs(fft[mask]))]
        fftRate = peakFreq * 60.0  # Convert to breaths per minute

    return fftRate

def CombineRREstimates(signal, samplingFreq):
    """Combine RR estimates from autocorrelation and FFT methods."""
    acRate = RRFromAutoCorrelation(signal, samplingFreq)
    fftRate = RRFromFFT(signal, samplingFreq)

    validRates = []
    if 8 <= acRate <= 26:
        validRates.append(acRate)
    if 8 <= fftRate <= 26:
        validRates.append(fftRate)

    if len(validRates) == 0:
        return 0, 0, 0
    
    finalRate = np.mean(validRates)
    return finalRate, acRate, fftRate

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