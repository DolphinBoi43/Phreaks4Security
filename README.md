# Home Security System

- MCU-A (STM32L476): UART to Pi and to MCU-B.
- MCU-B: actuators.
- Pi: camera + motion sensor as primary trigger.

## Layout
- firmware/mcu-a/stm32cube
- firmware/mcu-b
- firmware/common
- pi/gateway, pi/camera
- docs (protocol, wiring, diagrams)

## Quick start (Pi)
```
pip install pyserial
python pi/gateway/gpio_motion.py
```
