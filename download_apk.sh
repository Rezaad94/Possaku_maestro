#!/bin/bash
# ==============================================================================
# Possaku Mobile Automation - Universal APK Downloader & Installer
# Supports:
# 1. Google Drive sharing links (handles virus scan prompts & cookies)
# 2. Dropbox links (auto converts dl=0 to dl=1)
# 3. Direct HTTP/HTTPS URLs (S3, Firebase, GitHub Releases)
# ==============================================================================

set -e

URL="${1}"
OUTPUT="${2:-app.apk}"

if [ -z "$URL" ]; then
  echo "Usage: ./download_apk.sh <APK_URL_OR_GDRIVE_LINK> [output_file.apk]"
  exit 1
fi

echo "=========================================================="
echo " Downloading APK from: $URL"
echo " Destination: $OUTPUT"
echo "=========================================================="

# Remove previous download if exists
rm -f "$OUTPUT"

if [[ "$URL" =~ drive\.google\.com ]]; then
  echo "🔍 Google Drive link detected."

  # Extract File ID
  FILE_ID=$(echo "$URL" | sed -nE 's/.*(\/d\/|[?&]id=)([a-zA-Z0-9_-]+).*/\2/p')

  if [ -n "$FILE_ID" ]; then
    echo "Extracted File ID: $FILE_ID"
    TARGET_URL="https://drive.google.com/uc?id=${FILE_ID}&export=download"
  else
    TARGET_URL="$URL"
  fi

  # Prefer gdown for reliable Google Drive download of large files
  if ! command -v gdown >/dev/null 2>&1; then
    echo "Installing gdown for reliable Google Drive download..."
    python3 -m pip install --quiet gdown || pip install --quiet gdown || true
  fi

  if command -v gdown >/dev/null 2>&1; then
    echo "Downloading with gdown..."
    gdown "$TARGET_URL" -O "$OUTPUT" --fuzzy
  else
    echo "gdown not available, falling back to curl with cookie handler..."
    COOKIE_JAR=$(mktemp)
    # Step 1: Initial request to get cookies & confirmation token
    CONFIRM=$(curl -s -c "$COOKIE_JAR" -L "$TARGET_URL" | sed -nE 's/.*confirm=([0-9a-zA-Z_]+).*/\1/p' | head -n 1)
    if [ -n "$CONFIRM" ]; then
      echo "Passing confirmation token: $CONFIRM"
      curl -fSL -b "$COOKIE_JAR" "https://drive.google.com/uc?export=download&confirm=${CONFIRM}&id=${FILE_ID}" -o "$OUTPUT"
    else
      curl -fSL -b "$COOKIE_JAR" "$TARGET_URL" -o "$OUTPUT"
    fi
    rm -f "$COOKIE_JAR"
  fi

elif [[ "$URL" =~ dropbox\.com ]]; then
  echo "🔍 Dropbox link detected. Ensuring direct download mode (dl=1)..."
  DIRECT_URL=$(echo "$URL" | sed 's/[?&]dl=0//g')
  if [[ "$DIRECT_URL" == *"?"* ]]; then
    DIRECT_URL="${DIRECT_URL}&dl=1"
  else
    DIRECT_URL="${DIRECT_URL}?dl=1"
  fi
  curl -fSL -o "$OUTPUT" "$DIRECT_URL"

else
  echo "Downloading from direct URL..."
  curl -fSL -o "$OUTPUT" "$URL"
fi

# Verification: Check file existence and size
if [ ! -s "$OUTPUT" ]; then
  echo "❌ Error: Downloaded file is empty or missing!"
  exit 1
fi

# Verification: Verify file is actually a valid ZIP/APK (starts with PK) and not an HTML error page
MAGIC_BYTES=$(head -c 2 "$OUTPUT")
if [ "$MAGIC_BYTES" != "PK" ]; then
  echo "❌ Error: Downloaded file is not a valid APK binary!"
  echo "   First 200 bytes of response:"
  head -n 5 "$OUTPUT"
  echo ""
  echo "💡 Tip for Google Drive: Make sure the file sharing permission is set to:"
  echo "   'Anyone with the link can view' (Publicly accessible)."
  rm -f "$OUTPUT"
  exit 1
fi

FILE_SIZE=$(du -h "$OUTPUT" | awk '{print $1}')
echo "✅ APK successfully downloaded: $OUTPUT ($FILE_SIZE)"

# Optional auto-install if adb has an active device
if command -v adb >/dev/null 2>&1; then
  CONNECTED_DEV=$(adb devices 2>/dev/null | awk 'NR>1 && $2=="device" {print $1; exit}')
  if [ -n "$CONNECTED_DEV" ]; then
    echo "Installing $OUTPUT to connected Android device ($CONNECTED_DEV)..."
    adb -s "$CONNECTED_DEV" install -r "$OUTPUT"
    echo "✅ Successfully installed $OUTPUT to $CONNECTED_DEV"
  fi
fi

echo "=========================================================="
