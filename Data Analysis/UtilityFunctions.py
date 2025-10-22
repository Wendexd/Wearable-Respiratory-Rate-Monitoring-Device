from scipy.signal import butter, filtfilt, find_peaks, welch
import numpy as np

RESP_LOW_BAND = 0.05
RESP_HIGH_BAND = 0.8


def BandpassFilter(signal, samplingFreq, low=0.05, high=0.8, order=4):
    nyq = 0.5 * samplingFreq
    b, a = butter(order, [low / nyq, high / nyq], btype='band')
    return filtfilt(b, a, signal)

def ComputeMagnitude(ax, ay, az):
    return np.sqrt(ax**2 + ay**2 + az**2)

def FilterRisingEges(riseTimes, maxBrpm = 30):

    mindt = 60.0 / maxBrpm  # Minimum time between breaths in seconds
    rt = np.asarray(riseTimes, dtype=float)
    if rt.size == 0:
        return rt
    keep = [0]
    for t in range(1, rt.size):
        if (rt[t] - rt[keep[-1]]) >= mindt:
            keep.append(t)
    return rt[keep]

def MOBrpm(manualSignal, timeSeconds, minBrpm=30):
    """ Calculate the breathing rate from manual observations."""
    # Find all rising edges (start of inhalation)
    # A rising edge is where the signal goes from 0 to 1
    # A breath cycle is from one rising edge to the next
    # Count the number of breaths and calculate the time duration
    t = np.asarray(timeSeconds, dtype=float)
    m = np.asarray(manualSignal, dtype=int)

    # Find rising edges
    dm = np.diff(m, prepend=m[0])
    riseIdx = np.where(dm == 1)[0]

    # Need at least two rising edges to define cycles
    if riseIdx.size < 2:
        return 0
    
    # Filter out rising edges which occured within the maximum brpm rate
    riseT = t[riseIdx]
    riseT = FilterRisingEges(riseT)

    if riseT.size < 2:
        return 0

    breath_count = riseT.size - 1
    duration_s = riseT[-1] - riseT[0]

    return float(60.0 * breath_count / duration_s)
