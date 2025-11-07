#pragma once
#include <stdint.h>

#define PROTO_SYNC 0xAA
#define PROTO_VER  0x01

enum {
  MSG_HELLO = 0x01,
  MSG_ACK = 0x02,
  MSG_SENSOR_EVENT = 0x10,
  MSG_HEARTBEAT = 0x11,
  MSG_CAMERA_EVENT = 0x12,
  MSG_ACTUATE = 0x20,
  MSG_CONFIG_SET = 0x30,
  MSG_CONFIG_GET = 0x31,
  MSG_CAMERA_TRIGGER = 0x40,
  MSG_CAMERA_STATUS = 0x41,
  MSG_CLIP_META = 0x42
};

typedef struct __attribute__((packed)) {
  uint8_t sync;
  uint8_t ver;
  uint8_t msg_id;
  uint16_t len;
  uint8_t seq;
} proto_hdr_t;
