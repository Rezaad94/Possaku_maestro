# Headless Emulator Execution for Maestro

## Overview
Running Maestro tests on a **headless Android emulator** allows CI pipelines and local automation to execute without opening a UI window. Maestro interacts with the device solely through ADB, so the emulator can be started in *no‑window* mode.

## Prerequisites
1. **Android SDK** installed (`$ANDROID_HOME`).
2. **Emulator** (`emulator` binary) available in `$PATH` (usually `$ANDROID_HOME/emulator`).
3. **ADB** installed (`adb` in `$ANDROID_HOME/platform-tools`).
4. **Maestro** installed and reachable (`maestro --version` works).
5. At least one AVD that matches the target Android version (e.g., `android_15`).

## Step‑by‑Step Guide
1. **Start the emulator headlessly**
   ```bash
   # Replace <AVD_NAME> with the name of an existing AVD, e.g., android_15
   emulator -avd <AVD_NAME> -no-window -no-audio &
   ```
   - `-no-window` disables the UI.
   - `-no-audio` avoids unnecessary audio resources.
   - The trailing `&` runs the emulator in the background.

2. **Wait for the device to become ready**
   ```bash
   # Wait until the emulator reports as a device
   adb wait-for-device
   # Optionally, give it a few seconds for boot completion
   sleep 15
   # Verify
   adb devices
   ```
   You should see a line like `emulator-5554   device`.

3. **Run a Maestro flow against the headless device**
   ```bash
   maestro test \
     --device emulator-5554 \
     flows/login/valid_login_flow.yaml \
     --format html \
     --output headless_report.html
   ```
   - `--device` specifies the ADB device ID.
   - The `--format html` flag produces a report you can view locally.  The Maestro Viewer (`http://127.0.0.1:9999/`) still works because it proxies UI actions over ADB.

4. **Stop the emulator when finished**
   ```bash
   adb -s emulator-5554 emu kill
   ```

## Convenience Script
Create `start_headless.sh` in your project root for one‑click startup:
```bash
#!/usr/bin/env bash
# Choose the AVD you want to run headlessly
AVD_NAME="android_15"

echo "Launching $AVD_NAME in headless mode..."
emulator -avd "$AVD_NAME" -no-window -no-audio &

echo "Waiting for device to be ready..."
adb wait-for-device
# Give the OS a moment to finish booting (adjust if needed)
sleep 15

echo "Device ready:"
adb devices
```
Make it executable:
```bash
chmod +x start_headless.sh
```
Run it with `./start_headless.sh` before invoking Maestro.

## Known Limitations
- **Screenshots**: The emulator does not render a visible screen, but `adb exec-out screencap` still works, so screenshots in HTML reports are generated.
- **Hardware Features**: Certain UI tests that rely on hardware sensors (e.g., GPS) may need additional emulator flags (`-gps`, `-camera-front`, etc.).
- **Performance**: Headless mode is faster and consumes less RAM, but the first boot can still take ~30‑60 seconds.

## References in Project Docs
- The list of available AVDs is shown by `maestro list_devices`:
  - `android_11`
  - `android_15`
  - `android_9`
- The obsolete AVDs `android_6` and `android_10` have been deleted.

---
*This document is part of the automation rules for the Possaku Maestro project. It should be linked from `AGENTS.md` under a **Headless Execution** section.*