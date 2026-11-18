# Comprehensive Test Plan: Menu Lain-Lain -> Cetak Struk (`flows/lain_lain/`)

## 1. Overview & Scope
This test plan provides complete automated test coverage for the **Cetak Struk** (Receipt & Slip Printing) feature located under **Menu Lain-Lain** in Possaku. It includes all 16 user-requested scenarios plus smoke, empty-state validation, and item deletion edge cases:

- **Add Product form catalog** (`Katalog Produk`)
- **Add custom product** (`Produk Kostum`)
- **Increase quantity product added** (Plus button & Qty input)
- **Decrease quantity product added** (Minus button)
- **Add transaction discount nominal** (Receipt Total Diskon nominal rollup)
- **Add transaction discount percent** (Receipt Total Diskon percent rollup)
- **Add item discount nominal** (`Edit Produk Keranjang` -> Nominal)
- **Add item discount percent** (`Edit Produk Keranjang` -> Persen)
- **Edit added product** (Item note & modifications)
- **Edit added discount** (Switch between Nominal/Percent or adjust value)
- **Preview struck** (`Preview` button & Receipt layout inspection)
- **Add created date** (`Pilih Tanggal Struk` -> `Atur Tanggal` calendar)
- **Add customer** (`Nama Pelanggan` -> `Pilih Pelanggan` selector)
- **Add payment method** (`Metode Pembayaran` -> Tunai, QRIS, Hutang, Debit)
- **Print struck** (`Cetak Struk` -> `Transaksi Sukses` / Printer dispatch)
- **New Transaction** (`Transaksi Baru` reset lifecycle)

---

## 2. Directory Architecture & File Structure

```
Possaku_maestro/
├── pages/
│   └── lain_lain/
│       ├── lain_lain_page.js             # Lain-Lain menu root selectors
│       └── cetak_struk_page.js           # Cetak Struk selectors & verified touchpoints
├── flows/
│   └── lain_lain/
│       ├── cetak_struk_smoke_flow.yaml   # [STRUK-01] Navigation & empty state verification
│       ├── cetak_struk_product_flow.yaml # [STRUK-02]-[STRUK-04], [STRUK-09]-[STRUK-10] Catalog & custom products, qty adjustment, delete
│       ├── cetak_struk_discount_flow.yaml# [STRUK-05]-[STRUK-08], [STRUK-11]-[STRUK-12] Item discounts (Nominal/Percent), edit discount & note
│       └── cetak_struk_preview_flow.yaml # [STRUK-13]-[STRUK-18] Preview layout, date, customer, payment method, print dispatch & new transaction
└── test_plans/
    └── cetak_struk_comprehensive_test_plan.md # Workspace copy of test plan
```

---

## 3. Test Case Coverage Matrix (100% User List Mapped)

All test cases adhere to the naming convention `# [STRUK-XX]`:

