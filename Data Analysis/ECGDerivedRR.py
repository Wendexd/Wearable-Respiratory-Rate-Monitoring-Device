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

def QrsBandpassAM(ecg, fs, low=0.5, high=25, order=4):
    return UF.BandpassFilter(ecg, fs, low, high, order)

def QrsBandpass(ecg, fs, low=0.5, high=40.0, order=4):
    return UF.BandpassFilter(ecg, fs, low, high, order)

def DetectRPeaksAM(ecgQrs, fs):
    # robust scale for prominence
    mad = np.median(np.abs(ecgQrs - np.median(ecgQrs)))
    prom = 3.0 * mad if mad > 0 else 0.5 * np.std(ecgQrs)

    min_distance = int(0.35 * fs)             # 350 ms refractory
    width_bounds = (int(0.02*fs), int(0.12*fs))  # 20–120 ms

    peaks, props = find_peaks(
        ecgQrs,
        distance=min_distance,
        prominence=prom,
        width=width_bounds
    )
    return peaks

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

def CalcAM(ecg, timeS, fs, onsetSearch=0.1, outputTime=None, uniformFs=5.0, useHighpass=False):

    # Detect R peaks for timing (measures amplitudes on raw ecg)
    ecgQRS = QrsBandpassAM(ecg, fs)
    rIndices = DetectRPeaksAM(ecgQRS, fs)
    if rIndices is None or len(rIndices) < 2:
        return None, None, rIndices
    
    # For each R, find local minimum in R - onsetSearch seconds before R peak (onset)
    win = max(1, int(round(onsetSearch * fs)))
    onsetIndices = []
    rIdxKept = []
    for ri in np.asarray(rIndices, dtype=int):
        i0 = max(0, ri - win)
        i1 = ri
        if i1 <= i0:
            continue
        onsetIdx = i0 + int(np.argmin(ecg[i0:i1+1]))
        if onsetIdx >= ri:
            continue
        onsetIndices.append(onsetIdx)
        rIdxKept.append(ri)

    if len(rIdxKept) < 2:
        return None, None, rIdxKept
    
    rIndices = np.asarray(rIdxKept, dtype=int)
    onsetIndices = np.asarray(onsetIndices, dtype=int)

    # Beat wise AM values and times
    amValues = ecg[rIndices] - ecg[onsetIndices]
    tBeats = 0.5 * (timeS[rIndices] + timeS[onsetIndices])

    # Normalise by mean (RRest style: dimensionless, arounds 1.0)
    m = np.nanmean(amValues)
    if not np.isfinite(m) or m == 0:
        return None, None, rIndices
    amValues = amValues / m

    # Resample to uniform grid
    if outputTime is None:
        outputTime = np.arange(float(tBeats[0]), float(tBeats[-1]), 1.0/uniformFs)
    f = interp1d(tBeats, amValues, kind="linear", fill_value="extrapolate", assume_sorted=True)
    amSignalUniform = f(outputTime)

    # light filtering
    fsUniform = 1.0 / np.median(np.diff(outputTime))
    if useHighpass:
        amSignal = UF.HighpassFilter(amSignalUniform, fsUniform)
    else:
        amSignal = UF.BandpassFilter(amSignalUniform, fsUniform, low=UF.RESP_LOW_BAND, high=UF.RESP_HIGH_BAND, order=4)

    return amSignal, outputTime, rIndices

def BuildWins(uniformTimeS, windowS=30, hopS=8, allowPartial=True):
    t0 = float(uniformTimeS[0])
    t1 = float(uniformTimeS[-1])
    tStarts = []
    tEnds = []
    t = t0
    while t + windowS <= t1 + 1e-9:
        tStarts.append(t)
        tEnds.append(t + windowS)
        t += hopS

    if allowPartial and not tStarts and (t1 - t0) > 0:
        # one partial window covering what you have
        tStarts.append(t0)
        tEnds.append(t1)
    return np.asarray(tStarts, dtype=float), np.asarray(tEnds, dtype=float)



