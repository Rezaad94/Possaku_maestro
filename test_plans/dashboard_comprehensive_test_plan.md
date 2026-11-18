# Possaku Dashboard – Comprehensive Test Plan & Test Cases Specification

**Document Version:** 1.0  
**Target Application:** Possaku Android POS & Business Management (`com.cloudiex.possaku`)  
**Target Environment:** Android 11 (`android_11`)  
**Automation Engine:** Maestro Mobile UI Automation  
**Date:** 2026-11-11  

---

## 1. Executive Summary & Objective

The **Dashboard (`Home`)** screen is the central operational hub of the Possaku application. It surfaces real-time sales performance, store operating state, operational shortcuts (Kasir, Products, Customers, Finance, Orders, Settings), and direct navigation to all core modules.

The objective of this test plan is to establish **100% functional test coverage** across all menus, controls, metrics, and navigation paths accessible from the Dashboard, ensuring robustness under standard, negative, and edge-case operational conditions.

---

## 2. Dashboard Architecture & Menu Decomposition

Based on live UI inspection and view hierarchy extraction on Android 11, the Dashboard comprises 5 core structural areas and 12 distinct functional modules:

```
+-------------------------------------------------------------------------------+
| [Greeting: "Selamat datang di"]  [Store: new ref wija]  [Notif Bell: (Badge)] |
| [Sync Timestamp: "Update X menit lalu"]                                       |
+-------------------------------------------------------------------------------+
| OVERVIEW & METRICS                                                            |
|  - Date Period Filter: [Hari ini | Minggu ini | Bulan ini]                    |
|  - Total Penjualan (Rp) | Total Transaksi (Count) | Total Produk Terjual      |
+-------------------------------------------------------------------------------+
| STORE STATUS & OPERATIONAL SLIDER                                             |
|  - Status Badge: [Buka / Tutup]                                               |
|  - Interactive Slider: [Jam operasional akan tutup/buka ... geser >>>]        |
+-------------------------------------------------------------------------------+
| OPERASIONAL (Main Grid Menus)                                                 |
|  [Kasir]           [Atur Produk]         [Daftar Pelanggan]                   |
|  [Keuangan]        [Daftar Pesanan (N)]  [Lain-Lain]                          |
|                                           |-> Cetak Struk                     |
|                                           |-> Toko Onlineku                   |
|                                           |-> Daftar Karyawan                 |
|                                           |-> Multi Usaha                     |
|                                           |-> Manajemen Aset                  |
+-------------------------------------------------------------------------------+
| BOTTOM NAVIGATION (Persistent Tabs)                                           |
|  [Tab 1: Home]   [Tab 2: Riwayat]   [Tab 3: Usahaku]   [Tab 4: Profil]        |
+-------------------------------------------------------------------------------+
```

---

## 3. Comprehensive Test Matrix

| Module ID | Module Name | Primary Functions | Priority |
| :--- | :--- | :--- | :--- |
| **DASH-HDR** | Header & Notifications | Greeting, Store Name, Notification Bell, Sync status | P1 |
| **DASH-OVR** | Overview & Metrics | Total Penjualan, Total Transaksi, Total Produk Terjual | P0 |
| **DASH-FLT** | Period Date Filter | Hari Ini, Minggu Ini, Bulan Ini dropdown selection | P1 |
| **DASH-STR** | Store Status & Slider | Swipe to Open/Close, Operational schedule notice, Kasir guard | P0 |
| **DASH-KAS** | Menu: Kasir | POS terminal launch, Closed-store restriction block | P0 |
| **DASH-PRD** | Menu: Atur Produk | Catalog view, Category tabs, Product list, Coachmark handling | P1 |
| **DASH-CUS** | Menu: Daftar Pelanggan | Customer list, Search customer, Empty state CTA | P2 |
| **DASH-FIN** | Menu: Keuangan | Saku Utama, Saku Lainnya, Add pocket CTA | P2 |
| **DASH-ORD** | Menu: Daftar Pesanan | Order queue badge, Status filter tabs, Bill & Complete order | P1 |
| **DASH-MSC** | Menu: Lain-Lain | Receipt printer, Online store, Staff, Multi-outlet, Assets | P1 |
| **DASH-NAV** | Bottom Navigation | Tab switching (Home, Riwayat, Usahaku, Profil) | P0 |

---

## 4. Detailed Test Cases

### 4.1 Header & Notifications (`DASH-HDR`)

