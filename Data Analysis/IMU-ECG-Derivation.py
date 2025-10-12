import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from scipy.signal import find_peaks, welch
from scipy.interpolate import interp1d
import UtilityFunctions as UF
import ECGDerivedRR as ECG
import IMUDerivedRR as IMU

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
    """
    Parses new lines like:
    Builds a flat dataframe with columns:
      Timestamp (sec), Time (s), Manual, ax..head, heart
    """
    # Read two columns: the quoted inner CSV and Manual
    df_in = pd.read_csv(
        filePath,
        header=None,
        names=["ESP32_Data", "Manual"],
        skiprows=1,        # skip the ':ESP32_Data,Manual' header
        quotechar='"',
        engine="python"
    )

    # Split the quoted inner CSV into 11 tokens (ts_us, KIND, 9 payload slots)
    parts = df_in["ESP32_Data"].astype(str).str.split(",", n=10, expand=True)
    parts.columns = ["ts_us","kind","ax","ay","az","gx","gy","gz","roll","pitch","last"]

    # Numeric conversions (coerce empties to NaN)
    for c in ["ts_us","ax","ay","az","gx","gy","gz","roll","pitch","last"]:
        parts[c] = pd.to_numeric(parts[c], errors="coerce")

    # Map 'last' into head (IMU) or heart (ECG)
    kind = parts["kind"].astype(str).str.upper()
    head  = np.where(kind=="IMU", parts["last"], np.nan)
    heart = np.where(kind=="ECG", parts["last"], np.nan)

    # Build the flat table your downstream code expects
    df = pd.DataFrame({
        "Timestamp": parts["ts_us"] / 1e6,   # seconds (device micros)
        "Manual": pd.to_numeric(df_in["Manual"], errors="coerce").fillna(0).astype(int),
        "ax": parts["ax"], "ay": parts["ay"], "az": parts["az"],
        "gx": parts["gx"], "gy": parts["gy"], "gz": parts["gz"],
        "roll": parts["roll"], "pitch": parts["pitch"], "head": head,
        "heart": heart,
    })

    # Relative time axis
    df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

    # Log a quick summary (optional)
    n_imu = (kind=="IMU").sum()
    n_ecg = (kind=="ECG").sum()
    print(f"[INFO] Parsed rows: {len(df)} (IMU={n_imu}, ECG={n_ecg})")

    return df