def CountOrigWindows(signal, outputTime, windowS=30, hopS=8, threshFactor=0.2, zeroCentre=True, minSamples=10):

    fsUniform = 1.0 / np.median(np.diff(outputTime))

    # Windows
    winStarts, winEnds = BuildWins(outputTime, windowS, hopS)
    print(f"WindowStart{winStarts}, WindowEnd{winEnds}")

    # run count orig on each window
    time = np.asarray(outputTime, dtype=float)
    x = np.asarray(signal, dtype=float)
    out = dict(t0=[], t1=[], RRBrpm=[], nCycles=[], threshold=[])

    for start, end in zip(winStarts, winEnds):
        inWindow = (time >= start) & (time < end)
        if np.count_nonzero(inWindow) >= minSamples:
            brpm, nCycles, threshold = CountOrig(x[inWindow], time[inWindow], threshFactor=threshFactor, zeroCentre=zeroCentre)
        else:
            brpm, nCycles, threshold = np.nan, 0, np.nan

        out["t0"].append(float(start))
        out["t1"].append(float(end))
        out["RRBrpm"].append(float(brpm))
        out["nCycles"].append(int(nCycles))
        out["threshold"].append(float(threshold))

    # convert lists to numpy arrays
    for key in out:
        out[key] = np.asarray(out[key])
    
    return out


def CountOrig(signal, timeS, threshFactor=0.2, zeroCentre=True, minBreathInterval=2.0, maxBreathInterval=10.0): # min 6 brpm, max 30 brpm

    signal = np.asarray(signal, dtype=float)
    timeS = np.asarray(timeS, dtype=float)
    
    if signal.size < 5:
        return np.nan, 0, np.nan
    
    if zeroCentre:
        signal = signal - np.mean(signal)

    # Local maxima / minima via derivative sign change,
    dx = np.diff(signal)
    peaks = np.where((dx[:-1] > 0) & (dx[1:] < 0))[0] + 1  # local maxima
    troughs = np.where((dx[:-1] < 0) & (dx[1:] > 0))[0] + 1  # local minima
    if peaks.size == 0 or troughs.size == 0:
        return np.nan, 0, np.nan
    
    # Count Orig threshold: 0.2 * 75th percentile of peak amplitudes
    q3 = np.percentile(signal[peaks], 75)
    threshold = float(threshFactor * q3)

    # relevant extrema
    relPeaks = peaks[signal[peaks] > threshold]
    relTroughs = troughs[signal[troughs] < 0]

    # valid cycles: consectuive relevant peaks with exactly one relevant trough between them
    durations = []
    for p0, p1 in zip(relPeaks[:-1], relPeaks[1:]):
        numTroughs = np.sum((relTroughs > p0) & (relTroughs < p1))
        if numTroughs == 1:
            dur = timeS[p1] - timeS[p0]
            if dur >= minBreathInterval and dur <= maxBreathInterval:
                durations.append(dur)

    if len(durations) == 0:
        return np.nan, 0, threshold
    
    aveBreathDurationS = float(np.mean(durations))
    if not np.isfinite(aveBreathDurationS) or aveBreathDurationS <= 0:
        return np.nan, 0, threshold
    
    brpm = 60.0 / aveBreathDurationS
    return brpm, len(durations), threshold


def ECGToBPM(ecgSignal, samplingFreq, rriMinS=0.3, rriMaxS=2.0):
    
    ecg, timeSeconds = GetRawECG(ecgSignal)

    # Filter into QRS band and detect R-peaks
    ecgQRS = QrsBandpass(ecg, samplingFreq)
    rPeaks = DetectRPeaks(ecgQRS, samplingFreq)
    rPeakTimesSeconds = timeSeconds[rPeaks].astype(float)

    # Not enough beats to compute RRI
    if len(rPeakTimesSeconds) < 2:
        return None
    
    # R-R Intervals (seconds) and validity mask
    rriS = np.diff(rPeakTimesSeconds)
    valid = (rriS >= rriMinS) & (rriS <= rriMaxS) # Drop ectopic/outliers

    if not np.any(valid):
        return None
    
    RRI_s_valid = rriS[valid]
    bpmInstant = 60.0 / RRI_s_valid
    bpmTimeS = 0.5 * (rPeakTimesSeconds[1:] + rPeakTimesSeconds[:-1])[valid] # mid points
    bpmMean = float(np.mean(bpmInstant))

    return bpmMean
