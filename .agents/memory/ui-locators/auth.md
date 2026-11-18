# UI Locators: Authentication & PIN Pad

- **Domain**: Cashier / Store Login
- **Page Object File**: `pages/login/login_page.js`
- **Global Object**: `output.login_page`
- **Reusable Subflow**: `pages/login/login_flow.yaml`

---

## 1. Login Screen Locators
| Logical Key | Selector / Pattern | Type | Notes |
| :--- | :--- | :--- | :--- |
| `skipButton` | `"Lewati"` | Text | Skips introductory onboarding screens |
| `loginButton` | `"Masuk"` | Text | Navigates from welcome screen to phone form |
| `phoneNumberField` | `"+62xxxxxxxxxx"` | Text | Placeholder for mobile phone input |
| `PINField` | `"50%,41%"` | Point | Coordinates for custom PIN keypad input |
| `submitButton` | `"Masuk"` | Text | Submits phone + PIN authentication form |

---

## 2. Toasts & Alert Assertions
| Condition | Matcher | Type | Notes |
| :--- | :--- | :--- | :--- |
| Successful Login | `".*Selamat datang.*"` | Regex | Toast visible upon valid credentials |
| Invalid Phone | `"Nomor HP tidak terdaftar"` | Text | Inline validation error |
| Invalid PIN | `"PIN yang Anda masukkan salah"` | Text | Error alert below PIN dots |
| Update Dialog | `"Mengerti"` | Text | System modal dialog button (dismiss with `optional: true`) |

