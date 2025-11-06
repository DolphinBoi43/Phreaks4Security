# Phreaks4Security
Home security with STM32 (sensors) + Raspberry Pi (camera/MQTT).

## STM32 Quick Start
1) CubeMX: enable FreeRTOS + USART2 @115200.
2) Copy `Core/Src/app_freertos.c` and `Core/Inc/app_config.h` from this repo into your project.
3) Flash. UART prints `doorbell_pressed` or `motion_detected` on events.

## Raspberry Pi Quick Start
```bash
sudo apt update && sudo apt install -y python3-pip libcamera-tools mosquitto
sudo usermod -aG video $USER
sudo mkdir -p /opt/phreaks4security && sudo cp -r "Raspberry Pi Codespace/daemon"/* /opt/phreaks4security
cd /opt/phreaks4security && sudo pip3 install -r requirements.txt
sudo mkdir -p /var/lib/phreaks4security/media
sudo cp systemd/phreaks4d.service /etc/systemd/system/
sudo systemctl enable --now phreaks4d


### 3) Fix CONTRIBUTING.md
```bash
cat > CONTRIBUTING.md <<'EOF'
# Contributing
- Branch names: feat/*, fix/*, chore/*, docs/*.
- Conventional commits.
- PR checklist:
  - CI passes.
  - Tested on hardware or include a simulation note.
  - Update docs if behavior changes.
