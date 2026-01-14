
#!/usr/bin/env bash
set -euo pipefail

APP_USER="${APP_USER:-pi}"
APP_DIR="/home/${APP_USER}/p4s"
SCRIPT_PATH="${APP_DIR}/pi_uart_cam.py"
SERVICE_NAME="phreaks4security.service"

echo "[*] Creating app dir at ${APP_DIR}"
sudo -u "${APP_USER}" mkdir -p "${APP_DIR}"

echo "[*] Installing Python dependencies"
sudo apt-get update
sudo apt-get install -y python3-opencv python3-serial python3-flask alsa-utils

echo "[*] Copying script"
sudo cp ./pi_uart_cam.py "${SCRIPT_PATH}"
sudo chown "${APP_USER}:${APP_USER}" "${SCRIPT_PATH}"
sudo chmod +x "${SCRIPT_PATH}"

echo "[*] Writing systemd unit"
sudo tee /etc/systemd/system/${SERVICE_NAME} >/dev/null <<EOF
[Unit]
Description=Phreaks4Security Pi Integration
After=network-online.target

[Service]
Type=simple
User=${APP_USER}
Environment=P4S_ENABLE_FLASK=1
Environment=P4S_FLASK_PORT=8088
ExecStart=/usr/bin/python3 ${SCRIPT_PATH}
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

echo "[*] Enabling UART on RPi (ensure console is disabled on UART)"
# This assumes enable_uart=1 in /boot/config.txt and serial console disabled via raspi-config.

echo "[*] Reloading and enabling service"
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
echo "[*] You can start now with: sudo systemctl start ${SERVICE_NAME}"
echo "[*] Check logs: journalctl -u ${SERVICE_NAME} -f"