| # | User Request Feature | Test Case ID | Target Flow | Priority | Description & Validation Criteria |
| :---: | :--- | :---: | :--- | :---: | :--- |
| 1 | **Navigation & Empty State** | `[STRUK-01]` | `cetak_struk_smoke_flow.yaml` | P0 | Navigates from Dashboard to `Lain-Lain` -> `Cetak Struk`; asserts header title `Cetak Struk`, empty state message `Belum ada Produk di Struk anda`, `Total Rp0`, action buttons, and back navigation. |
| 2 | **Add Product form catalog** | `[STRUK-02]` | `cetak_struk_product_flow.yaml` | P0 | Taps `Katalog Produk` (`point: "285, 1513"`), selects product (e.g. `beras oye`), adjusts variant qty, taps `Tambahkan`, taps `Tambahkan ke Struk`; asserts product added with price and total updated. |
| 3 | **Increase quantity product added** | `[STRUK-03]` | `cetak_struk_product_flow.yaml` | P0 | On the added product card, taps Plus button (`point: "953, 354"`); asserts quantity increments (1 -> 2) and total amount updates accordingly. |
| 4 | **Decrease quantity product added** | `[STRUK-04]` | `cetak_struk_product_flow.yaml` | P0 | On the added product card, taps Minus button (`point: "744, 354"`); asserts quantity decrements (2 -> 1) and total recalculates. |
| 5 | **Add custom product** | `[STRUK-05]` | `cetak_struk_product_flow.yaml` | P0 | Taps `Produk Kostum` (`point: "795, 1513"`), inputs `Nama Produk` ("Kopi Hitam"), `Jumlah` ("2"), `Harga` ("15000"), taps `Tambah`; asserts custom product card appears with calculated total. |
| 6 | **Delete added product** *(Edge Case)* | `[STRUK-06]` | `cetak_struk_product_flow.yaml` | P1 | Swipes added item card left (`start: "900, 354", end: "200, 354"`), taps red Trash button (`point: "954, 354"`); asserts product removed from receipt cart. |
| 7 | **Add item discount nominal** | `[STRUK-07]` | `cetak_struk_discount_flow.yaml` | P0 | Swipes item card left, taps pencil Edit button (`point: "808, 354"`), selects chip `Nominal`, inputs discount amount (e.g. "5000"), taps `Terapkan`; asserts item displays discounted price. |
| 8 | **Add item discount percent** | `[STRUK-08]` | `cetak_struk_discount_flow.yaml` | P0 | Swipes item card left, taps pencil Edit button, selects chip `Persen`, inputs percentage (e.g. "10"), taps `Terapkan`; asserts percentage discount applied correctly. |
| 9 | **Edit added product** | `[STRUK-09]` | `cetak_struk_discount_flow.yaml` | P0 | In `Edit Produk Keranjang`, updates `Catatan Produk` ("Less Sugar"), taps `Terapkan`; asserts product card displays updated note `Catatan: Less Sugar`. |
| 10 | **Edit added discount** | `[STRUK-10]` | `cetak_struk_discount_flow.yaml` | P0 | Re-opens `Edit Produk Keranjang`, modifies discount value or switches discount type, taps `Terapkan`; asserts recalculated discount reflected. |
| 11 | **Add transaction discount nominal** | `[STRUK-11]` | `cetak_struk_discount_flow.yaml` | P1 | Verifies multi-item/item nominal discounts roll up into the overall transaction `Total Diskon` on the receipt preview. |
| 12 | **Add transaction discount percent** | `[STRUK-12]` | `cetak_struk_discount_flow.yaml` | P1 | Verifies proportional percentage discounts aggregate accurately into the overall receipt total and transaction summary. |
| 13 | **Preview struck** | `[STRUK-13]` | `cetak_struk_preview_flow.yaml` | P0 | Taps `Preview` button (`point: "540, 1667"`); asserts Preview Struk screen opens with store name, outlet, Pelanggan, Kasir, item list, Subtotal, Total Diskon, and Total. |
| 14 | **Add created date** | `[STRUK-14]` | `cetak_struk_preview_flow.yaml` | P0 | On Preview screen, taps `Pilih Tanggal Struk` (`point: "540, 299"`), selects date in `Atur Tanggal` calendar modal, taps `Terapkan`; asserts selected date & time reflected on receipt header. |
| 15 | **Add customer** | `[STRUK-15]` | `cetak_struk_preview_flow.yaml` | P0 | On Preview screen, taps `Nama Pelanggan` (`point: "540, 462"`), opens `Pilih Pelanggan` modal, taps `Pilih` (`point: "900, 1000"`); asserts customer name displayed in `Pelanggan` field. |
| 16 | **Add payment method** | `[STRUK-16]` | `cetak_struk_preview_flow.yaml` | P0 | On Preview screen, taps `Metode Pembayaran` (`point: "540, 625"`), selects radio button (e.g. `Tunai` at `point: "920, 1119"`); asserts selected method displayed in receipt metadata. |
| 17 | **Print struck** | `[STRUK-17]` | `cetak_struk_preview_flow.yaml` | P0 | On Preview screen, taps `Cetak Struk` button (`point: "540, 1491"`); verifies navigation to `Transaksi Sukses` with receipt details and `Pilih Printer` option. |
| 18 | **New Transaction** | `[STRUK-18]` | `cetak_struk_preview_flow.yaml` | P0 | On `Transaksi Sukses` (or Preview screen), taps `Transaksi Baru` (`point: "540, 1667"`); asserts transaction reset and returned to fresh cashier/builder state. |

---

## 4. Architectural Interaction Flow

