#pragma once
#include <stdint.h>
#include "protocol.h"

#define PROTO_MAX_LEN 128

int proto_pack(uint8_t msg_id, const uint8_t* payload, uint16_t len, uint8_t seq,
               uint8_t* out, uint16_t* out_len);

int proto_try_deframe(uint8_t byte, uint8_t* msg_id, uint8_t* seq,
                      uint8_t* payload, uint16_t* payload_len);