#### TC-DASH-HDR-001: Header Store Greeting & Name Verification
* **Tags:** `regression-p1`, `dashboard`, `header`
* **Pre-condition:** User is successfully logged in.
* **Test Steps:**
  1. Launch app and observe top header.
  2. Verify greeting text contains `Selamat datang di`.
  3. Verify store name label matches logged-in merchant (e.g. `new ref wija`).
  4. Verify data sync text contains `Update .* yang lalu`.
* **Expected Result:** Header correctly displays personalized merchant greeting and recent sync time.

#### TC-DASH-HDR-002: Notification Center Navigation & Notification Counter
* **Tags:** `regression-p1`, `dashboard`, `notifications`
* **Pre-condition:** User is on Dashboard with unread notifications.
* **Test Steps:**
  1. Verify notification icon displays an unread count badge (e.g. `7`).
  2. Tap on the notification bell.
  3. Assert navigation to `Notifikasi` screen.
  4. Verify presence of `Baca Semua`, filter tabs (`Semua`, `Belum Dibaca`, `Sudah Dibaca`), and activity logs.
  5. Tap `Home` tab or `Kembali` button.
* **Expected Result:** Notification screen opens, displays date-grouped logs, and returns smoothly to Dashboard.

---

### 4.2 Overview & Metrics (`DASH-OVR`)

#### TC-DASH-OVR-001: Overview Metrics Cards Display
* **Tags:** `regression-p0`, `smoke`, `dashboard`, `metrics`
* **Pre-condition:** User is on Dashboard.
* **Test Steps:**
  1. Assert `Overview` section title is visible.
  2. Assert `Total Penjualan` card is visible and formatted in Rupiah currency (`Rp.*`).
  3. Assert `Total Transaksi` card is visible with numerical count (`\d+`).
  4. Assert `Total Produk Terjual` card is visible with numerical count (`\d+`).
* **Expected Result:** All three operational KPIs display correctly with appropriate numerical formatting.

---

### 4.3 Period Date Filter (`DASH-FLT`)

#### TC-DASH-FLT-001: Open Period Filter Modal
* **Tags:** `regression-p1`, `dashboard`, `filters`
* **Pre-condition:** User is on Dashboard.
* **Test Steps:**
  1. Tap on the period filter dropdown button (`Hari ini`).
  2. Assert filter bottom sheet/modal appears.
  3. Assert `Filter Periode` header is displayed.
  4. Assert options `Hari ini`, `Minggu ini`, and `Bulan ini` are all visible.
* **Expected Result:** Period modal displays with all 3 reporting intervals available.

#### TC-DASH-FLT-002: Period Selection & Metrics Refresh
* **Tags:** `regression-p1`, `dashboard`, `filters`
* **Pre-condition:** Period modal is open.
* **Test Steps:**
  1. Select option `Minggu ini`.
  2. Verify modal dismisses.
  3. Verify period filter button label updates to reflect selected period.
  4. Repeat for `Bulan ini` and `Hari ini`.
* **Expected Result:** Filter selection updates active period and triggers KPI data reload.

---

### 4.4 Store Operating Status & Slider (`DASH-STR`)

#### TC-DASH-STR-001: Toggle Store from Open (`Buka`) to Closed (`Tutup`)
* **Tags:** `regression-p0`, `dashboard`, `store-control`
* **Pre-condition:** Store status is `Buka`.
* **Test Steps:**
  1. Assert status indicator displays `Buka`.
  2. Swipe the operating slider from left to right (`start: 20%,45%`, `end: 80%,45%`).
  3. Confirm store closing dialog by tapping `Ya`.
  4. Assert status indicator transitions to `Tutup`.
  5. Assert operating helper text updates to opening schedule (`Jam operasional akan buka pada ...`).
* **Expected Result:** Store transitions to Closed state and updates UI immediately.

#### TC-DASH-STR-002: Toggle Store from Closed (`Tutup`) to Open (`Buka`)
* **Tags:** `regression-p0`, `dashboard`, `store-control`
* **Pre-condition:** Store status is `Tutup`.
* **Test Steps:**
  1. Swipe the operating slider from left to right.
  2. Confirm store opening dialog by tapping `Ya`.
  3. Assert status indicator transitions to `Buka`.
  4. Assert operating helper text updates to closing schedule (`Jam operasional akan tutup pada ...`).
* **Expected Result:** Store transitions back to Open state.

