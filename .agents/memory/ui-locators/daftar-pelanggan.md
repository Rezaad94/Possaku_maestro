# UI Locators: Daftar Pelanggan (Customer Directory)

- **Domain**: Customer Management
- **Page Object File**: `pages/daftar_pelanggan/daftar_pelanggan_page.js`
- **Global Object**: `output.daftar_pelanggan_page`

---

## 1. Directory Locators
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `daftarPelangganIcon` | `"Daftar\nPelanggan"` | Text | Menu button / icon for customer directory |
| `skipIntroPelangganButton` | `"Lewati"` | Text | Skips customer feature tour |
| `searchPelangganField` | `"Cari pelanggan"` | Text | Search input field for customer names/phones |

---

## 2. Customer Actions
| Condition | Matcher | Type | Notes |
| :--- | :--- | :--- | :--- |
| Add Customer Button | `"Tambah Pelanggan"` | Text | Opens customer creation form |
| Customer Name Field | `"Nama Pelanggan"` | Text | Input for customer full name |
| Customer Phone Field| `"Nomor Telepon"` | Text | Input for customer mobile phone |
| Save Customer Button| `"Simpan"` | Text | Submits new customer form |

