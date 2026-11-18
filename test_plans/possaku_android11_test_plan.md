# Possaku Android 11 – Comprehensive Test Plan

**Project**: Possaku Maestro Automation
**Target Device**: Android 11 AVD (`android_11`)
**Test Framework**: Maestro (YAML flows) – executed via headless emulator (see `headless_emulator_rules.md`).

---
## 1. Scope & Objectives
| Item | Description |
|------|-------------|
| **App version** | Possaku Android application (latest build deployed for Android 11). |
| **Target platform** | Android 11 emulator (`android_11`). |
| **Goal** | Verify that **all user‑visible features** function correctly, meet functional and regression requirements, and obey Hunt’s zero‑sleep policy. |
| **Out of scope** | Internal unit tests, backend API contract tests, performance/load testing (covered elsewhere). |

---
## 2. Feature Matrix
| Feature | Related Flow(s) | Primary Tags | Test Types |
|---------|----------------|--------------|-----------|
| **Login** | `login/valid_login_flow.yaml`<br>`login/invalid_login_flow.yaml` | regression‑p1, login | functional, negative, regression |
| **Dashboard – Overview** | `dashboard/overview_flow.yaml` | regression‑p1, dashboard, metrics | functional, UI visibility |
| **Dashboard – Filter** | `dashboard/filter_flow.yaml` | regression‑p2, dashboard, filters | functional, UI interaction |
| **Dashboard – Open/Close Store** | `dashboard/open_close_store_flow.yaml` | regression‑p2, dashboard, store‑control | functional |
| **Kasir – Cart Quantity** | `kasir/cart_qty_flow.yaml` | regression‑p2, kasir, cart | functional |
| **Kasir – Catalog Quantity** | `kasir/catalog_qty_flow.yaml` | regression‑p2, kasir, catalog | functional |
| **Usahaku – Open/Close Store** | `usahaku/open_close_store_flow.yaml` | regression‑p2, usahaku, store‑control | functional |
| **Lain‑Lain – Store Settings (Non‑linear)** | `lain_lain/nonline_store_setting_flow.yaml` | regression‑p2, lain‑lain, settings | functional |

> **Note**: The above flows are the *baseline* coverage. Additional edge‑case tests are listed in Section 4.

---
## 3. Test Environment
1. **Emulator** – `android_11` AVD started headlessly (`emulator -avd android_11 -no-window -no-audio &`).
2. **ADB** – ensure `adb devices` shows `emulator-5554   device`.
3. **Maestro** – latest version (`maestro --version` → 2.12.1). Use the viewer URL (`http://127.0.0.1:9999/`) for HTML reports.
4. **Test Data** – credentials stored in `pages/login/login_credential.js`; use the `dev` environment values.
5. **Artifacts** – HTML report per flow, screenshots (captured via ADB screen‑capture), and a consolidated CSV summary.

---
## 4. Detailed Test Cases
Below each test case references the existing flow file and lists any **additional assertions** or **data variations** that should be added.

### 4.1 Login
| TC ID | Description | Flow | Additional Steps |
|-------|-------------|------|------------------|
| **LOGIN‑POS‑001** | Valid login with correct phone & PIN | `login/valid_login_flow.yaml` | Verify welcome toast contains user name; capture post‑login dashboard screenshot. |
| **LOGIN‑POS‑002** | Invalid login – wrong PIN | `login/invalid_login_flow.yaml` | Ensure error message `PIN salah` appears; attempt a second login with correct PIN to confirm recovery. |
| **LOGIN‑POS‑003** | Invalid login – unregistered phone | `login/invalid_login_flow.yaml` (modify env `phoneNumber` to a non‑existent number) | Verify “Akun tidak ditemukan” error.

### 4.2 Dashboard – Overview
| TC ID | Description | Flow | Additional Assertions |
|-------|-------------|------|----------------------|
| **DASH‑OV‑001** | Verify all metric labels & values are visible after login | `dashboard/overview_flow.yaml` | Add `assertVisible` for each metric value element (`${output.dashboard_page.totalPenjualanValue}` etc.). |
| **DASH‑OV‑002** | Data refresh – pull‑to‑refresh works | Duplicate `overview_flow.yaml` with added swipe gesture (`swipe: down`) before assertions. |

### 4.3 Dashboard – Filter
| TC ID | Description | Flow | Extra Checks |
|-------|-------------|------|-------------|
| **DASH‑FL‑001** | Filter "Hari ini" shows today’s transactions only | `dashboard/filter_flow.yaml` (already selects Hari ini) | After selection, assert that the list count matches the API response for today (optional JSON extraction). |
| **DASH‑FL‑002** | Filter "Minggu ini" and "Bulan ini" – range correctness | Create two flows based on `filter_flow.yaml` with respective option taps; add date‑range label assertions. |

