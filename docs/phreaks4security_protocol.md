
# Phreaks4Security UART Protocol (STM32 → Raspberry Pi)

**Baud:** 115200  **Data:** 8N1  **Encoding:** ASCII lines terminated by `\n`

## Message Frames
- `MOTION` — PIR detected motion.
- `DOOR_OPEN` — Reed switch indicates door/window open.
- `DOOR_CLOSED` — Reed switch closed.
- `CLEAR` — Sensor suite cleared.
- `HEARTBEAT` — Periodic aliveness signal (e.g., every 5s).
- `TEMP:<Celsius>` — Temperature reading (e.g., `TEMP:23.4`).
- `SMOKE:<ppm>` — Smoke level sample.
- `GAS:<ppm>` — Gas level sample.

## Error Frames
- `ERR:<code>` — e.g., `ERR:UART_OVERRUN`, `ERR:SENSOR_FAIL`

## Example STM32 Pseudocode
```c
// on PIR interrupt:
uart_println("MOTION");
// on reed switch open:
uart_println("DOOR_OPEN");
// periodic:
uart_println("HEARTBEAT");
// telemetry:
sprintf(buf, "TEMP:%0.1f", temp_c); uart_println(buf);
```

## Pi Behavior
- `MOTION` or `DOOR_OPEN` → play alert, capture image, log CSV.
- Other frames → log CSV.

## Reliability
- Keep messages ≤ 32 chars.
- Debounce sensors on STM32.
- Consider repeating critical alerts 2–3 times spaced 100 ms.
