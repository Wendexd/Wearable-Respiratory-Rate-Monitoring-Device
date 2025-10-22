from collections import deque
import numpy as np
import UtilityFunctions as UF
import IMUDerivedRR as IMU
import ECGDerivedRR as ECG


class LiveDerivation:
    """
    Class for live derivation of respiratory rate from IMU and ECG data Stream
    """

    def __init__(self, fsIMU, fsECG, slidingWindow=30, hopInterval=1):
        self.slidingWindow = slidingWindow
        self.fsIMU = fsIMU
        self.fsECG = fsECG
        self.sampleWindowIMU = int(round(slidingWindow * fsIMU))
        self.hopNIMU = int(round(hopInterval * fsIMU))
        self.hopNECG = int(round(hopInterval * fsECG))
        self.sampleWindowECG = int(round(slidingWindow * fsECG))

        # ring buffers
        self.buffZ = deque(maxlen=self.sampleWindowIMU)
        self.buffPitch = deque(maxlen=self.sampleWindowIMU)
        self.buffAccelPitch = deque(maxlen=self.sampleWindowIMU)
        self.buffECG = deque(maxlen=self.sampleWindowECG)
        self.manualBuff = deque(maxlen=self.sampleWindowIMU)

        # counter to decide when to compute
        self.nSinceLastIMU = 0
        self.nSinceLastECG = 0


    def PrepareIMU(self, buff):
        data = np.asarray(buff, dtype=float)
        data = UF.BandpassFilter(data, self.fsIMU, UF.RESP_LOW_BAND, UF.RESP_HIGH_BAND, order=4)
        return data
    

    def PrepareECG(self, buff):
        data = np.asarray(buff, dtype=float)
        data = UF.BandpassFilter(data, self.fsECG, 5, 40, order=4)
        return data
    
    def UpdateECG(self, ecgSample):
        """ Push one new ECG Sample"""
        self.buffECG.append(float(ecgSample))
        self.nSinceLastECG += 1

    def ComputeEDR(self, fsUniform=5.0):
        """ Once per hop, compute EDR if enough data """
        
        if len(self.buffECG) < self.sampleWindowECG:
            return None
        if self.nSinceLastECG < self.hopNECG:
            return None
        self.nSinceLastECG = 0

        # Build time axis for current ECG window
        ecg = np.asarray(self.buffECG, dtype=float)
        timeS = np.arange(len(ecg)) / self.fsECG

        ecgFiltered = self.PrepareECG(ecg)

        amSignal, amTime, _ = ECG.CalcAM(
            ecgFiltered,
            timeS,
            self.fsECG,
            onsetSearch=0.1,
            outputTime=None,
            uniformFs=fsUniform,
            useHighpass=False
        )
        if amSignal is None or amTime is None:
            print("Am Signal is None")
            return None
        
        rrAM = ECG.CountOrigWindows(
            amSignal,
            amTime,
            windowS=self.slidingWindow,
            hopS=self.slidingWindow, # single window estimate
            threshFactor=0.2,
            zeroCentre=True)
        
        if rrAM["RRBrpm"].size == 0 or not np.any(np.isfinite(rrAM["RRBrpm"])):
            print("Could not get an estimated RR")
            return None
        
        rrEstimate = float(rrAM["RRBrpm"][-1])

        return {"RR": rrEstimate}

    def Update(self, az, devicePitch, accelPitch, manualSignal):
        """
        Push one new sample for each stream, compute RR every hop interval if enough data
        """

        self.buffZ.append(float(az))
        self.buffPitch.append(float(devicePitch))
        self.buffAccelPitch.append(float(accelPitch))
        self.manualBuff.append(int(manualSignal))
        self.nSinceLastIMU += 1



        # Need a full window first
        if len(self.buffZ) < self.sampleWindowIMU:
            timeLeft = self.slidingWindow - len(self.buffZ) / self.sampleWindowIMU * self.slidingWindow
            print(f"Initalising buffers... Please wait {timeLeft:.2f}s")
            return None
        
        # Only Compute every hop
        if self.nSinceLastIMU < self.hopNIMU:
            # print(f"waiting for next hop interval")
            return None
        self.nSinceLastIMU = 0

        # Prepare windowed signals
        windowZ = self.PrepareIMU(self.buffZ)
        windowPitch = self.PrepareIMU(self.buffPitch)
        windowAccelPitch = self.PrepareIMU(self.buffAccelPitch)
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
        