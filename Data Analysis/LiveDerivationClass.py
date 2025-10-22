from collections import deque
import numpy as np
import UtilityFunctions as UF
import IMUDerivedRR as IMU


class LiveDerivation:
    """
    Class for live derivation of respiratory rate from IMU and ECG data Stream
    """

    def __init__(self, fsIMU, fsECG, slidingWindow=30, hopInterval=1):
        self.slidingWindow = slidingWindow
        self.fsIMU = 50
        self.fsECG = 500
        self.sampleWindowIMU = int(round(slidingWindow * fsIMU))
        self.hopNIMU = int(round(hopInterval * fsIMU))
        self.hopNECG = int(round(hopInterval * fsECG))
        self.samppleWindowECG = int(round(slidingWindow * fsECG))

        # ring buffers
        self.buffZ = deque(maxlen=self.sampleWindowIMU)
        self.buffPitch = deque(maxlen=self.sampleWindowIMU)
        self.buffAccelPitch = deque(maxlen=self.sampleWindowIMU)
        self.manualBuff = deque(maxlen=self.sampleWindowIMU)

        # counter to decide when to compute
        self.nSinceLast = 0


    def Prepare(self, buff):
        data = np.asarray(buff, dtype=float)
        data = UF.BandpassFilter(data, self.fsIMU, UF.RESP_LOW_BAND, UF.RESP_HIGH_BAND, order=4)
        return data

    def Update(self, az, devicePitch, accelPitch, manualSignal):
        """
        Push one new sample for each stream, compute RR every hop interval if enough data
        """

        self.buffZ.append(float(az))
        self.buffPitch.append(float(devicePitch))
        self.buffAccelPitch.append(float(accelPitch))
        self.manualBuff.append(int(manualSignal))
        self.nSinceLast += 1



        # Need a full window first
        if len(self.buffZ) < self.sampleWindowIMU:
            timeLeft = self.slidingWindow - len(self.buffZ) / self.sampleWindowIMU * self.slidingWindow
            print(f"Initalising buffers... Please wait {timeLeft:.2f}s")
            return None
        
        # Only Compute every hop
        if self.nSinceLast < self.hopNIMU:
            # print(f"waiting for next hop interval")
            return None
        self.nSinceLast = 0

        # Prepare windowed signals
        windowZ = self.Prepare(self.buffZ)
        windowPitch = self.Prepare(self.buffPitch)
        windowAccelPitch = self.Prepare(self.buffAccelPitch)
        manualBrpm = UF.MOBrpm(self.manualBuff, np.arange(len(self.manualBuff)) / self.fsIMU, minBrpm=30)

        zFinal, zAC, zFFT = IMU.CombineRREstimates(windowZ, self.fsIMU)
        pitchFinal, pitchAC, pitchFFT = IMU.CombineRREstimates(windowPitch, self.fsIMU)
        accelPitchFinal, accelPitchAC, accelPitchFFT = IMU.CombineRREstimates(windowAccelPitch, self.fsIMU)

        return {
            "z" : {"RR": zFinal, "AC": zAC, "FFT": zFFT},
            "pitch" : {"RR": pitchFinal, "AC": pitchAC, "FFT": pitchFFT},
            "accelPitch" : {"RR": accelPitchFinal, "AC": accelPitchAC, "FFT": accelPitchFFT}
            ,"manualBrpm": manualBrpm
        }
        