# UI Locators: Usahaku (Store Management & Shifts)

- **Domain**: Store Shifts & Store Status
- **Page Object File**: `pages/usahaku/usahaku_page.js`
- **Global Object**: `output.usahaku_page`

---

## 1. Store Management Locators
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `usahakuHeader` | `"Usahaku"` | Text | Header text for Usahaku screen |
| `toggleStoreSwitchPoint` | `"878,341"` | Point | Coordinates for the store status toggle (Buka / Tutup) |
| `confirmYesButton` | `"Ya"` | Text | Confirmation dialog accept button |
| `confirmNoButton` | `"Tidak"` | Text | Confirmation dialog dismiss button |

---

## 2. Shift Management
| Condition | Matcher | Type | Notes |
| :--- | :--- | :--- | :--- |
| Modal Buka Usaha | `"Buka Usaha"` | Text | Modal header for opening shift |
| Modal Tutup Usaha | `"Tutup Usaha"` | Text | Modal header for closing shift |
| Input Modal Awal | `"Masukkan modal awal"`| Text | Starting drawer cash input field |
| Button Simpan Shift | `"Simpan"` | Text | Submits shift status change |

