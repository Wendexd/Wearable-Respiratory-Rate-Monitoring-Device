import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from scipy.signal import butter, filtfilt, find_peaks, welch
from scipy.interpolate import interp1d

# --- Configuration ---
# Path to your "Recording Sessions" folder
RECORDING_FOLDER = r"C:\Users\wende\OneDrive\UNI Cloud\2025\Thesis Project\Technical Stuff\Data Analysis\Recording Scripts\Recording Sessions"
RESP_MODE_DEFAULT = "z" # Options: "x", "y", "z", "mag"


def ChooseFile():
    """CLI menu to pick a CSV file from RECORDING_FOLDER."""
    files = [f for f in os.listdir(RECORDING_FOLDER) if f.endswith(".csv")]
    
    if not files:
        print("No CSV files found in Recording Sessions folder.")
        exit(1)
    
    print("\nSelect a recording file:\n")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f}")
    
    choice = int(input("\nEnter the number of the file: ")) - 1
    return os.path.join(RECORDING_FOLDER, files[choice])

def LoadData(filePath, saveBadRows=True):


    df = pd.read_csv(filePath)

    # Relative time
    df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

    # --- 1) Filter by exact field count BEFORE splitting ---
    expectedCols = 10                      # ax, ay, az, gx, gy, gz, roll, pitch, head, heart
    # Count commas; a valid line has expectedCols-1 commas
    commaMask = df["ESP32_Data"].astype(str).str.count(",") == (expectedCols - 1)
    badCountFields = (~commaMask).sum()

    if badCountFields > 0:
        print(f"[Warning] Rows with wrong field count: {badCountFields}/{len(df)}")
        print(df.loc[~commaMask, ["Timestamp", "ESP32_Data"]].head())

    dfGood = df.loc[commaMask].copy()
    badRows = df.loc[~commaMask].copy()

    # --- 2) Split and convert to numeric ---
    esp32Split = dfGood["ESP32_Data"].str.split(",", expand=True)
    # Convert to numeric; invalid -> NaN
    esp32Split = esp32Split.apply(pd.to_numeric, errors="coerce")

    # --- 3) Drop rows with NaNs (corrupted numeric values) ---
    nanMask = esp32Split.isna().any(axis=1)
    badCountNumeric = nanMask.sum()
    if badCountNumeric > 0:
        print(f"[Warning] Rows with non-numeric values: {badCountNumeric}/{len(dfGood)}")
        print(dfGood.loc[nanMask, ["Timestamp", "ESP32_Data"]].head())

    # Accumulate all bads (for optional save)
    badRows = pd.concat([badRows, dfGood.loc[nanMask]], axis=0)

    # Keep only clean rows
    dfClean = dfGood.loc[~nanMask].copy()
    esp32Clean = esp32Split.loc[~nanMask].copy()

    # --- 4) Name columns and merge back ---
    esp32Clean.columns = [
        "ax", "ay", "az",
        "gx", "gy", "gz",
        "roll", "pitch", "head",
        "heart"
    ]
    dfClean = dfClean.reset_index(drop=True)
    esp32Clean = esp32Clean.reset_index(drop=True)
    dfClean = pd.concat([dfClean, esp32Clean], axis=1)

    # --- 5) Final logging & optional dump of bad rows ---
    totalBad = badCountFields + badCountNumeric
    kept = len(dfClean)
    print(f"[INFO] Loaded {kept} clean rows; dropped {totalBad} corrupted rows out of {len(df)} total.")

    if saveBadRows and totalBad > 0:
        out_bad = Path(filePath).with_name(Path(filePath).stem + "_badrows.csv")
        badRows.to_csv(out_bad, index=False)
        print(f"[INFO] Saved {len(badRows)} bad rows to: {out_bad}")

    return dfClean


def BandpassFilter(signal, samplingFreq, low=0.05, high=0.8, order=4):
    nyq = 0.5 * samplingFreq
    b, a = butter(order, [low / nyq, high / nyq], btype='band')
    return filtfilt(b, a, signal)

def ComputeMagnitude(ax, ay, az):
    return np.sqrt(ax**2 + ay**2 + az**2)

def GetRespSignal(df, mode=RESP_MODE_DEFAULT):
    mode = mode.lower()
    if mode == "z":
        return df["az"].to_numpy(), "Z-axis (g)"
    elif mode == "mag":
        mag = ComputeMagnitude(df["ax"].to_numpy(), df["ay"].to_numpy(), df["az"].to_numpy())
        return mag, "Accel Magnitude (g)"
    else:
        raise ValueError('mode must be "z" or "mag"')
    