#### TC-DASH-STR-003: Operational Restriction on Closed Store
* **Tags:** `regression-p0`, `dashboard`, `kasir-guard`
* **Pre-condition:** Store status is `Tutup`.
* **Test Steps:**
  1. Tap on `Kasir` from the Operasional menu.
  2. Assert warning dialog appears (`Konfirmasi`, `Buka usaha dulu untuk menggunakan fitur ini`).
  3. Tap `Batal` / `Tidak`.
  4. Verify POS terminal does not open, and user remains on Dashboard.
* **Expected Result:** App prevents POS operations when the store is marked as closed.

---

### 4.5 Menu 1: Kasir POS (`DASH-KAS`)

#### TC-DASH-KAS-001: Launch POS Terminal from Dashboard
* **Tags:** `regression-p0`, `smoke`, `dashboard`, `kasir`
* **Pre-condition:** Store status is `Buka`.
* **Test Steps:**
  1. Tap on `Kasir` icon in Operasional grid.
  2. Assert POS screen opens.
  3. Assert category tabs (`Semua`, `Sembako`, etc.) and `Scan Barcode` icon are visible.
  4. Tap Android Back or `Kembali`.
* **Expected Result:** POS terminal loads successfully and returns cleanly to Dashboard.

---

### 4.6 Menu 2: Atur Produk (`DASH-PRD`)

#### TC-DASH-PRD-001: Product Catalog Management Navigation & Category Filtering
* **Tags:** `regression-p1`, `dashboard`, `atur-produk`
* **Pre-condition:** User is on Dashboard.
* **Test Steps:**
  1. Tap on `Atur Produk` in Operasional grid.
  2. Dismiss onboarding coachmark if displayed (`Lewati` or `Selesai`).
  3. Assert title `Atur Produk` is visible.
  4. Assert category tabs exist (e.g. `Semua (2)`, `Sembako (2)`).
  5. Assert product item cards are visible with Name, Price, Variant count, and Status (`Aktif`).
  6. Switch between categories and verify filtered list updates.
  7. Tap `Kembali`.
* **Expected Result:** Catalog management loads with correct stock and pricing information.

---

### 4.7 Menu 3: Daftar Pelanggan (`DASH-CUS`)

#### TC-DASH-CUS-001: Customer Directory Screen & Search
* **Tags:** `regression-p2`, `dashboard`, `pelanggan`
* **Pre-condition:** User is on Dashboard.
* **Test Steps:**
  1. Tap on `Daftar Pelanggan` in Operasional grid.
  2. Dismiss onboarding coachmark if present (`Lewati`).
  3. Assert title `Daftar Pelanggan` is visible.
  4. Assert search field `Cari pelanggan` is present.
  5. If list is empty, verify empty state (`Kamu Belum Punya Daftar Pelanggan`) and CTA `Tambahkan Pelanggan`.
  6. Tap `Kembali`.
* **Expected Result:** Customer directory screen displays with search and creation capabilities.

---

### 4.8 Menu 4: Keuangan / Financial Pockets (`DASH-FIN`)

#### TC-DASH-FIN-001: Financial Management & Pocket Categorization
* **Tags:** `regression-p2`, `dashboard`, `keuangan`
* **Pre-condition:** User is on Dashboard.
* **Test Steps:**
  1. Tap on `Keuangan` in Operasional grid.
  2. Assert title `Keuangan` is visible.
  3. Assert `Saku Utama` card is present with subtitle `Pegang Kendali Usahamu`.
  4. Assert `Saku Lainnya` section exists with empty state/list and CTA `+ Tambahkan Saku`.
  5. Tap `Kembali`.
* **Expected Result:** Financial pocket interface is displayed with primary and auxiliary wallets.

---

### 4.9 Menu 5: Daftar Pesanan / Orders (`DASH-ORD`)

#### TC-DASH-ORD-001: Order Queue Screen & Badge Synchronization
* **Tags:** `regression-p1`, `dashboard`, `pesanan`
* **Pre-condition:** Dashboard displays active order badge (e.g. `2`).
* **Test Steps:**
  1. Verify `Daftar Pesanan` icon displays badge matching pending orders.
  2. Tap on `Daftar Pesanan`.
  3. Assert filter tabs: `Semua`, `Terbayar`, and `Belum Terbayar`.
  4. Assert order cards display Queue Number, Payment Status, Notes (`Catatan`), and Total Price.
  5. Assert action buttons `Tagih` and `Selesai` exist for unpaid/in-progress orders.
  6. Assert `Reset Nomor Antrian` footer button is visible.
  7. Tap `Kembali` or `Home`.
* **Expected Result:** Order queue accurately displays active merchant tickets with action controls.

---

