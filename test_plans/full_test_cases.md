# Possaku Android 11 – Full Test Case Suite

## Overview
The suite covers **all user‑visible features** in the Possaku app, exercising both happy‑path and edge‑case scenarios. Each test case is expressed as a Maestro **flow YAML** that can be run on the Android 11 emulator (headless or UI). The flows are grouped by functional area and reference the shared memory objects (`.agents/memory/*`) for reliable locators.

---
## 1. Authentication
| TC ID | Description | Flow File | Notes |
|------|-------------|-----------|-------|
| **Auth‑01** | Valid login with phone `validPhoneNumber1` (local format) | `flows/login/valid_login_flow.yaml` | Already exists and passes. |
| **Auth‑02** | Valid login with phone `validPhoneNumber2` (E.164) | `flows/login/valid_login_flow.yaml` (reuse) | Uses same flow – different env variable. |
| **Auth‑03** | Empty PIN → error *“Isikan nomor pin anda*” | `flows/login/invalid_login_flow.yaml` (step 1) | Verify error toast/message. |
| **Auth‑04** | Empty phone number → error *“Isikan nomor telepon anda*” | `flows/login/invalid_login_flow.yaml` (step 2) |
| **Auth‑05** | Invalid phone & PIN → error *“Nomor Telepon … tidak terdaftar*” | `flows/login/invalid_login_flow.yaml` (step 3) |
| **Auth‑06** | Empty phone + PIN → both messages | `flows/login/invalid_login_flow.yaml` (step 4) |
| **Auth‑07** | Inactive user → *“Status User Tidak Aktif!*” | `flows/login/invalid_login_flow.yaml` (step 5) |
| **Auth‑08** | Logout flow (after successful login) | `flows/login/logout_flow.yaml` *(new)* | Tap profile → Logout, assert login screen appears. |

---
## 2. Dashboard
### 2.1 Overview
| TC ID | Description | Flow File |
|------|-------------|-----------|
| **Dash‑OV‑01** | Verify all overview metric labels are visible after login | `flows/dashboard/overview_flow.yaml` |
| **Dash‑OV‑02** | Verify numeric values are non‑empty and formatted (e.g., contains digits) | Extend `overview_flow.yaml` with `assertMatch` on `${output.dashboard_page.totalPenjualanLabel}` value. |

### 2.2 Filters
| TC ID | Description | Flow File |
|------|-------------|-----------|
| **Dash‑FL‑01** | Open filter, select **Hari ini**, verify list updates for today | `flows/dashboard/filter_flow_hari_ini.yaml` *(new)* |
| **Dash‑FL‑02** | Select **Minggu ini**, verify list contains only this week’s data | `flows/dashboard/filter_flow_minggu.ini.yaml` *(new)* |
| **Dash‑FL‑03** | Select **Bulan ini**, verify list contains this month’s data | `flows/dashboard/filter_flow_bulan.ini.yaml` *(new)* |
| **Dash‑FL‑04** | Dismiss filter without selection, ensure UI returns to previous state | Re‑use `filter_flow.yaml` with a `tapOn` on background. |

### 2.3 Store Control (Open/Close)
| TC ID | Description | Flow File |
|------|-------------|-----------|
| **Dash‑SC‑01** | Open store from closed state, assert label changes to **Buka** | `flows/dashboard/open_close_store_flow.yaml` (step open) |
| **Dash‑SC‑02** | Close store from open state, assert label changes to **Tutup** | Same flow (step close). |
| **Dash‑SC‑03** | Attempt to open store when already open – no change, toast *already open* | New flow `flows/dashboard/open_close_store_noop.yaml`. |

---
## 3. Kasir (POS)
| TC ID | Description | Flow File |
|------|-------------|-----------|
| **Kasir‑01** | Add a product to cart, increase quantity, verify total updates | `flows/kasir/cart_qty_flow.yaml` |
| **Kasir‑02** | Decrease quantity to zero, verify item removal | Extend `cart_qty_flow.yaml` with a loop of `tapOn` minus. |
| **Kasir‑03** | Browse catalog, select product, add to cart, verify catalog quantity decrements | `flows/kasir/catalog_qty_flow.yaml` |
| **Kasir‑04** | Search for a non‑existent product, assert *“Tidak ada hasil”* message | New flow `flows/kasir/search_not_found.yaml`. |
| **Kasir‑05** | Apply a discount code (if UI provides), verify price reduction | New flow `flows/kasir/discount_flow.yaml`. |