def GetRawECG(df):
    ecg = df["heart"].to_numpy()
    t = df["Time (s)"].to_numpy(dtype=float)
    return ecg, t
    
def DetectRRECG(signal, samplingFreq, sanityFilter=True):
    """Lightweight R-peak finder: bandpass then peaks with basic RR sanity."""
    ecgFiltered = BandpassFilter(signal, samplingFreq, low=0.5, high=40.0, order=4)
    # Enforce physionlogical separation between peaks (250ms)
    distance = int(samplingFreq * 0.25)  # min Xms between beats
    # Prominenve scaled to signal dispersion to surpress noise peaks
    peakProminence = np.std(ecgFiltered) * 0.5

    peaks, _ = find_peaks(ecgFiltered, distance=distance, prominence=peakProminence)

    # Optional sanity filter: drop improbable RR intervals (<0.3s or >6s)
    if len(peaks) >= 3 and sanityFilter:
        rrIntervalSeconds = np.diff(peaks) / samplingFreq
        keepMask = np.hstack(
            [True], # Keep first peak
            (rrIntervalSeconds > 0.3) & (rrIntervalSeconds < 6.0))
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
    edrFiltered = BandpassFilter(
        edrUniform,
        fs=samplingFreq,
        low=respLowFreq,
        high=respHighFreq,
        order=4
    )
    
    return edrFiltered

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

def PlotECG(df, samplingFreq, bandLow, bandHigh, order, displayRaw=True):
    """Plot raw and filtered ECG from dataframe."""
    # Extractp
    ecgRaw, timeSeconds = GetRawECG(df)

    # Filter ECG
    nyq = 0.5 * samplingFreq
    highHz = min(bandHigh, nyq * 0.9)  # avoid >Nyquist
    ecgFiltered = BandpassFilter(ecgRaw, samplingFreq, low=bandLow, high=highHz, order=order)

    # Print some stats
    print(f"[ECG] fs={samplingFreq:.1f} Hz, band={bandLow}-{highHz} Hz, order={order}")
    print(f"[ECG] Raw mean={np.mean(ecgRaw):.2f}, std={np.std(ecgRaw):.2f}")
    print(f"[ECG] Filt mean={np.mean(ecgFiltered):.2f}, std={np.std(ecgFiltered):.2f}")

    # Plot
    plt.figure(figsize=(14, 5))
    if (displayRaw):
        plt.plot(timeSeconds, ecgRaw,  alpha=0.4, label="Raw ECG")
    plt.plot(timeSeconds, ecgFiltered, linewidth=1.5, label="Filtered ECG (QRS band)")
    plt.xlabel("Time (s)")
    plt.ylabel("ECG (a.u.)")
    plt.title(f"ECG: Raw vs. Filtered (Band {bandLow}-{highHz} Hz)")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()



def PlotSignals(df, respSignal, peaks):
    fig, ax1 = plt.subplots(figsize=(14, 7))
    ax1.plot(df["Time (s)"], respSignal, label="Filtered Respiration (mag)", color="blue")
    ax1.plot(df["Time (s)"].iloc[peaks], respSignal[peaks], "rx", label="Detected Breaths")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Respiration Signal (a.u.)")
    ax1.legend(loc="upper right")

    # Manual breathing overlay
    ax2 = ax1.twinx()
    ax2.step(df["Time (s)"], df["Manual"], color="darkred", where="post", alpha=0.5, label="Manual (0/1)")
    ax2.set_ylabel("Manual Breathing", color="darkred")

    fig.suptitle("Respiratory Signal Extraction")
    fig.tight_layout()
    plt.show()

