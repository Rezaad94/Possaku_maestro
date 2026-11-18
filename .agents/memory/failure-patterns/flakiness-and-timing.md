# Failure Pattern: Zero Hard Sleep & Dynamic Waiting

- **Symptom**: Flows waste 40–60s+ per run on cold logins, repeated `delay.js` sleeps, and 7-second timeouts on absent `optional: true` / `when: visible:` guards.
- **Root Cause**: Re-wiping app state (`clearState: true`) on every flow and polling absent coachmarks repeatedly.

---

## Verified Resolutions

### 1. Session Reuse via `pages/login/ensure_logged_in.yaml`
All feature flows (Kasir, Dashboard, etc.) should use `pages/login/ensure_logged_in.yaml` instead of `login_flow.yaml`. It uses `launchApp: clearState: false, stopApp: true` + `extendedWaitUntil`, falling back to `login_flow.yaml` only when not already authenticated.

### 2. Replace `delay.js` with `extendedWaitUntil` / `assertVisible`
Never add `pages/delay.js` in feature flows. Maestro automatically waits for accessibility nodes.

### 3. Minimize 7-Second `optional: true` / `when:` Guards
Every absent `optional: true` or `when: visible:` element costs ~7 seconds. Only check `Mengerti` coachmarks on the first entry in a flow, not on subsequent loops.

### 4. Post-Airplane-Mode Recovery (`toggleAirplaneMode`)
After toggling Airplane Mode back OFF, Android emulator LTE takes ~5s to re-establish connectivity. Keep sorting checks after `toggleAirplaneMode` or rely on `login_flow.yaml`'s `"Masalah koneksi"` retry guard (`point: "540,1160"`).
