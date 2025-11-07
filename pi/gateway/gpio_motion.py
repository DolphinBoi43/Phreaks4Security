import time, struct
import serial
try:
    import RPi.GPIO as GPIO
except ImportError:
    class GPIOStub:
        BCM=IN=PUD_DOWN=None
        def setmode(self,*a,**k): pass
        def setup(self,*a,**k): pass
        def input(self,*a,**k): return 0
        def add_event_detect(self,*a,**k): pass
        def cleanup(self): pass
    GPIO=GPIOStub()
PIN=17
SYNC=0xAA; VER=0x01; MSG_CAMERA_EVENT=0x12; MSG_CAMERA_TRIGGER=0x40
def crc16(data, crc=0xFFFF):
    for b in data:
        crc ^= (b<<8)
        for _ in range(8):
            if crc & 0x8000: crc=((crc<<1)^0x1021)&0xFFFF
            else: crc=(crc<<1)&0xFFFF
    return crc
def pack(msg_id,payload=b"",seq=0):
    hdr=bytes([SYNC,VER,msg_id])+len(payload).to_bytes(2,'little')+bytes([seq])
    c=crc16(hdr[1:]+payload).to_bytes(2,'little')
    return hdr+payload+c
def main():
    ser=serial.Serial('/dev/ttyAMA0',115200,timeout=0.02)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    last=0
    while True:
        s=GPIO.input(PIN)
        if s!=last:
            ts=int(time.time()*1000)
            payload=bytes([1 if s else 0])+ts.to_bytes(4,'little')+bytes([0])
            ser.write(pack(MSG_CAMERA_EVENT,payload))
            if s==1: ser.write(pack(MSG_CAMERA_TRIGGER,b""))
            last=s
        time.sleep(0.05)
if __name__=='__main__':
    main()
