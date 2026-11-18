# Maestro Page Object Model (POM) & Subflow Architecture

This guide explains how to structure Page Objects and Test Flows in Possaku Maestro.

---

## 1. Architectural Separation

The framework separates UI element definitions from scenario flows:

```text
pages/                    <-- Element Locators & Reusable Action Modules
  └── kasir/
      └── kasir_page.js   <-- Registers output.kasir_page
flows/                    <-- Scenarios / Test Cases
  └── kasir/
      └── catalog_qty_flow.yaml <-- Imports page JS, executes steps, asserts outcomes
```

---

## 2. Page Object Definitions (`pages/<domain>/<name>_page.js`)

Page objects export a clean dictionary attached to Maestro's global `output` object:

```javascript
output.kasir_page = {
  // Navigation
  kasirMenuButton: "Kasir\n",

  // Catalog selectors
  searchFieldHint: "Cari produk",
  productRegularText: "O1\no1\nRp12.000\n1 Varian",
  variantReguler: "Reguler.*",
  variantSheetAdd: "Tambahkan",
  variantSheetQtyMinus: "-",
  variantSheetQtyPlus: "+",

  // Cart selectors
  cartButtonRegex: "Keranjang.*",
  cartPayButton: "Bayar"
};
```

### Accessing in Flows:
```yaml
- runScript:
    file: ../../pages/kasir/kasir_page.js

- tapOn: "${output.kasir_page.kasirMenuButton}"
```

---

## 3. Reusable Subflows (`pages/<domain>/<name>_flow.yaml`)

When a multi-step sequence is reused across multiple flows (such as logging in or dismissing app update banners), encapsulate it into a subflow:

```yaml
# pages/login/login_flow.yaml
appId: ${APP_ID}
---
- tapOn: "${output.login_page.phoneInputField}"
- inputText: "${phoneNumber}"
- tapOn: "${output.login_page.pinField}"
- inputText: "${PIN}"
- assertVisible:
    text: "${expectedToast}"
```

### Invoking Subflows:
```yaml
- runFlow:
    file: ../../pages/login/login_flow.yaml
    env:
      phoneNumber: "${output.login_credential.dev.validPhoneNumber2}"
      PIN: "${output.login_credential.dev.validPIN}"
      expectedToast: ".*Selamat datang.*"
```