```mermaid
flowchart TD
    Dashboard["Dashboard Operasional"] -->|"Lain-Lain tile (876,1490)"| LainModal["Lain-Lain Modal"]
    LainModal -->|"Cetak Struk (222,1206)"| CS["Cetak Struk Builder"]

    subgraph Product Management
        CS -->|"Katalog Produk (285,1513)"| Katalog["[STRUK-02] Katalog Produk Modal"]
        Katalog -->|"Select Item & Qty"| CS
        CS -->|"Produk Kostum (795,1513)"| CustomP["[STRUK-05] Tambah Produk Kostum"]
        CustomP -->|"Input Name, Qty, Price"| CS
        CS -->|"Plus button (953,354)"| IncQty["[STRUK-03] Increase Qty"]
        CS -->|"Minus button (744,354)"| DecQty["[STRUK-04] Decrease Qty"]
        CS -->|"Swipe Left -> Trash (954,354)"| DelItem["[STRUK-06] Delete Product"]
    end

    subgraph Discounts & Product Edit
        CS -->|"Swipe Left -> Pencil (808,354)"| EditModal["Edit Produk Keranjang"]
        EditModal -->|"Nominal Chip"| DiscNom["[STRUK-07] Item Discount Nominal"]
        EditModal -->|"Persen Chip"| DiscPct["[STRUK-08] Item Discount Percent"]
        EditModal -->|"Catatan Produk"| EditNote["[STRUK-09] Edit Added Product"]
        EditModal -->|"Modify Discount"| EditDisc["[STRUK-10] Edit Added Discount"]
    end

    subgraph Receipt Preview & Configuration
        CS -->|"Preview Button (540,1667)"| Preview["[STRUK-13] Preview Struk Screen"]
        Preview -->|"Pilih Tanggal Struk (540,299)"| DateModal["[STRUK-14] Atur Tanggal Modal"]
        Preview -->|"Nama Pelanggan (540,462)"| CustModal["[STRUK-15] Pilih Pelanggan Modal"]
        Preview -->|"Metode Pembayaran (540,625)"| PayModal["[STRUK-16] Metode Pembayaran Modal"]
        Preview -->|"Rollup Verification"| TxDisc["[STRUK-11]/[STRUK-12] Tx Discount Rollup"]
    end

    subgraph Print Dispatch & Reset
        Preview -->|"Cetak Struk Button (540,1491)"| TxSuccess["[STRUK-17] Transaksi Sukses & Print"]
        TxSuccess -->|"Transaksi Baru (540,1667)"| Reset["[STRUK-18] New Transaction Reset"]
    end
```

---

## 5. Verification Commands

Run test flows individually with detailed step-level reports:
```bash
# 1. Smoke, Navigation & Empty State
./run_detailed_test.sh flows/lain_lain/cetak_struk_smoke_flow.yaml reports/cetak_struk_smoke_report.html

# 2. Product Management (Catalog, Custom, Qty, Delete)
./run_detailed_test.sh flows/lain_lain/cetak_struk_product_flow.yaml reports/cetak_struk_product_report.html

# 3. Discounts & Product Editing
./run_detailed_test.sh flows/lain_lain/cetak_struk_discount_flow.yaml reports/cetak_struk_discount_report.html

# 4. Preview, Date, Customer, Payment & Print Dispatch
./run_detailed_test.sh flows/lain_lain/cetak_struk_preview_flow.yaml reports/cetak_struk_preview_report.html
```

---

## 6. Execution Results & Verification Metrics (100% Pass)

| Flow Name | Test Cases Covered | Duration | Result | Detailed HTML Report |
| :--- | :--- | :---: | :---: | :--- |
| `cetak_struk_smoke_flow.yaml` | `[STRUK-01]` (Navigation & Empty State) | **22s** | **PASSED (100%)** | [cetak_struk_smoke_report.html](file:///Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro/reports/cetak_struk_smoke_report.html) |
| `cetak_struk_product_flow.yaml` | `[STRUK-02]`, `[STRUK-03]`, `[STRUK-04]`, `[STRUK-05]`, `[STRUK-06]` | **55s** | **PASSED (100%)** | [cetak_struk_product_report.html](file:///Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro/reports/cetak_struk_product_report.html) |
| `cetak_struk_discount_flow.yaml` | `[STRUK-07]`, `[STRUK-08]`, `[STRUK-09]`, `[STRUK-10]`, `[STRUK-11]`, `[STRUK-12]` | **1m 14s** | **PASSED (100%)** | [cetak_struk_discount_report.html](file:///Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro/reports/cetak_struk_discount_report.html) |
| `cetak_struk_preview_flow.yaml` | `[STRUK-13]`, `[STRUK-14]`, `[STRUK-15]`, `[STRUK-16]`, `[STRUK-17]`, `[STRUK-18]` | **42s** | **PASSED (100%)** | [cetak_struk_preview_report.html](file:///Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro/reports/cetak_struk_preview_report.html) |
| **Total Suite** | **18 / 18 Test Cases** | **~3m 17s** | **100% Pass** | **4 Enriched HTML Reports** |
