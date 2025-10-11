from scipy.signal import butter, filtfilt, find_peaks, welch
import numpy as np



def BandpassFilter(signal, samplingFreq, low=0.05, high=0.8, order=4):
    nyq = 0.5 * samplingFreq
    b, a = butter(order, [low / nyq, high / nyq], btype='band')
    return filtfilt(b, a, signal)

def ComputeMagnitude(ax, ay, az):
    return np.sqrt(ax**2 + ay**2 + az**2)