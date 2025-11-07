import time, struct, serial
SYNC=0xAA; VER=0x01
def crc16(data, crc=0xFFFF):
    for b in data:
        crc ^= (b<<8)
        for _ in range(8):
            if crc & 0x8000: crc=((crc<<1)^0x1021)&0xFFFF
            else: crc=(crc<<1)&0xFFFF
    return crc
def pack(msg_id, payload=b"", seq=0):
    hdr=bytes([SYNC,VER,msg_id])+len(payload).to_bytes(2,'little')+bytes([seq])
    c=crc16(hdr[1:]+payload).to_bytes(2,'little')
    return hdr+payload+c
def main():
    ser=serial.Serial('/dev/ttyAMA0',115200,timeout=0.05)
    while True:
        time.sleep(0.5)
if __name__=='__main__':
    main()
