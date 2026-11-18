# UI Locators: Dashboard & Metrics

- **Domain**: Store Dashboard & Operational Summary
- **Page Object File**: `pages/dashboard/dashboard_page.js`
- **Global Object**: `output.dashboard_page`

---

## 1. Metrics & Cards
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `overviewLabel` | `"Overview"` | Text | Screen header indicator |
| `totalPenjualanLabel` | `"Total Penjualan"` | Text | Gross revenue card |
| `totalTransaksiLabel` | `"Total Transaksi\n.*"` | Regex | Order counter card |
| `totalProdukTerjualLabel` | `"Total Produk Terjual\n.*"` | Regex | Item volume card |

---

## 2. Date Filtering
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `dateFilterButton` | `"Hari ini"` | Text | Active period button |
| `filterHeaderLabel` | `"Filter Periode"` | Text | Filter bottom sheet header |
| `filterOptionHariIni` | `"Hari ini"` | Text | Today filter option |
| `filterOptionMingguIni` | `"Minggu ini"` | Text | Current week filter option |
| `filterOptionBulanIni` | `"Bulan ini"` | Text | Current month filter option |

---

## 3. Store Status Indicators
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `storeStatusLabelBuka` | `"Buka"` | Text | Store is actively open |
| `storeStatusLabelTutup` | `"Tutup"` | Text | Store is closed |
| `bukaUsahaWarningText` | `"(?s)Buka usaha dulu untuk menggunakan fitur ini.*"` | Regex | Warning banner when cashier tries to sell while closed |
| `jamOperasionalBukaInfo` | `"Jam operasional akan buka pada .* atau geser untuk membuka >>>"` | Regex | Swipe guide when closed |
| `jamOperasionalTutupInfo`| `"Jam operasional akan tutup pada .* atau geser untuk menutup >>>"` | Regex | Swipe guide when open |

---

## 4. Operasional Grid Menus
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `kasirMenuButton` | `"Kasir\n.*"` | Regex | POS Cashier terminal launch |
| `aturProdukMenuButton` | `"Atur\nProduk.*"` | Regex | Product catalog management |
| `daftarPelangganMenuButton` | `"Daftar\nPelanggan.*"` | Regex | Customer directory |
| `keuanganMenuButton` | `"Keuangan"` | Text | Financial management & pockets |
| `daftarPesananMenuButton` | `"Daftar\nPesanan.*"` | Regex | Order queue & kitchen tickets |
| `lainLainMenuButton` | `"Lain-Lain"` | Text | More options bottom sheet modal |

---

## 5. Bottom Navigation Tabs
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `homeTab` | `"Home\nTab 1.*"` | Regex | Active Home Dashboard view |
| `riwayatTab` | `"Riwayat\nTab 2.*"` | Regex | Transaction history tab |
| `usahakuTab` | `"Usahaku\nTab 3.*"` | Regex | Business profile and settings tab |
| `profilTab` | `"Profil\nTab 4.*"` | Regex | Merchant profile and account tab |
