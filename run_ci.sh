#!/bin/bash
# ==============================================================================
# Possaku Mobile Automation - CI Test Runner for Android Emulator
# ==============================================================================

set -e

# Ensure Maestro is in PATH
export PATH="/usr/local/bin:$HOME/.maestro/bin:$PATH"

echo "=========================================================="
echo " Starting Possaku Android Emulator CI Execution"
echo "=========================================================="

# 0. Generate config/env.yaml from CI secrets and environment if not present
mkdir -p config
if [ ! -f "config/env.yaml" ]; then
  echo "Generating config/env.yaml from environment variables & secrets..."
  cat <<EOF > config/env.yaml
APP_ID: "${APP_ID:-com.cloudiex.possaku}"
PHONE_NUMBER: "${PHONE_NUMBER}"
PIN: "${PIN}"
INVALID_PHONE: "${INVALID_PHONE:-085672222335}"
INVALID_PIN: "${INVALID_PIN:-111222}"
INACTIVE_PHONE: "${INACTIVE_PHONE:-0856633633}"
EOF
  echo "config/env.yaml successfully created."
fi

# 1. Device check & online guarantee
echo "Connected Android devices on Linux runner:"
adb devices
./restore_internet.sh

# Dismiss lockscreen/keyguard on emulator
adb shell input keyevent 82 2>/dev/null || true
adb shell wm dismiss-keyguard 2>/dev/null || true

# 2. Install APK if URL (including Google Drive) or local path is provided
if [ -n "$APK_URL" ]; then
  echo "Downloading and installing APK from URL: $APK_URL"
  ./download_apk.sh "$APK_URL" app.apk
elif [ -n "$APK_PATH" ] && [ -f "$APK_PATH" ]; then
  echo "Installing APK from path: $APK_PATH"
  adb install -r -d -g "$APK_PATH" || adb install -r "$APK_PATH"
fi

# Ensure runtime permissions are granted if app.apk was downloaded
if [ -f "app.apk" ]; then
  echo "Ensuring app runtime permissions are granted..."
  adb install -r -d -g app.apk 2>/dev/null || true
fi

# 3. Resolve target flow (default to regression suite if empty)
TARGET="${TARGET_FLOW:-.maestro/regression_suite.yaml}"

echo "=========================================================="
echo " Executing Target: $TARGET"
echo "=========================================================="

./run_suite.sh "$TARGET"
