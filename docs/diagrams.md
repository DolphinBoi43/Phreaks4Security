
# Phreaks4Security Diagrams (Mermaid)

## Hardware Block Diagram
```mermaid
graph TD
  subgraph Power
    AC120[AC 120V] --> PSU5V[5V DC Supply]
    PSU5V --> RPI[ Raspberry Pi 3B+ ]
    PSU5V --> STM32[ STM32 MCU ]
  end

  STM32 -->|UART 115200| RPI
  PIR[PIR Sensor] --> STM32
  Reed[Magnetic Reed Switch] --> STM32

  Cam[Pi Camera] -->|CSI| RPI
  USBMic[USB Microphone] -->|USB| RPI
  Buzzer[Buzzer / Speaker] -->|Audio Out / GPIO| RPI

  RPI -->|Wi‑Fi| Phone[Local Phone/PC UI]
  LCD[Local LCD (opt)] --> RPI
```

## Software Block Diagram
```mermaid
graph LR
  subgraph STM32 Firmware
    A1[Sensor Drivers<br/>PIR/Reed] --> A2[Debounce & State]
    A2 --> A3[UART TX Task]
  end

  subgraph Raspberry Pi App (Python)
    B1[UART Listener] --> B2[Event Router]
    B2 --> B3[Camera Capture]
    B2 --> B4[Audio Alert]
    B2 --> B5[CSV Logger]
    B2 --> B6[(Snapshots Dir)]
    B5 --> B7[(events.csv)]
  end

  subgraph Optional UI
    C1[Flask /last.jpg] --> User[Browser]
    C2[/health] --> User
  end

  A3 -->|ASCII Frames| B1
  B6 --> C1
```