def PlotECG(df, samplingFreq, bandLow, bandHigh, order, displayRaw=True):
    """Plot raw and filtered ECG from dataframe."""
    # Extractp
    ecgRaw, timeSeconds = ECG.GetRawECG(df)

    # Filter ECG
    nyq = 0.5 * samplingFreq
    highHz = min(bandHigh, nyq * 0.9)  # avoid >Nyquist
    ecgFiltered = UF.BandpassFilter(ecgRaw, samplingFreq, low=bandLow, high=highHz, order=order)
    # EDRFiltered = ECG.DeriveEDRFromRPeaks(
    # ecgSignal=ecgRaw,
    # timeSeconds=timeSeconds,
    # samplingFreq=samplingFreq,
    # respLowFreq=0.05,
    # respHighFreq=0.8,
    # outputTime=timeSeconds 
    # )

    # --------------------------------- AM --------------------------------
    # QRSbased band for peak detection
    ecgQRS = ECG.QrsBandpass(ecgRaw, samplingFreq)

    # R peak detection
    rPeaks = ECG.DetectRPeaks(ecgQRS, samplingFreq)
    if len(rPeaks) < 2:
        print("[AM] Not enough peaks detected to build EDR.")
        # fallback: plot what we have and return
        plt.figure(figsize=(14, 5))
        if displayRaw:
            plt.plot(timeSeconds, ecgRaw, alpha=0.35, label="ECG raw")
        plt.plot(timeSeconds, ecgQRS, label=f"ECG (QRS {bandLow}-{highHz} Hz)")
        plt.xlabel("Time (s)"); plt.ylabel("ECG (a.u.)")
        plt.title(f"ECG (fs={samplingFreq:.1f} Hz)")
        plt.legend(); plt.tight_layout(); plt.show()
        return
    
    # AM Feature: beat times and amplitudes at R Peaks
    beatTimes = timeSeconds[rPeaks].astype(float)
    beatAmps = ecgRaw[rPeaks].astype(float)

    # Resample AM series to uniform grid and respiration band filter
    edrFs = 10.0  # Hz
    t0, t1 = float(timeSeconds[0]), float(timeSeconds[-1])
    edrTime, edrUniform = ECG.ResampleToUniform(beatTimeS=beatTimes, beatValues=beatAmps, uniformFs=edrFs, tStart=t0, tEnd=t1)
    edrResp = UF.BandpassFilter(edrUniform, edrFs, low=0.1, high=0.5, order=4)

    # Windowed Brpm using estimator
    amRRWindows = ECG.EstimateRRWindows(uniformTimeS=edrTime, edrUniform=edrResp, winSeconds=32, hopSeconds=8, estimator=ECG.AdaptiveUpcrossCount)
    mean_brpm = np.mean([w["RR_brpm"] for w in amRRWindows]) if amRRWindows else np.nan

    # ------------------------- Baseline Wander RR -------------------------
    edrBw, rIndices = ECG.EdrBaselineWander(ecgRaw, timeSeconds, samplingFreq)
    bwRR = ECG.EstimateRRWindows(timeSeconds, edrBw, winSeconds=32, hopSeconds=8, estimator=ECG.AdaptiveUpcrossCount)

    # Print some stats
    print(f"[ECG] fs={samplingFreq:.1f} Hz, band={bandLow}-{highHz} Hz, order={order}")
    print(f"[ECG] Raw mean={np.mean(ecgRaw):.2f}, std={np.std(ecgRaw):.2f}")
    print(f"[ECG] Filt mean={np.mean(ecgFiltered):.2f}, std={np.std(ecgFiltered):.2f}")
    print(f"[AM] R-peaks: {len(rPeaks)} | EDR fs={edrFs} Hz | mean BRPM={mean_brpm:.2f}")

    if amRRWindows:
        print("\n[AM] Windowed BRPM estimates:")
        for r in amRRWindows:
            print(f"{r['t0']:.1f}-{r['t1']:.1f}s: {r['RR_brpm']:.1f} brpm (crossings={r['crossings']})")

    if bwRR:
        print("\n[BW] Windowed BRPM estimates:")
        for r in bwRR:
            print(f"{r['t0']:.1f}-{r['t1']:.1f}s: {r['RR_brpm']:.1f} brpm (crossings={r['crossings']})")
    # Plot
    if displayRaw:
        plt.plot(timeSeconds, ecgRaw, alpha=0.35, label="ECG raw")
    plt.plot(timeSeconds, ecgQRS, linewidth=1.2, label=f"ECG (QRS {bandLow}-{highHz} Hz)")
    plt.plot(timeSeconds[rPeaks], ecgQRS[rPeaks], "rx", ms=4, label="R-peaks")
    # plt.plot(timeSeconds, edrBw, label="EDR (BW)", linewidth=1.5, alpha=0.7)
    plt.xlabel("Time (s)"); plt.ylabel("ECG (a.u.)")
    plt.title("ECG with R-peaks (QRS-band)")
    plt.legend(loc="upper right"); plt.tight_layout(); plt.show()

    # (b) EDR from AM
    plt.figure(figsize=(14, 5))
    plt.plot(edrTime, edrUniform, alpha=0.5, label="EDR (AM, uniform)")
    plt.plot(edrTime, edrResp, linewidth=1.5, label="EDR (0.1–0.5 Hz)")
    ttxt = f"EDR (AM) — mean BRPM={mean_brpm:.2f}" if np.isfinite(mean_brpm) else "EDR (AM)"
    plt.title(ttxt)
    plt.xlabel("Time (s)"); plt.ylabel("EDR (a.u.)")
    plt.legend(loc="upper right"); plt.tight_layout(); plt.show()



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

    # --- Split the mixed dataframe ---
    # IMU rows have accel values; ECG rows have 'heart'
    df_imu = df[df["az"].notna()].sort_values("Time (s)").reset_index(drop=True)
    df_ecg = df[df["heart"].notna()].sort_values("Time (s)").reset_index(drop=True)

    # --- Sampling frequencies per stream ---
    imuSamplingFreq = 50.0
    ecgSamplingFreq = 500.0

    # --- ECG plotting/processing uses the ECG-only frame ---
    PlotECG(df_ecg, ecgSamplingFreq, bandLow=0.5, bandHigh=40.0, order=4, displayRaw=True)

    # --- Resp/IMU path uses the IMU-only frame ---
    respRaw, respLabel = IMU.GetRespSignal(df_imu, mode=RESP_MODE_DEFAULT)
    IMUfiltered = UF.BandpassFilter(respRaw, imuSamplingFreq, low=0.05, high=0.8, order=4)

    # Peak detection on IMUfiltered; index aligns with df_imu after reset_index above
    peaks, _ = find_peaks(IMUfiltered, distance=int(imuSamplingFreq*1), prominence=0.1)

    # Use the IMU timeline for RR (time-domain) calc
    rrTime = IMU.EstimateRRTime(peaks, df_imu["Time (s)"].to_numpy())
    rrFreq = IMU.EstimateRRFreq(IMUfiltered, imuSamplingFreq, window=30, low=0.05, high=0.8)

    print(f"Estimated RR (Time Domain): {rrTime:.2f} breaths/min" if rrTime else "RR (Time Domain): N/A")
    print(f"Estimated RR (Freq Domain): {rrFreq:.2f} breaths/min" if rrFreq else "RR (Freq Domain): N/A")

    # Plot respiration vs IMU time, overlay Manual from df_imu
    PlotSignals(df_imu, IMUfiltered, peaks)

