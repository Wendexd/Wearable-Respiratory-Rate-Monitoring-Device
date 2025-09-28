import os
import pandas as pd
import matplotlib.pyplot as plt

# Path to your "Recording Sessions" folder
RECORDING_FOLDER = r"C:\Users\wende\OneDrive\UNI Cloud\2025\Thesis Project\Technical Stuff\Data Analysis\Recording Scripts\Recording Sessions"

def choose_file():
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

def plot_file(filePath):
    """Load and plot ESP32 + manual breathing data from CSV."""
    df = pd.read_csv(filePath)
    
    # Convert timestamp to relative time
    df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

    # Split ESP32_Data into named columns (10 values total)
    esp32_split = df["ESP32_Data"].str.split(",", expand=True).astype(float)
    esp32_split.columns = [
        "ax", "ay", "az", 
        "gx", "gy", "gz", 
        "roll", "pitch", "head", 
        "heart"
    ]
    df = pd.concat([df, esp32_split], axis=1)

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Accelerometer
    ax1.plot(df['Time (s)'], df['ax'], label="ax (g)", color="blue")
    ax1.plot(df['Time (s)'], df['ay'], label="ay (g)", color="green")
    ax1.plot(df['Time (s)'], df['az'], label="az (g)", color="purple")

    # Gyroscope
    ax1.plot(df['Time (s)'], df['gx'], label="gx (°/s)", linestyle="--", color="orange")
    ax1.plot(df['Time (s)'], df['gy'], label="gy (°/s)", linestyle="--", color="red")
    ax1.plot(df['Time (s)'], df['gz'], label="gz (°/s)", linestyle="--", color="brown")

    # Orientation
    ax1.plot(df['Time (s)'], df['roll'], label="roll (°)", linestyle=":", color="cyan")
    ax1.plot(df['Time (s)'], df['pitch'], label="pitch (°)", linestyle=":", color="magenta")
    ax1.plot(df['Time (s)'], df['head'], label="head (°)", linestyle=":", color="black")

    # Heart activity (if useful, optional line)
    ax1.plot(df['Time (s)'], df['heart'], label="heart", linestyle="-.", color="gray")

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
    esp32_split = df["ESP32_Data"].str.split(",", expand=True).astype(float)
    esp32_split.columns = ["ax", "ay", "az", "gx", "gy", "gz", "roll", "pitch", "head"]
    df = pd.concat([df, esp32_split], axis=1)

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot accelerometer data
    ax1.plot(df['Time (s)'], df['ax'], label="ax (g)", color="blue")
    ax1.plot(df['Time (s)'], df['ay'], label="ay (g)", color="green")
    ax1.plot(df['Time (s)'], df['az'], label="az (g)", color="purple")
    
    # Plot gyro data (on same axis for simplicity)
    ax1.plot(df['Time (s)'], df['gx'], label="gx (deg/s)", linestyle="--", color="orange")
    ax1.plot(df['Time (s)'], df['gy'], label="gy (deg/s)", linestyle="--", color="red")
    ax1.plot(df['Time (s)'], df['gz'], label="gz (deg/s)", linestyle="--", color="brown")

    # Plot orientation (roll, pitch, head)
    ax1.plot(df['Time (s)'], df['roll'], label="roll (deg)", linestyle=":", color="cyan")
    ax1.plot(df['Time (s)'], df['pitch'], label="pitch (deg)", linestyle=":", color="magenta")
    ax1.plot(df['Time (s)'], df['head'], label="head (deg)", linestyle=":", color="black")

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
    filePath = choose_file()
    print(f"\nSelected file: {filePath}")
    plot_file(filePath)
