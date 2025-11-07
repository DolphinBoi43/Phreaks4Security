SYNC=0xAA; VER=0x01

class Deframer:
    def __init__(self, max_len=256):
        self.s=0; self.h=[]; self.p=bytearray(); self.len=0; self.max=max_len

    @staticmethod
    def _crc16(data, crc=0xFFFF):
        for b in data:
            crc ^= (b<<8)
            for _ in range(8):
                crc = ((crc<<1)^0x1021)&0xFFFF if (crc & 0x8000) else (crc<<1)&0xFFFF
        return crc

    def feed(self, b):
        if self.s==0:            # SYNC
            if b==SYNC: self.s=1; self.h=[]; self.p.clear()
        elif self.s==1:          # HDR (VER,ID,LENlo,LENhi,SEQ)
            self.h.append(b)
            if len(self.h)==5:
                if self.h[0]!=VER: self.s=0; return None
                self.len = self.h[2] | (self.h[3]<<8)
                if self.len>self.max: self.s=0; return None
                self.s = 3 if self.len else 4
        elif self.s==3:          # PAYLOAD
            self.p.append(b)
            if len(self.p)==self.len: self.s=4
        elif self.s==4:          # CRC0
            self.c0=b; self.s=5
        elif self.s==5:          # CRC1 -> validate
            crc = self._crc16(bytes(self.h)+bytes(self.p))
            if (crc & 0xFF)==self.c0 and (crc>>8)==b:
                msg_id=self.h[1]; seq=self.h[4]
                frame = (msg_id, seq, bytes(self.p))
                self.s=0
                return frame
            self.s=0
        return None
