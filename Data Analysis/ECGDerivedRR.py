import UtilityFunctions as UF
import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import interp1d


def GetRawECG(df):
    ecg = df["heart"].to_numpy()
    t = df["Time (s)"].to_numpy(dtype=float)
    return ecg, t

def DetectRRECG(signal, samplingFreq, sanityFilter=True):
    """Lightweight R-peak finder: bandpass then peaks with basic RR sanity."""
    ecgFiltered = UF.BandpassFilter(signal, samplingFreq, low=0.5, high=40.0, order=4)
    # Enforce physionlogical separation between peaks (250ms)
    distance = int(samplingFreq * 0.25)  # min Xms between beats
    # Prominenve scaled to signal dispersion to surpress noise peaks
    peakProminence = np.std(ecgFiltered) * 0.5

    peaks, _ = find_peaks(ecgFiltered, distance=distance, prominence=peakProminence)

    rPeakIndices = peaks.copy()
    # Optional sanity filter: drop improbable RR intervals (<0.3s or >6s)
    if len(peaks) >= 3 and sanityFilter:
        rrIntervalSeconds = np.diff(peaks) / samplingFreq
        keepMask = np.hstack(
            [True, # Keep first peak
            (rrIntervalSeconds > 0.3) & (rrIntervalSeconds < 6.0)])
        rPeakIndices = peaks[keepMask]

    return peaks, rPeakIndices

def DeriveEDRFromRPeaks(ecgSignal, timeSeconds, samplingFreq, respLowFreq=0.05, respHighFreq=0.8, outputTime=None):
    # 1) detect R-peaks on the ECG and get a "filtered" ECG version to sample from.
    rPeaks, rPeakIndices = DetectRRECG(ecgSignal, samplingFreq)

    # Need at least a few beats to build a breathing waveform. Also need a target time axis.
    if outputTime is None or len(rPeaks) < 2:
        return None
    
    # 2) For each dettected R-peak, get:
    # - The time of the R-peak (in seconds)
    # - The "Filtered" ECG Amplitude at that beat (This carries the respiration modulation)
    rPeakTimesSeconds = timeSeconds[rPeakIndices].astype(float)
    rPeakAmplitudes = ecgSignal[rPeakIndices].astype(float)

    # 3) Beat amplitude outlier suppression (robust to ectopy/artifacts)
    # Clip extreme values so they don't domintate the interpolation or filtering.
    lowerClip, upperClip = np.percentile(rPeakAmplitudes, [1, 99])
    rPeakAmplitudes = np.clip(rPeakAmplitudes, lowerClip, upperClip)

    # 4) We only have beat-to-beat samples. To compare with IMU or to filter,
    # we resample this irregular series onto a *uniform* time base = outputTime
    # (Typicall the IMU time vector)
    interpolateRampToUniform = interp1d(
        rPeakTimesSeconds,
        rPeakAmplitudes,
        kind="linear",
        fill_value="extrapolate",
        assume_sorted=True
    )
    edrUniform = interpolateRampToUniform(outputTime)

    # 5) Determine the sampling rate of the uniform axis so we can filter correctly.
    dtSeconds = np.median(np.diff(outputTime))
    if not np.isfinite(dtSeconds) or dtSeconds <= 0:
        return None
    samplingFreq = 1.0 / dtSeconds

    # 6) The beat amplitude trace still has slow drift and residual noise.
    # Bandpass in the respiratory band (default 0.1-0.5Hz) to get the final EDR waveform.
    edrFiltered = UF.BandpassFilter(
        edrUniform,
        samplingFreq=samplingFreq,
        low=respLowFreq,
        high=respHighFreq,
        order=4
    )
    
    return edrFiltered

def QrsBandpass(ecg, fs, low=0.5, high=40.0, order=4):
    return UF.BandpassFilter(ecg, fs, low, high, order)

def DetectRPeaks(ecgFiltered, fs):
    distance = int(fs * 0.25)  # min 250ms between beats
    peakProminence = np.std(ecgFiltered) * 0.5
    peaks, _ = find_peaks(ecgFiltered, distance=distance, prominence=peakProminence)
    return peaks

