#!/bin/bash

# ==============================================================================
# Possaku Mobile Automation - Network Restoration Utility
# Guarantees Airplane Mode is Disabled and Wi-Fi / Cellular Data are Enabled
# ==============================================================================

if [ -n "$1" ]; then
  DEVICE="$1"
elif [ -n "$DEVICE" ]; then
  DEVICE="$DEVICE"
else
  CONNECTED_DEV=$(adb devices 2>/dev/null | awk 'NR>1 && $2=="device" {print $1; exit}')
  DEVICE="${CONNECTED_DEV:-emulator-5554}"
fi

echo "=========================================================="
echo " Restoring Network Connectivity on $DEVICE"
echo "=========================================================="

# Check ADB device status
if ! adb -s "$DEVICE" get-state >/dev/null 2>&1; then
  echo "⚠️ Warning: Device $DEVICE not found in adb devices list."
  adb devices
  exit 1
fi

# 1. Disable Airplane Mode
adb -s "$DEVICE" shell cmd connectivity airplane-mode disable 2>/dev/null

# 2. Enable Wi-Fi
adb -s "$DEVICE" shell svc wifi enable 2>/dev/null

# 3. Enable Cellular Data
adb -s "$DEVICE" shell svc data enable 2>/dev/null

# 4. Read back global settings to confirm
AIRPLANE_STATE=$(adb -s "$DEVICE" shell settings get global airplane_mode_on 2>/dev/null | tr -d '\r\n ')

if [ "$AIRPLANE_STATE" = "0" ]; then
  echo "✅ Airplane Mode: DISABLED (Online)"
  echo "✅ Wi-Fi: ENABLED"
  echo "✅ Cellular Data: ENABLED"
  echo "Internet successfully restored on $DEVICE!"
else
  echo "⚠️ Warning: Airplane mode returned '$AIRPLANE_STATE' (expected 0)"
fi
echo "=========================================================="