def plot_file(filePath):


    """Load and plot ESP32 + manual breathing data from CSV."""
    df = pd.read_csv(filePath)
    
    # Convert timestamp to relative time
    df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

    # Split ESP32_Data into named columns (10 values total)
    esp32Split = df["ESP32_Data"].str.split(",", expand=True).astype(float)
    esp32Split.columns = [
        "ax", "ay", "az", 
        "gx", "gy", "gz", 
        "roll", "pitch", "head", 
        "heart"
    ]
    df = pd.concat([df, esp32Split], axis=1)

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Accelerometer
    ax1.plot(df['Time (s)'], df['ax'], label="ax (g)", color="blue")
    ax1.plot(df['Time (s)'], df['ay'], label="ay (g)", color="green")
    ax1.plot(df['Time (s)'], df['az'], label="az (g)", color="purple")

    # Gyroscope
    # ax1.plot(df['Time (s)'], df['gx'], label="gx (°/s)", linestyle="--", color="orange")
    # ax1.plot(df['Time (s)'], df['gy'], label="gy (°/s)", linestyle="--", color="red")
    # ax1.plot(df['Time (s)'], df['gz'], label="gz (°/s)", linestyle="--", color="brown")

    # Orientation
    # ax1.plot(df['Time (s)'], df['roll'], label="roll (°)", linestyle=":", color="cyan")
    # ax1.plot(df['Time (s)'], df['pitch'], label="pitch (°)", linestyle=":", color="magenta")
    # ax1.plot(df['Time (s)'], df['head'], label="head (°)", linestyle=":", color="black")

    # Heart activity (if useful, optional line)
    # ax1.plot(df['Time (s)'], df['heart'], label="heart", linestyle="-.", color="gray")

    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("ESP32 Sensor Values")
    ax1.legend(loc="upper right", fontsize=8)

    # Manual breathing
    ax2 = ax1.twinx()
    ax2.step(df['Time (s)'], df['Manual'], color="darkred", where="post", label="Manual Breathing (0/1)")
    ax2.set_ylabel("Manual Breathing", color="darkred")

    fig.suptitle("ESP32 Data (Accel, Gyro, Orientation, Heart) and Manual Breathing")
    fig.tight_layout()
    plt.show()
    """Load and plot ESP32 + manual breathing data from CSV."""
    df = pd.read_csv(filePath)
    
    # Convert timestamp to relative time
    df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

    # Split ESP32_Data into named columns
    esp32Split = df["ESP32_Data"].str.split(",", expand=True).astype(float)
    esp32Split.columns = ["ax", "ay", "az", "gx", "gy", "gz", "roll", "pitch", "head"]
    df = pd.concat([df, esp32Split], axis=1)

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot accelerometer data
    ax1.plot(df['Time (s)'], df['ax'], label="ax (g)", color="blue")
    ax1.plot(df['Time (s)'], df['ay'], label="ay (g)", color="green")
    ax1.plot(df['Time (s)'], df['az'], label="az (g)", color="purple")
    
    # Plot gyro data (on same axis for simplicity)
    # ax1.plot(df['Time (s)'], df['gx'], label="gx (deg/s)", linestyle="--", color="orange")
    # ax1.plot(df['Time (s)'], df['gy'], label="gy (deg/s)", linestyle="--", color="red")
    # ax1.plot(df['Time (s)'], df['gz'], label="gz (deg/s)", linestyle="--", color="brown")

    # Plot orientation (roll, pitch, head)
    # ax1.plot(df['Time (s)'], df['roll'], label="roll (deg)", linestyle=":", color="cyan")
    # ax1.plot(df['Time (s)'], df['pitch'], label="pitch (deg)", linestyle=":", color="magenta")
    # ax1.plot(df['Time (s)'], df['head'], label="head (deg)", linestyle=":", color="black")

    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("ESP32 Sensor Values")
    ax1.legend(loc="upper right", fontsize=8)

    # Manual breathing on secondary axis
    ax2 = ax1.twinx()
    ax2.step(df['Time (s)'], df['Manual'], color="darkred", where="post", label="Manual Breathing (0/1)")
    ax2.set_ylabel("Manual Breathing", color="darkred")

    fig.suptitle("ESP32 Data (Accel, Gyro, Orientation) and Manual Breathing")
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    filePath = ChooseFile()
    print(f"\nSelected file: {filePath}")
    df = LoadData(filePath)

    # Processing 
    samplingFreq = 50.0 # assumed sampling frequency
    PlotECG(df, samplingFreq, bandLow=0.5, bandHigh=40.0, order=4, displayRaw=True)
    respRaw, respLabel = GetRespSignal(df, mode=RESP_MODE_DEFAULT)

    IMUfiltered = BandpassFilter(respRaw, samplingFreq, low=0.05, high=0.8, order=4)

    # Peak detection
    peaks, _ = find_peaks(IMUfiltered, distance=samplingFreq*1, prominence=0.1)  # min 1s apart
    rrTime = EstimateRRTime(peaks, df["Time (s)"])
    rrFreq = EstimateRRFreq(IMUfiltered, samplingFreq, window=30, low=0.05, high=0.8)
    print(f"Estimated RR (Time Domain): {rrTime:.2f} breaths/min" if rrTime else "RR (Time Domain): N/A")
    print(f"Estimated RR (Freq Domain): {rrFreq:.2f} breaths/min" if rrFreq else "RR (Freq Domain): N/A")
    PlotSignals(df, IMUfiltered, peaks)
    # plot_file(filePath)