---
## 4. Usahaku (Business Management)
| TC ID | Description | Flow File |
|------|-------------|-----------|
| **Usah‑01** | Open store (same as dashboard) – verify store status label **Buka** | `flows/usahaku/open_close_store_flow.yaml` |
| **Usah‑02** | Close store – verify label **Tutup** | Same flow (close step). |
| **Usah‑03** | Attempt to open store when already open – expect toast *already open*. |

---
## 5. Lain‑Lain (Settings / Misc)
| TC ID | Description | Flow File |
|------|-------------|-----------|
| **LL‑01** | Open *Store Settings* screen, toggle a switch (e.g., “Enable notifications”), save, verify persisted state on re‑open. | `flows/lain_lain/online_store_setting_flow.yaml` |
| **LL‑02** | Try to save with a mandatory field empty → validation error *“Wajib diisi”* | Extend `online_store_setting_flow.yaml` with cleared field.
| **LL‑03** | Change store name, verify it updates on Dashboard header. |

---
## 6. General UI Navigation & Stability
| TC ID | Description | Flow File |
|------|-------------|-----------|
| **Gen‑01** | Launch app, wait for home screen, take a screenshot (baseline) | `flows/tmp/quick_inspect.yaml` (already exists). |
| **Gen‑02** | Rotate device (portrait ↔ landscape) and ensure UI elements remain visible. | New flow `flows/tmp/rotate_device.yaml`. |
| **Gen‑03** | Background the app (press home) and resume, verify session persists. |
| **Gen‑04** | Simulate low‑memory kill (adb shell pm clear) and relaunch – ensure login required. |

---
## 7. Test Data & Parameterization
All flows use **environment variables** defined in `config/env.yaml` and `pages/login/login_credential.js`. Example usage:
```yaml
env:
  phoneNumber: "${output.login_credential.dev.validPhoneNumber1}"
  PIN: "${output.login_credential.dev.validPIN}"
```
For data‑driven tests (e.g., different products, discount codes), add a `data` block at the top of the flow and reference `${data.<key>}` inside steps.

---
## 8. Running the Full Suite
1. **Start the emulator** (headless preferred):
   ```bash
   ./start_headless.sh   # from project root
   ```
2. **Execute all flows** (parallel execution is possible via Maestro Cloud, but on local you can run sequentially):
   ```bash
   maestro test \
     --device emulator-5554 \
     --format html \
     --output full_report.html \
     $(git ls-files "flows/**/*.yaml" | tr '\n' ' ') 
   ```
3. **Collect reports** – the generated `full_report.html` aggregates each flow’s step log and screenshots.

---
## 9. Creating New Flows (quick guide)
1. **Record** (optional):
   ```bash
   maestro record --device emulator-5554 --output flows/tmp/recorded.yaml
   ```
   Perform the actions manually; Maestro will generate a flow skeleton.
2. **Refactor** – replace any `runScript: ../../pages/delay.js` with appropriate `delay: <ms>` or `assertVisible`.
3. **Parameterise** – add an `env:` block at the top for credentials, product IDs, etc.
4. **Validate** – run `maestro check-syntax <flow.yaml>` before execution.

---
## 10. Next Steps for You
- **Create missing flow files** listed above (you can copy an existing flow as a template).  I can generate empty skeletons for any you specify.
- **Update the UI text expectations** for the filter flow (the failure was *“Bulan ini”* not visible).  Use the UI dump (`ui_dump.xml`) to verify the exact string.
- **Run the new flows** individually to confirm they pass, then invoke `run_suite.sh` again.
- **Optionally enable Maestro Cloud** for parallel execution (see the banner in the suite output).

---
### TL;DR
We now have a **full test‑case matrix** covering login, dashboard, kasir, usahaku, and settings. Each case maps to a Maestro YAML flow that you can create (or I can scaffold). After the flows exist, run the suite to produce a consolidated HTML report.

*Prepared by Antigravity (AGY) – 2026‑11‑11*