### 4.10 Menu 6: Lain-Lain / Advanced Modules (`DASH-MSC`)

#### TC-DASH-MSC-001: Open and Inspect "Lain-Lain" Operational Modal
* **Tags:** `regression-p1`, `dashboard`, `lain-lain`
* **Pre-condition:** User is on Dashboard.
* **Test Steps:**
  1. Tap on `Lain-Lain` in Operasional grid.
  2. Assert bottom modal opens with header `Lain-Lain`.
  3. Verify all 5 advanced operational options are visible:
     - `Cetak Struk` (Receipt & Bluetooth Printer)
     - `Toko Onlineku` (Online Storefront settings)
     - `Daftar Karyawan` (Employee management)
     - `Multi Usaha` (Multi-outlet switching)
     - `Manajemen Aset` (Asset inventory)
  4. Tap `Tutup`.
  5. Assert modal closes and returns focus to Dashboard.
* **Expected Result:** Bottom sheet presents all secondary business tools and closes without error.

#### TC-DASH-MSC-002: Navigation to Toko Onlineku from Lain-Lain
* **Tags:** `regression-p2`, `dashboard`, `lain-lain`, `online-store`
* **Pre-condition:** User opened `Lain-Lain` modal.
* **Test Steps:**
  1. Tap on `Toko Onlineku`.
  2. Assert navigation to Online Store configuration screen.
  3. Verify toggle switches and domain/link settings are visible.
  4. Tap `Kembali`.
* **Expected Result:** Navigates directly to online store settings and back.

---

### 4.11 Bottom Navigation Bar (`DASH-NAV`)

#### TC-DASH-NAV-001: Seamless Navigation Across All 4 Main Tabs
* **Tags:** `regression-p0`, `smoke`, `navigation`
* **Pre-condition:** User is on Dashboard (`Home`).
* **Test Steps:**
  1. Tap `Riwayat\nTab 2 dari 4`. Assert transaction history screen opens.
  2. Tap `Usahaku\nTab 3 dari 4`. Assert business details, QR code, and tax settings open.
  3. Tap `Profil\nTab 4 dari 4`. Assert merchant profile, account settings, and logout open.
  4. Tap `Home\nTab 1 dari 4`. Assert return to Dashboard screen with `Overview` and `Operasional`.
* **Expected Result:** Tab switches instantly without session reset or visual glitches.

---

## 5. Execution Strategy & Traceability Matrix

| Feature | Automated Flow File | Status | Runtime Estimate |
| :--- | :--- | :--- | :--- |
| Overview & Metrics | `flows/dashboard/overview_flow.yaml` | ✅ Automated & Passing | ~55s |
| Period Date Filter | `flows/dashboard/filter_flow.yaml` | ⚠️ Needs locator regex update | ~1m 15s |
| Store Status Toggle | `flows/dashboard/open_close_store_flow.yaml` | ✅ Automated | ~1m 30s |
| Kasir POS Launch | `flows/kasir/catalog_qty_flow.yaml` | ✅ Automated | ~1m 10s |
| Lain-Lain Settings | `flows/lain_lain/online_store_setting_flow.yaml` | ✅ Automated | ~45s |
| Atur Produk | *New candidate flow* (`flows/dashboard/atur_produk_flow.yaml`) | 📝 Planned | ~40s |
| Daftar Pesanan | *New candidate flow* (`flows/dashboard/daftar_pesanan_flow.yaml`) | 📝 Planned | ~45s |
| Keuangan | *New candidate flow* (`flows/dashboard/keuangan_flow.yaml`) | 📝 Planned | ~35s |
| Daftar Pelanggan | *New candidate flow* (`flows/dashboard/daftar_pelanggan_flow.yaml`) | 📝 Planned | ~35s |

---

## 6. Zero-Sleep Policy & Verification Rules

In compliance with project QA rules (`.agents/rules/maestro-standards.md`):
1. **No Hard Sleeps:** Never use `pages/delay.js` (busy-wait loops). Replace all with explicit `assertVisible` or `when: visible`.
2. **Coachmark Handling:** All secondary screens (`Atur Produk`, `Daftar Pelanggan`) contain first-time coachmark overlays. Flows must handle them using:
   ```yaml
   - tapOn:
       text: "Lewati"
       optional: true
   - tapOn:
       text: "Selesai"
       optional: true
   ```
3. **Accessibility Locators:** Use exact `content-desc` or regex patterns (e.g. `Home\nTab 1.*`, `Kasir\n.*`, `Daftar\nPesanan\n.*`).