### 4.4 Dashboard – Open/Close Store
| TC ID | Description | Flow |
|-------|-------------|------|
| **DASH‑SC‑001** | Open store from closed state | `dashboard/open_close_store_flow.yaml` (first half) |
| **DASH‑SC‑002** | Close store when already open | Same flow – add pre‑condition to ensure store is open, then tap close. |

### 4.5 Kasir – Cart Quantity
| TC ID | Description | Flow |
|-------|-------------|------|
| **KASIR‑CART‑001** | Add item to cart, increase quantity, verify total updates | `kasir/cart_qty_flow.yaml` |
| **KASIR‑CART‑002** | Decrease quantity to zero, verify item removal | Extend flow with tap on minus until count 0, then `assertNotVisible` for item row. |

### 4.6 Kasir – Catalog Quantity
| TC ID | Description | Flow |
|-------|-------------|------|
| **KASIR‑CAT‑001** | Browse catalog, select an item, add to cart, verify catalog count changes | `kasir/catalog_qty_flow.yaml` |
| **KASIR‑CAT‑002** | Search functionality – nonexistent product yields “Tidak ada hasil” | Duplicate flow with search term `"xyz_not_exists"`; add `assertVisible: "Tidak ada hasil"`. |

### 4.7 Usahaku – Open/Close Store
| TC ID | Description | Flow |
|-------|-------------|------|
| **USAH‑SC‑001** | Open store from usahaku screen | `usahaku/open_close_store_flow.yaml` |
| **USAH‑SC‑002** | Close store and verify status label changes to “Tutup” | Extend flow with close tap and `assertVisible: "Tutup"`. |

### 4.8 Lain‑Lain – Store Settings (Non‑linear)
| TC ID | Description | Flow |
|-------|-------------|------|
| **LAIN‑SET‑001** | Open store settings, toggle a switch, save, verify persisted state | `lain_lain/nonline_store_setting_flow.yaml` |
| **LAIN‑SET‑002** | Attempt to save with mandatory field empty – expect validation error | Modify flow to clear required field before save, add `assertVisible: "Wajib diisi"`. |

---
## 5. Test Data & Parameterization
- **Credentials** – stored in `pages/login/login_credential.js`. Use `dev` env values for all flows.
- **Phone numbers** – valid: `${output.login_credential.dev.validPhoneNumber2}`; invalid: `"+6281234567890"` (non‑registered).
- **PINs** – valid: `${output.login_credential.dev.validPIN}`; invalid: `"0000"`.
- **Search terms** – valid product names from seed data; invalid term `"xyz_not_exists"`.

All flows support **environment variables** (`env:` block). When creating new test cases, add a new `env:` section to inject the above data.

---
## 6. Execution Checklist (Android 11)
1. **Start headless emulator** – run `./start_headless.sh` (script in project root) or the commands in `headless_emulator_rules.md`.
2. **Confirm device** – `adb devices` → `emulator-5554`.
3. **Run Maestro suite** (example):
   ```bash
   maestro test \
     --device emulator-5554 \
     --format html \
     --output test_report.html \
     $(git ls-files "flows/**/*.yaml" | tr '\n' ' ')
   ```
   - This runs **all** flows sequentially. Adjust the list if you want a subset.
4. **Review report** – open `test_report.html` in a browser; screenshots are embedded.
5. **Cleanup** – after the run, stop the emulator: `adb -s emulator-5554 emu kill`.

---
## 7. Maintenance & Extensions
- **Add new flows**: place the YAML under the appropriate feature directory and update **Section 4** of this document with a new test case entry.
- **Zero‑sleep compliance**: replace any `runScript: ../../pages/delay.js` with explicit `assertVisible` or conditional waits. Use `optional: true` for transient dialogs.
- **Headless considerations**: screenshots still work via ADB; however, verify that any UI‑only animations are not required for assertions.
- **CI Integration**: the above `maestro test` command can be wrapped in a GitHub Action or Cloud Build step; just ensure the Android SDK and emulator are installed in the runner image.

---
## 8. References
- **Flow files** – located under `flows/` directory.
- **Headless execution guide** – `headless_emulator_rules.md`.
- **Automation standards** – `.agents/rules/maestro-standards.md`.
- **Locator memory** – `.agents/memory/*` for UI element identifiers.

*Prepared by Antigravity (AGY) – 2026‑11‑11*