def ResampleToUniform(beatTimeS, beatValues, uniformFs, tStart, tEnd):
    if tStart is None:
        tStart = float(beatTimeS[0])
    if tEnd is None:
        tEnd = float(beatTimeS[-1])
    
    uniformTimeS = np.arange(tStart, tEnd, 1.0/uniformFs)
    interpolateFunc = interp1d(
        beatTimeS,
        beatValues,
        kind="linear",
        fill_value="extrapolate",
        assume_sorted=True
    )

    return uniformTimeS, interpolateFunc(uniformTimeS)

def AdaptiveUpcrossCount(windowValues, windowTimeS):
    vMax = np.max(windowValues)
    vAvg = np.mean(windowValues)
    thresholdMax = 0.25 * vMax + 0.75 * vAvg
    thresholdAvg = vAvg

    windowLenS = max(windowTimeS[-1] - windowTimeS[0], 1e-6)  # avoid div by zero

    # provisional at average-based threshold
    provisional = np.sum(
        (windowValues[1:] >= thresholdAvg) & (windowValues[:-1] < thresholdAvg)
    )

    provisionalBrpm = provisional * (60.0 / windowLenS)

    thresholdUsed = thresholdMax if provisionalBrpm > 20 else thresholdAvg

    crossings = np.sum(
        (windowValues[1:] >= thresholdUsed) & (windowValues[:-1] < thresholdUsed)
    )
    brpm = crossings * (60.0 / windowLenS)
    return brpm, crossings, thresholdUsed

def EstimateRRWindows(uniformTimeS, edrUniform, winSeconds, hopSeconds, estimator=AdaptiveUpcrossCount):
    results = []
    start_time = float(uniformTimeS[0])

    while start_time + winSeconds <= float(uniformTimeS[-1]) + 1e-9:
        in_win = (uniformTimeS >= start_time) & (uniformTimeS <= start_time + winSeconds)
        win_times = uniformTimeS[in_win]
        win_values = edrUniform[in_win]

        if len(win_times) >= 10:
            brpm, n_cross, thr = estimator(win_values, win_times)
            results.append({
                "t0": float(win_times[0]),
                "t1": float(win_times[-1]),
                "RR_brpm": float(brpm),        # <-- explicit BREATHS per minute
                "crossings": int(n_cross),
                "threshold": float(thr),
            })

        start_time += hopSeconds

    return results

def InterpolateNans(x):
    """Linear fill NaNs in a 1d array."""
    y = np.asarray(x, dtype=float).copy()
    nans = np.isnan(y)

    # nothing to do
    if not np.any(nans):
        return y

    # if everything is NaN, there's nothing to interpolate
    if np.all(nans):
        return np.zeros_like(y)

    idx = np.arange(y.size)
    y[nans] = np.interp(idx[nans], idx[~nans], y[~nans])
    return y

def RemoveQrsByMask(ecg, rIndices, fs, halfWidthMs=80):
    """Zero-out ECG samples around each R-peak to remove QRS influence."""
    y = ecg.astype(float).copy()
    halfWidth = max(1, int(round(halfWidthMs * fs / 1000.0)))
    for i in np.asarray(rIndices, dtype=int):
        i0 = max(0, i - halfWidth)
        i1 = min(len(y) - 1, i + halfWidth)
        y[i0:i1+1] = np.nan
    return InterpolateNans(y)

def EdrBaselineWander(ecg, timeS, fs, rIndices=None, respLow=0.05, respHigh=0.7, qrsHalfWidthMs=80, bpOrder=4):
    """Baseline wander EDR:
    1) If rIndices not given, detect R-peaks
    2) Mask qrsHalfWidthMs around each R-peak and fill by interpolation
    3) Bandpass the result in the respiratory band
    """
    if rIndices is None or len(rIndices) == 0:
        ecgQRS = QrsBandpass(ecg, fs)
        rIndices = DetectRPeaks(ecgQRS, fs)

    ecgNoQRS = RemoveQrsByMask(ecg, rIndices, fs, halfWidthMs=qrsHalfWidthMs)

    edrBw = UF.BandpassFilter(
        ecgNoQRS,
        samplingFreq=fs,
        low=respLow,
        high=respHigh,
        order=bpOrder
    )
    return edrBw, rIndices

