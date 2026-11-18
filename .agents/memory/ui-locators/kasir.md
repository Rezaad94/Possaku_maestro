# UI Locators: Kasir / Catalog / Cart / Payment

- **Domain**: Point of Sale Catalog & Checkout
- **Page Object File**: `pages/kasir/kasir_page.js`
- **Global Objects**: `output.kasir_page`, `output.kasir_utils`

---

## 1. Navigation & Catalog Header
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `kasirMenuButton` | `"Kasir\n.*"` | Regex | Dashboard Operasional menu item |
| `searchIconPoint` | `"848,270"` | Point | Tap to open catalog search bar |
| `searchFieldPoint` | `"477,274"` | Point | EditText search field |
| `searchCloseButton` | `"Tutup"` | Text | Closes search bar |
| `searchFieldHint` | `"Cari produk"` | Text | Placeholder for catalog product search |
| `scanBarcodeButton` | `"Scan Barcode"` | Text | Opens `Pilih Mode` (`Scan Barcode` / `Buka Kamera`) |
| `customProductButton` | `"Produk Kostum"` | Text | Opens custom product modal sheet |
| `sortButtonPoint` | `"975,270"` | Point | Tap to open catalog sorting modal |

---

## 2. Products & Variants
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `productRegularText` | `"BO\nberas oye\n1 Varian"` | Text | Default regular test product |
| `variantReguler` | `"Reguler.*"` | Regex | Variant choice in modal sheet |
| `variantSheetAdd` | `"Tambahkan"` | Text | Adds selected variant to cart |
| `variantSheetClose` | `"Tutup"` | Text | Dismisses variant modal sheet |
| `variantSheetQtyMinusPoint` | `"785,1230"` | Point | Decrements sheet quantity |
| `variantSheetQtyPlusPoint` | `"996,1230"` | Point | Increments sheet quantity |
| `variantSheetQtyInputPoint` | `"891,1230"` | Point | Direct tap to edit quantity input |

---

## 3. Categories & Sorting
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `categorySemua` | `"Semua.*"` | Regex | All products category filter |
| `categorySembako` | `"Sembako.*"` | Regex | Groceries category filter |
| `sortAlphabetAsc` | `"Alfabet A-Z"` | Text | Alphabetical sort ascending |
| `sortAlphabetDesc` | `"Alfabet Z-A"` | Text | Alphabetical sort descending |
| `sortStockAsc` | `"Stok Terendah"` | Text | Stock quantity sort ascending |
| `sortStockDesc` | `"Stok Terbanyak"` | Text | Stock quantity sort descending |

---

## 4. Cart, Swipe Actions & Modals
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `cartButtonRegex` | `"Keranjang.*"` | Regex | Floating cart button showing count |
| `cartItemPlusPoint` | `"953,354"` | Point | Increases first item qty in Cart |
| `cartItemMinusPoint` | `"744,354"` | Point | Decreases first item qty in Cart |
| `cartItemQtyInputPoint` | `"849,354"` | Point | Direct qty EditText for first item in Cart (submit with `pressKey: "enter"`) |
| `cartItemSwipeStart` / `End` | `"83%,19%"` &rarr; `"18%,19%"` | Swipe | Reveals item Edit (pencil) & Delete (trash) buttons |
| `cartItemEditPencilPoint` | `"808,354"` | Point | Opens `Edit Produk Keranjang` sheet |
| `cartItemDeleteTrashPoint` | `"954,354"` | Point | Prompts `Hapus <item> dari keranjang?` (`Ya` / `Tidak`) |
| `cartTopTrashPoint` | `"980,137"` | Point | Clears all items in Cart (`Ya` / `Tidak`) |
| `cartTopCustomerPoint` | `"754,137"` | Point | Opens `Pilih Pelanggan` drawer (`Pilih` at `920,1650`; `+` add icon at `rightOf: "Pilih Pelanggan", above: "Cari pelanggan"`) |
| `cartBottomDiscountPoint` | `"169,1667"` | Point | Opens `Tambah Potongan Harga` (`Voucher` / `Diskon`) |
| `cartBottomQueuePoint` | `"423,1667"` | Point | Opens `Antrian` (`Bayar Sekarang` / `Bayar Nanti`) |
| `cartAddItemButton` | `"\+ Tambah Produk"` | Regex | Returns to catalog from cart to add more |
| `cartPayButton` | `"Bayar"` | Text | Opens payment tender sheet |

### Bottom Sheet Compact Focus Coordinates (Two-Tap Pattern)
- **`Edit Produk Keranjang`**: Tap `540,1175` &rarr; sheet shrinks to compact focus mode &rarr; tap `540,1487` &rarr; `inputText` &rarr; `pressKey: "enter"` &rarr; `Terapkan`.
- **`Tambah Potongan Harga` (`Diskon`)**: Tap `540,1487` &rarr; sheet shrinks to compact focus mode &rarr; tap `540,857` &rarr; `inputText` &rarr; `pressKey: "enter"` &rarr; `Terapkan`.
- **`Tambah Potongan Harga` (`Voucher`)**: Tap `"Tentukan kode voucher"` &rarr; tap `477,720` &rarr; `inputText` &rarr; `pressKey: "enter"` &rarr; `"Cek Kode"`.

---

## 5. Payment Methods, Tax & Receipt
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `payMethodTunai` | `"Tunai"` | Text | Cash payment tender |
| `payMethodHutang` | `"Hutang"` | Text | Credit / Pay Later tender (requires customer, `Masa Hutang`, `Uang Muka` e.g. `Rp5.000`) |
| `payMethodDebitCredit` | `"Debit/Kredit"` | Text | Card payment tender (requires `Masukkan Nomor Kartu`) |
| `payMethodQrisTransfer` | `"QRIS/Transfer"` | Text | QRIS or Bank transfer (renders `TRANSFER` on receipt) |
| `payExactCashButton` | `"Uang Pas"` | Text | Exact cash shortcut |
| `payExcessCashButton` | `"Rp50.000"` | Text | Excess cash suggestion chip |
| `paySuccessButton` | `"Pembayaran Berhasil"` | Text | Confirms Debit/Kredit and QRIS/Transfer payments |
| `dateSelector` | `".*202[0-9].*"` | Regex | Back-date transaction selector |
| `receiptTitle` | `"Transaksi Sukses"` | Text | Success receipt screen header |
| `receiptCloseButton` | `"Transaksi Baru"` | Text | Starts next transaction |
| `usahakuTabButton` / `pajakMenuRegex` | `"Usahaku\n.*"` / `"Pajak.*"` | Regex | Tax toggle (`pajakSwitchPoint: "985,231"`, `pajakPercentInputPoint: "540,349"`, confirm `Tutup` at `540,1160`) |

---

## 6. Dynamic Assertion Utilities (`output.kasir_utils`)
- `parseRp(str)`: Parses `"Rp20.000"` &rarr; `20000`.
- `formatRpRegex(num)`: Formats `20000` &rarr; `"Rp20\\.000"`.
- `parseCount(str)`: Parses `"Keranjang (3)"` &rarr; `3`.
- `getBackDateInfo()`: Computes yesterday's `pickerPattern`, `shortDateRegex`, and `receiptDateRegex` dynamically using `new Date()`.
