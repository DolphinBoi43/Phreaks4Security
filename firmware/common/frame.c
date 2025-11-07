#include "frame.h"
#include "crc16.h"

enum { S_SYNC, S_HDR, S_PAY, S_CRC0, S_CRC1 };
static uint8_t s_state, s_hdr[5], s_idx, s_pay[PROTO_MAX_LEN], s_crc0;
static uint16_t s_len;

int proto_pack(uint8_t msg_id, const uint8_t* payload, uint16_t len, uint8_t seq,
               uint8_t* out, uint16_t* out_len) {
  if (len > PROTO_MAX_LEN) return -1;
  out[0] = PROTO_SYNC;
  out[1] = PROTO_VER;
  out[2] = msg_id;
  out[3] = (uint8_t)(len & 0xFF);
  out[4] = (uint8_t)(len >> 8);
  out[5] = seq;
  for (uint16_t i = 0; i < len; ++i) out[6 + i] = payload[i];
  uint16_t crc = crc16_ccitt_false(&out[1], 5 + len, 0xFFFF);
  out[6 + len] = (uint8_t)(crc & 0xFF);
  out[7 + len] = (uint8_t)(crc >> 8);
  *out_len = 8 + len;
  return 0;
}

int proto_try_deframe(uint8_t b, uint8_t* msg_id, uint8_t* seq,
                      uint8_t* payload, uint16_t* payload_len) {
  switch (s_state) {
    case S_SYNC:
      if (b == PROTO_SYNC) { s_state = S_HDR; s_idx = 0; }
      break;
    case S_HDR:
      s_hdr[s_idx++] = b;
      if (s_idx == 5) {
        if (s_hdr[0] != PROTO_VER) { s_state = S_SYNC; break; }
        s_len = (uint16_t)s_hdr[2] | ((uint16_t)s_hdr[3] << 8);
        if (s_len > PROTO_MAX_LEN) { s_state = S_SYNC; break; }
        s_state = (s_len == 0) ? S_CRC0 : S_PAY;
        s_idx = 0;
      }
      break;
    case S_PAY:
      s_pay[s_idx++] = b;
      if (s_idx == s_len) { s_state = S_CRC0; }
      break;
    case S_CRC0:
      s_crc0 = b; s_state = S_CRC1; break;
    case S_CRC1: {
      uint8_t crc1 = b;
      uint8_t buf[5 + PROTO_MAX_LEN];
      for (int i = 0; i < 5; ++i) buf[i] = s_hdr[i];
      for (uint16_t i = 0; i < s_len; ++i) buf[5 + i] = s_pay[i];
      uint16_t crc = crc16_ccitt_false(buf, 5 + s_len, 0xFFFF);
      if (((crc & 0xFF) == s_crc0) && ((crc >> 8) == crc1)) {
        *msg_id = s_hdr[1];
        *payload_len = s_len;
        *seq = s_hdr[4];
        for (uint16_t i = 0; i < s_len; ++i) payload[i] = s_pay[i];
        s_state = S_SYNC; return 1;
      }
      s_state = S_SYNC;
      break;
    }
  }
  return 0;
}
