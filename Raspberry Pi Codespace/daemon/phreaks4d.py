import os, time, json, serial, subprocess
from datetime import datetime
from pathlib import Path
import paho.mqtt.client as mqtt

MQTT_HOST=os.getenv("MQTT_HOST","localhost")
MQTT_TOPIC="phreaks4security/events"
MEDIA_DIR=Path(os.getenv("MEDIA_DIR","/var/lib/phreaks4security/media"))
SER_DEV=os.getenv("SER_DEV","/dev/ttyUSB0")  # adjust if using GPIO UART
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

def capture_clip(tag):
    ts=datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out=MEDIA_DIR/f"{ts}_{tag}.mp4"
    cmd=["libcamera-vid","-t","10000","-o",str(out)]
    subprocess.run(cmd, check=False)
    return str(out)

def on_event(evt, client):
    payload={"event":evt,"ts":int(time.time())}
    if evt in ("doorbell_pressed","motion_detected"):
        payload["media"]=capture_clip(evt)
    client.publish(MQTT_TOPIC, json.dumps(payload), qos=1, retain=False)

if __name__=="__main__":
    client=mqtt.Client(client_id="phreaks4d")
    client.connect(MQTT_HOST,1883,60); client.loop_start()
    try:
        ser=serial.Serial(SER_DEV, baudrate=115200, timeout=1)
        print(f"Listening on {SER_DEV}")
    except Exception as e:
        print(f"UART open failed: {e}")
        ser=None
    print("Daemon started.")
    while True:
        line=None
        if ser and ser.in_waiting:
            line=ser.readline().decode(errors="ignore").strip()
        if line in ("doorbell_pressed","motion_detected"):
            on_event(line, client)
        time.sleep(0.02)
