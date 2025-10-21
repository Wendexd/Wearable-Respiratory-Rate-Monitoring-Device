from scipy.signal import butter, filtfilt, find_peaks, welch
import numpy as np



def BandpassFilter(signal, samplingFreq, low=0.05, high=0.8, order=4):
    nyq = 0.5 * samplingFreq
    b, a = butter(order, [low / nyq, high / nyq], btype='band')
    return filtfilt(b, a, signal)

def ComputeMagnitude(ax, ay, az):
    return np.sqrt(ax**2 + ay**2 + az**2)

def MOBrpm(manualSignal, timeSeconds):
    """ Calculate the breathing rate from manual observations."""
    # Find all rising edges (start of inhalation)
    # A rising edge is where the signal goes from 0 to 1
    # A breath cycle is from one rising edge to the next
    # Count the number of breaths and calculate the time duration
    t = np.asarray(timeSeconds, dtype=float)
    m = np.asarray(manualSignal, dtype=int)

    # Ensure binary (in case of stray values)
    m = (m > 0).astype(np.uint8)

    # Find rising edges
    dm = np.diff(m, prepend=m[0])
    rise_idx = np.where(dm == 1)[0]

    # Need at least two rising edges to define cycles
    if rise_idx.size < 2:
        return np.nan

    rise_t = t[rise_idx]
    breath_count = rise_t.size - 1
    duration_s = rise_t[-1] - rise_t[0]
    if duration_s <= 0:
        return np.nan

    return float(60.0 * breath_count / duration_s)
