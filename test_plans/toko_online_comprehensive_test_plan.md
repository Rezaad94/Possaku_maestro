# Comprehensive Test Plan: (Lain - lain) Toko Online

## 1. Feature Overview
The **Toko Online** (Online Store) feature in Possaku enables merchants to publish an e-commerce catalog accessible via web link and QR Code. Merchants can manage customer access links, share storefront links via Android system sharesheet, configure store operating hours, select active days of operation, update WhatsApp contact information for order communications, and preview or export a printable QR Code poster.

---

## 2. Test Architecture & Standards
- **Automation Framework**: Maestro CLI with `run_detailed_test.sh` reporting.
- **Target Device**: Android 11 (`emulator-5554`), App ID: `com.cloudiex.possaku`.
- **Page Object**: `pages/lain_lain/toko_online_page.js`.
- **Test ID Convention**: `[TOKO-XX]`.
- **Assertion Strategy**: Explicit verification of visual state, toast messages, Android Chooser intent resolution, and form field roundtrips.

---

## 3. Test Cases Specification

| Test ID | Test Case Name | Preconditions | Test Steps | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[TOKO-01]` | Navigasi & Onboarding Toko Online | User logged in on Dashboard | 1. Tap Lain-Lain.<br>2. Tap Toko Onlineku.<br>3. Dismiss onboarding guide if displayed. | Toko Online screen opens with store name, URL link, settings summary, and QR Code button. | P0 |
| `[TOKO-02]` | Copy store link | On Toko Online screen | 1. Tap Copy Store Link button. | Toast/Snackbar "Link telah disalin" appears and store URL is placed on clipboard. | P0 |
| `[TOKO-03]` | Share store link | On Toko Online screen | 1. Tap Share Store Link button. | Native Android Share Sheet (ChooserActivity) opens containing store invitation and URL. Press Back to return. | P0 |
| `[TOKO-04]` | View QR code | On Toko Online screen | 1. Tap "QR Code Tokomu" button.<br>2. Verify QR Code preview screen elements.<br>3. Tap Kembali to return. | QR Code screen opens displaying title, store name, visual QR image, and "Print to PDF" button. | P1 |
| `[TOKO-05]` | Change Phone number (Nomor WA) | On Toko Online screen | 1. Tap Update button.<br>2. Clear phone input and enter valid WhatsApp number.<br>3. Tap Simpan. | Settings saved successfully, returns to main screen, and updated phone number is displayed. | P0 |
| `[TOKO-06]` | Change Time open store (Jam Buka) | On Toko Online screen | 1. Tap Update button.<br>2. Tap Jam Buka Toko field.<br>3. Verify time picker bottom sheet.<br>4. Tap Simpan on picker.<br>5. Tap Simpan on form. | Operating hours updated and verified on main screen. | P1 |
| `[TOKO-07]` | Change day open store (Hari Buka) | On Toko Online screen | 1. Tap Update button.<br>2. Toggle days of the week (e.g. Senin).<br>3. Tap Simpan. | Operating days updated and persisted without validation errors. | P1 |

---

## 4. Execution Plan
1. `flows/lain_lain/toko_online_link_qr_flow.yaml`: Covers `[TOKO-01]`, `[TOKO-02]`, `[TOKO-03]`, and `[TOKO-04]`.
2. `flows/lain_lain/toko_online_settings_flow.yaml`: Covers `[TOKO-05]`, `[TOKO-06]`, and `[TOKO-07]`.
