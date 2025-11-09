
#!/usr/bin/env python3
"""
Phreaks4Security: Raspberry Pi Integration
- Listens on UART for STM32 alerts
- Captures an image on alert
- Plays a local buzzer/sound
- Logs events to CSV
- (Optional) exposes a minimal Flask endpoint to view last snapshot
Hardware:
  - UART: /dev/serial0 (enable via raspi-config; disable console login)
  - Camera: /dev/video0 or PiCamera2 (USB cam also supported with OpenCV)
  - Buzzer: local audio device (plays WAV) OR simple GPIO pin (see TODO)
"""
import os
import sys
import time
import csv
import threading
from datetime import datetime
from pathlib import Path

import serial
import cv2

# === CONFIG ===
UART_PORT = os.environ.get("P4S_UART_PORT", "/dev/serial0")
UART_BAUD = int(os.environ.get("P4S_UART_BAUD", "115200"))
CAPTURE_DIR = Path(os.environ.get("P4S_CAPTURE_DIR", "/home/pi/phreaks_captures"))
LOG_FILE = Path(os.environ.get("P4S_LOG_FILE", str(CAPTURE_DIR / "events.csv")))
ALERT_SOUND = os.environ.get("P4S_ALERT_SOUND", "/home/pi/alert.wav")  # provide a wav file
CAMERA_INDEX = int(os.environ.get("P4S_CAMERA_INDEX", "0"))  # 0 for default /dev/video0

ENABLE_FLASK = os.environ.get("P4S_ENABLE_FLASK", "0") == "1"
FLASK_PORT = int(os.environ.get("P4S_FLASK_PORT", "8088"))

CAPTURE_DIR.mkdir(parents=True, exist_ok=True)

# === UART ===
ser = serial.Serial(UART_PORT, UART_BAUD, timeout=1)

# === Camera ===
cam = cv2.VideoCapture(CAMERA_INDEX)
if not cam.isOpened():
    print("[ERR] Could not open camera index", CAMERA_INDEX, file=sys.stderr)

# === Utils ===
def now_ts():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def log_event(event_type, detail, image_path=""):
    is_new = not LOG_FILE.exists()
    with LOG_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp", "event_type", "detail", "image_path"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), event_type, detail, image_path])

def capture_image(prefix="capture"):
    ret, frame = cam.read()
    if not ret:
        print("[WARN] Failed to read frame, retrying once...")
        time.sleep(0.1)
        ret, frame = cam.read()
    if ret:
        fname = f"{prefix}_{now_ts()}.jpg"
        fpath = CAPTURE_DIR / fname
        cv2.imwrite(str(fpath), frame)
        return str(fpath)
    return ""

def play_alert():
    # Prefer aplay on RPi. You can also wire a buzzer to a GPIO pin and toggle it (TODO if needed).
    if os.path.isfile(ALERT_SOUND):
        os.system(f"aplay -q {ALERT_SOUND} &")

# === Flask (optional) ===
app = None
last_image_path = [""]  # mutable holder for latest image path

def flask_worker():
    from flask import Flask, send_file, jsonify
    flask_app = Flask(__name__)

    @flask_app.get("/health")
    def health():
        return {"ok": True, "last_image": last_image_path[0]}

    @flask_app.get("/last.jpg")
    def last_jpg():
        p = last_image_path[0]
        if p and os.path.exists(p):
            return send_file(p, mimetype="image/jpeg")
        return jsonify({"error": "no image yet"}), 404

    flask_app.run(host="0.0.0.0", port=FLASK_PORT, debug=False)

if ENABLE_FLASK:
    t = threading.Thread(target=flask_worker, daemon=True)
    t.start()

print("[P4S] Listening on", UART_PORT, "@", UART_BAUD)
try:
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
        except Exception as e:
            line = ""
        if not line:
            continue
        # Expected frames, eg.: MOTION, DOOR_OPEN, DOOR_CLOSED, HEARTBEAT, TEMP:23.5
        evt = line.upper()
        img_path = ""
        if evt in ("MOTION", "DOOR_OPEN"):
            play_alert()
            img_path = capture_image(prefix=evt.lower())
            last_image_path[0] = img_path or last_image_path[0]
            log_event("ALERT", evt, img_path)
            print(f"[P4S] ALERT {evt} -> {img_path}")
        elif evt.startswith("TEMP:") or evt.startswith("SMOKE:") or evt.startswith("GAS:"):
            log_event("SENSOR", evt, "")
            print("[P4S] SENSOR", evt)
        elif evt in ("DOOR_CLOSED", "CLEAR"):
            log_event("INFO", evt, "")
            print("[P4S] INFO", evt)
        elif evt == "HEARTBEAT":
            # periodic check from STM32
            print("[P4S] ♥ heartbeat")
        else:
            # unknown line; still log for troubleshooting
            log_event("RAW", evt, "")
            print("[P4S] RAW:", evt)
except KeyboardInterrupt:
    pass
finally:
    cam.release()
    ser.close()
    print("[P4S] Exiting...")
