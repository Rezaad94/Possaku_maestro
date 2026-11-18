# Failure Pattern: ADB Device Disconnection & Restarts

- **Symptom**: `maestro test` fails immediately with `Device not found` or hangs during command initialization.
- **Root Cause**: ADB server dropped connection or the emulator daemon crashed during execution.

---

## 🛠️ Verified Resolutions

### 1. Check Attached Devices
```bash
adb devices
```
If the device shows `offline` or `unauthorized`:
```bash
adb kill-server
adb start-server
adb devices
```

### 2. Verify Port & UDID
When multiple emulators or devices are attached, supply the explicit device ID to Maestro:
```bash
maestro test --device "emulator-5554" flows/...
```

### 3. Maestro MCP Check
When using Maestro MCP:
- Run `list_devices` to verify the exact connected `device_id`.
- Ensure `ANDROID_HOME=/Library/Android/sdk` and `platform-tools` are present in your MCP environment.

