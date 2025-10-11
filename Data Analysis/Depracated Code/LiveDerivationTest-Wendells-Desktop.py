import serial, time, numpy as np
from collections import deque
from scipy.signal import butter, filtfilt, find_peaks
import pyqtgraph as pg

PORT = "COM3"      # e.g. "COM5", "/dev/ttyUSB0", "/dev/cu.usbmodemXYZ"
BAUD = 115200
FS   = 50.0        # must match your MCU config
WIN_SEC, HOP_SEC = 30.0, 0.5
BAND = (0.15, 0.40)
PLAUS_BPM = (8, 26)

# IMU band-pass
b, a = butter(4, [BAND[0]/(0.5*FS), BAND[1]/(0.5*FS)], btype='band')

def rr_from_autocorr(x, fs, min_bpm=6, max_bpm=30):
    n = len(x)
    if n < fs*5: return np.nan
    ac = np.correlate(x, x, mode='full')[n-1:]
    minlag = int((60/max_bpm)*fs); maxlag = int((60/min_bpm)*fs)
    if maxlag <= minlag or maxlag >= len(ac): return np.nan
    idx = np.argmax(ac[minlag:maxlag]) + minlag
    lag = idx / fs
    return 60.0/lag if lag > 0 else np.nan

def rr_from_fft(x, fs, lo, hi):
    n = len(x)
    if n == 0: return np.nan
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1/fs)
    m = (f >= lo) & (f <= hi)
    if not np.any(m): return np.nan
    fpk = f[m][np.argmax(np.abs(X[m]))]
    return 60.0 * fpk

# Buffers
N = int(WIN_SEC * FS)
t_buf = deque(maxlen=N)
az_buf = deque(maxlen=N)
man_buf = deque(maxlen=N)

ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(0.4)  # let serial settle; header may arrive

# UI
app = pg.mkQApp("Live RR")
win = pg.GraphicsLayoutWidget(show=True, title="IMU Live RR")
p = win.addPlot(title="Filtered az_g + peaks + manual")
curve = p.plot(pen=pg.mkPen(width=1))
peaks_scatter = p.plot(pen=None, symbol='o', symbolSize=5)
manual_curve = pg.PlotCurveItem(pen=pg.mkPen(style=pg.QtCore.Qt.DashLine))
p.addItem(manual_curve)
txt = pg.TextItem(anchor=(0,1)); p.addItem(txt); txt.setPos(0,1)

last_update = 0

def parse_line(line):
    # t_ms,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps,pitch_deg,roll_deg,yaw_deg,manual,heart
    parts = line.strip().split(',')
    if len(parts) != 12: return None
    try:
        t_ms = float(parts[0])
        az_g = float(parts[3])
        manual = float(parts[10])
        return t_ms/1000.0, az_g, manual
    except ValueError:
        return None

def update():
    global last_update
    while ser.in_waiting:
        raw = ser.readline().decode(errors='ignore')
        if not raw or raw.startswith('t_ms'):  # skip header
            continue
        parsed = parse_line(raw)
        if parsed is None: 
            continue
        t, az, m = parsed
        t_buf.append(t); az_buf.append(az); man_buf.append(m)

    if len(az_buf) < int(FS*5) or time.time() - last_update < HOP_SEC:
        return
    last_update = time.time()

    x = np.array(az_buf, dtype=float)
    xf = filtfilt(b, a, x, method="pad")

    ac_bpm  = rr_from_autocorr(xf, FS, 6, 30)
    fft_bpm = rr_from_fft(xf, FS, BAND[0], BAND[1])
    vals = [v for v in (ac_bpm, fft_bpm) if PLAUS_BPM[0] < (v if not np.isnan(v) else -1e9) < PLAUS_BPM[1]]
    rr = np.mean(vals) if vals else np.nan

    # Visuals
    t_arr = np.array(t_buf)
    curve.setData(t_arr, xf)

    min_dist = int(FS * (60/30))
    pk, _ = find_peaks(xf, distance=min_dist)
    peaks_scatter.setData(t_arr[pk], xf[pk])

    if not np.all(np.isnan(man_buf)):
        m = np.array(man_buf); 
        lo, hi = np.nanmin(xf), np.nanmax(xf)
        if np.nanmax(m) > np.nanmin(m):
            mm = (m - np.nanmin(m)) / (np.nanmax(m)-np.nanmin(m))
            manual_curve.setData(t_arr, mm*(hi-lo)+lo)
    p.enableAutoRange('xy', True)
    txt.setText(f"RR ≈ {rr:.1f} bpm   (AC {ac_bpm:.1f}, FFT {fft_bpm:.1f})")

timer = pg.QtCore.QTimer(); timer.timeout.connect(update)
timer.start(int(HOP_SEC*1000))
pg.exec()
