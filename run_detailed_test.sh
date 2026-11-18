#!/bin/bash

# Ensure script is run from project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

REPORTS_DIR="reports"
mkdir -p "$REPORTS_DIR"

TARGET="${1:-flows/kasir/}"
OUTPUT_REPORT="${2}"
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

# Trap ensures internet is restored even if the test fails, crashes, or is aborted
trap ensure_online EXIT INT TERM

# Ensure online before running any test flow
ensure_online

# If output report is not specified, generate a meaningful default name inside reports/
if [ -z "$OUTPUT_REPORT" ]; then
  if [ -d "$TARGET" ]; then
    CLEAN_DIR_NAME=$(basename "$TARGET")
    OUTPUT_REPORT="${REPORTS_DIR}/${CLEAN_DIR_NAME}_full_report.html"
  else
    BASE_FILE=$(basename "$TARGET" .yaml)
    OUTPUT_REPORT="${REPORTS_DIR}/${BASE_FILE}_detailed.html"
  fi
else
  # If a filename without directory was given, place it inside reports/
  if [[ "$OUTPUT_REPORT" != *"/"* ]]; then
    OUTPUT_REPORT="${REPORTS_DIR}/${OUTPUT_REPORT}"
  fi
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_REPORT")"

# Load environment arguments from config/env.yaml if file exists
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
if [ -n "$PHONE_NUMBER" ] && [[ "$ENV_ARGS" != *"PHONE_NUMBER="* ]]; then
  ENV_ARGS="$ENV_ARGS -e PHONE_NUMBER=$PHONE_NUMBER"
fi
if [ -n "$PIN" ] && [[ "$ENV_ARGS" != *"PIN="* ]]; then
  ENV_ARGS="$ENV_ARGS -e PIN=$PIN"
fi
if [ -n "$APP_ID" ] && [[ "$ENV_ARGS" != *"APP_ID="* ]]; then
  ENV_ARGS="$ENV_ARGS -e APP_ID=$APP_ID"
fi

echo "=========================================================="
echo " Running Maestro Test with Detailed Step-Level Reporting"
echo " Target: $TARGET"
echo " Output: $OUTPUT_REPORT"
echo "=========================================================="

# Clean existing debug dir if present
rm -rf "$DEBUG_DIR"

# Run Maestro with HTML format and debug logs
maestro test \
  --device "$DEVICE_TARGET" \
  --format html \
  --output "$OUTPUT_REPORT" \
  --debug-output "$DEBUG_DIR" \
  $ENV_ARGS \
  $TARGET

MAESTRO_EXIT_CODE=$?

if [ -f "$OUTPUT_REPORT" ]; then
  echo ""
  echo "Enriching $OUTPUT_REPORT with per-step execution logs and screenshots..."
  python3 inject_steps.py --report "$OUTPUT_REPORT" --debug "$DEBUG_DIR"
  echo "=========================================================="
  echo " Detailed report ready: $OUTPUT_REPORT"
  echo " Open with: open $OUTPUT_REPORT"
  echo "=========================================================="
else
  echo ""
  echo "⚠️ Maestro did not produce a report (exit code: $MAESTRO_EXIT_CODE). Check device connection."
fi

# Explicitly guarantee online state at end of script
ensure_online

exit $MAESTRO_EXIT_CODE
