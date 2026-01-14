import time, serial, sys
from .util_proto import pack
from .deframe import Deframer
from pi.camera.capture import capture_clip

MSG_CAMERA_EVENT   = 0x12
MSG_CAMERA_TRIGGER = 0x40
MSG_ACK            = 0x02

def main():
    try:
        ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.05)
    except Exception as e:
        print(f"[uart_bridge] Serial open failed: {e}", file=sys.stderr)
        return

    d = Deframer()
    last_hb = time.time()
    seq = 0

    while True:
        # Read and parse any incoming bytes
        try:
            data = ser.read(128)
        except Exception as e:
            print(f"[uart_bridge] Serial read error: {e}", file=sys.stderr)
            time.sleep(0.5)
            continue

        for b in data:
            out = d.feed(b)
            if out:
                msg_id, rxseq, payload = out
                if msg_id == MSG_CAMERA_EVENT and len(payload)>=1:
                    state = payload[0]
                    if state == 1:
                        path = capture_clip(5)
                        print(f"[bridge] capture => {path or 'FAILED'}")
                        try:
                            ser.write(pack(MSG_CAMERA_TRIGGER, b"", seq & 0xFF))
                            seq += 1
                        except Exception as e:
                            print(f"[uart_bridge] Serial write error: {e}", file=sys.stderr)
                else:
                    # ACK everything else for now
                    try:
                        ser.write(pack(MSG_ACK, b"", rxseq))
                    except Exception as e:
                        print(f"[uart_bridge] Serial write error: {e}", file=sys.stderr)

        # Optional heartbeat/log throttle
        if time.time() - last_hb > 5:
            print("[bridge] alive")
            last_hb = time.time()
        time.sleep(0.02)

if __name__ == '__main__':
    main()
