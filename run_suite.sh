#!/bin/bash

# Ensure the script is run from the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

REPORTS_DIR="reports"
mkdir -p "$REPORTS_DIR"
OUTPUT_REPORT="${REPORTS_DIR}/regression_suite_report.html"
DEBUG_DIR="debug_out"

# Dynamic Device Resolution (supports CI runners, custom env, or adb fallback)
if [ -z "$DEVICE_TARGET" ]; then
  if [ -n "$DEVICE" ]; then
    DEVICE_TARGET="$DEVICE"
  else
    CONNECTED_DEV=$(adb devices 2>/dev/null | awk 'NR>1 && $2=="device" {print $1; exit}')
    if [ -n "$CONNECTED_DEV" ]; then
      DEVICE_TARGET="$CONNECTED_DEV"
    else
      echo "⚠️ Warning: No active Android device found in 'adb devices'."
      echo "   Please launch your emulator (e.g., 'emulator -avd android_11') or connect a device."
      DEVICE_TARGET="emulator-5554"
    fi
  fi
fi

# ------------------------------------------------------------------------------
# Network Safety Guard: Guarantee Internet / Online Mode is Always Restored
# ------------------------------------------------------------------------------
ensure_online() {
  if command -v adb >/dev/null 2>&1; then
    adb -s "$DEVICE_TARGET" shell cmd connectivity airplane-mode disable 2>/dev/null
    adb -s "$DEVICE_TARGET" shell svc wifi enable 2>/dev/null
    adb -s "$DEVICE_TARGET" shell svc data enable 2>/dev/null
  fi
}

# Trap ensures internet is restored even if tests fail, crash, or are aborted
trap ensure_online EXIT INT TERM

# Ensure online before starting regression suite
ensure_online

# Read environment variables from config/env.yaml if file exists
ENV_ARGS=""
if [ -f "config/env.yaml" ]; then
  ENV_ARGS=$(awk -F: '/^[A-Za-z0-9_]+/ {
    key = $1;
    val = substr($0, length($1) + 2);
    gsub(/^[ \t"'\''\r\n]+|[ \t"'\''\r\n]+$/, "", val);
    print "-e " key "=" val
  }' config/env.yaml | tr '\n' ' ')
fi

# Load local environment overrides from config/env.local.yaml (ignored by git)
if [ -f "config/env.local.yaml" ]; then
  LOCAL_ARGS=$(awk -F: '/^[A-Za-z0-9_]+/ {
    key = $1;
    val = substr($0, length($1) + 2);
    gsub(/^[ \t"'\''\r\n]+|[ \t"'\''\r\n]+$/, "", val);
    print "-e " key "=" val
  }' config/env.local.yaml | tr '\n' ' ')
  ENV_ARGS="$ENV_ARGS $LOCAL_ARGS"
fi

# Allow environment variables / CI secrets to override or supplement env.yaml
if [[ "$ENV_ARGS" != *"APP_ID="* ]]; then
  ENV_ARGS="$ENV_ARGS -e APP_ID=${APP_ID:-com.cloudiex.possaku}"
fi
if [ -n "$PHONE_NUMBER" ] && [[ "$ENV_ARGS" != *"PHONE_NUMBER="* ]]; then
  ENV_ARGS="$ENV_ARGS -e PHONE_NUMBER=$PHONE_NUMBER"
fi
if [ -n "$PIN" ] && [[ "$ENV_ARGS" != *"PIN="* ]]; then
  ENV_ARGS="$ENV_ARGS -e PIN=$PIN"
fi
if [ -n "$INVALID_PHONE" ] && [[ "$ENV_ARGS" != *"INVALID_PHONE="* ]]; then
  ENV_ARGS="$ENV_ARGS -e INVALID_PHONE=$INVALID_PHONE"
fi
if [ -n "$INVALID_PIN" ] && [[ "$ENV_ARGS" != *"INVALID_PIN="* ]]; then
  ENV_ARGS="$ENV_ARGS -e INVALID_PIN=$INVALID_PIN"
fi

# Support optional custom target: ./run_suite.sh [target_directory_or_flow] [output_report]
TARGET="${1}"
if [ -z "$TARGET" ] || [ "$TARGET" = ".maestro/regression_suite.yaml" ]; then
  OUTPUT_REPORT="${REPORTS_DIR}/regression_suite_report.html"
  FLOW_FILES=$(awk '/runFlow:/ {gsub(/\.\.\//, ""); print $NF}' .maestro/regression_suite.yaml | tr '\n' ' ')
  if [ -z "$FLOW_FILES" ]; then
    echo "Error: No flow files found in .maestro/regression_suite.yaml"
    exit 1
  fi
  SUITE_TARGET="$FLOW_FILES"
else
  if [ -n "$2" ]; then
    OUTPUT_REPORT="$2"
    if [[ "$OUTPUT_REPORT" != *"/"* ]]; then
      OUTPUT_REPORT="${REPORTS_DIR}/${OUTPUT_REPORT}"
    fi
  else
    CLEAN_NAME=$(basename "$TARGET" .yaml)
    OUTPUT_REPORT="${REPORTS_DIR}/${CLEAN_NAME}_suite_report.html"
  fi
  SUITE_TARGET="$TARGET"
fi

echo "=========================================================="
echo " Running Maestro Regression Suite"
echo " Target: ${TARGET:-.maestro/regression_suite.yaml}"
echo " Report: $OUTPUT_REPORT"
echo "=========================================================="

# Clean existing debug dir if present
rm -rf "$DEBUG_DIR"

# Run Maestro with html format and debug output options
# Start background watchdog to prevent any test failure from stranding the device in airplane mode
(
  AP_COUNT=0
  while true; do
    sleep 5
    AP_STATE=$(adb -s "$DEVICE_TARGET" shell settings get global airplane_mode_on 2>/dev/null | tr -d '\r\n')
    if [ "$AP_STATE" = "1" ]; then
      AP_COUNT=$((AP_COUNT + 5))
      if [ $AP_COUNT -ge 20 ]; then
        echo "⚠️ Watchdog: Device was left in Airplane Mode for >= 20s. Restoring connectivity..."
        ensure_online
        AP_COUNT=0
      fi
    else
      AP_COUNT=0
    fi
  done
) &
WATCHDOG_PID=$!
trap "kill $WATCHDOG_PID 2>/dev/null; ensure_online" EXIT INT TERM

maestro test \
  --device "$DEVICE_TARGET" \
  --format html \
  --output "$OUTPUT_REPORT" \
  --debug-output "$DEBUG_DIR" \
  $ENV_ARGS \
  $SUITE_TARGET

MAESTRO_EXIT_CODE=$?

# Terminate watchdog
kill $WATCHDOG_PID 2>/dev/null

if [ -f "$OUTPUT_REPORT" ]; then
  echo ""
  echo "Enriching $OUTPUT_REPORT with Playwright-style steps and screenshots..."
  python3 inject_steps.py --report "$OUTPUT_REPORT" --debug "$DEBUG_DIR"
  echo "=========================================================="
  echo " Regression report ready: $OUTPUT_REPORT"
  echo " Open with: open $OUTPUT_REPORT"
  echo "=========================================================="
else
  echo ""
  echo "⚠️ Maestro did not produce a report (exit code: $MAESTRO_EXIT_CODE). Check device connection."
fi

# Clean up temporary debug output folder
rm -rf "$DEBUG_DIR"

# Explicitly guarantee online state at end of suite run
ensure_online

exit $MAESTRO_EXIT_CODE
