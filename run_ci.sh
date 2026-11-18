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

# 1. Device check & online guarantee
echo "Connected Android devices on Linux runner:"
adb devices
./restore_internet.sh

# 2. Install APK if URL (including Google Drive) or local path is provided
if [ -n "$APK_URL" ]; then
  echo "Downloading and installing APK from URL: $APK_URL"
  ./download_apk.sh "$APK_URL" app.apk
elif [ -n "$APK_PATH" ] && [ -f "$APK_PATH" ]; then
  echo "Installing APK from path: $APK_PATH"
  adb install -r "$APK_PATH"
fi

# 3. Resolve target flow (default to regression suite if empty)
TARGET="${TARGET_FLOW:-.maestro/regression_suite.yaml}"

echo "=========================================================="
echo " Executing Target: $TARGET"
echo "=========================================================="

./run_suite.sh "$TARGET"
