# Maestro Assertions & Verifications

This guide details best practices for assertions in Maestro flows.

---

## 1. Assertion Types

### 1.1 `assertVisible`
Validates that an element is present and rendered on the screen:
```yaml
# Simple string match
- assertVisible: "Keranjang \\(1\\)"

# By Resource ID
- assertVisible:
    id: "dashboard_total_sales"

# By Regex
- assertVisible: ".*Selamat datang.*"
```

### 1.2 `assertNotVisible`
Validates that an element has disappeared from the view hierarchy (e.g. after dismissing a dialog or completing an order):
```yaml
- assertNotVisible:
    text: "Memproses transaksi..."
```

### 1.3 `assertTrue` with JavaScript Expressions
Enables complex validations such as comparing calculated totals, verifying environment variables, or parsing text:
```yaml
- runScript:
    file: ../../pages/helpers/calculate_total.js
- assertTrue: ${output.calculated_total == output.displayed_total}
```

---

## 2. Assertion Anti-Patterns to Avoid

- **Never assert inside Page Object files**: `pages/` files must only declare locators and reusable action subflows. Pass/fail assertions belong strictly in `flows/`.
- **Never insert arbitrary sleeps before assertions**: Maestro automatically polls the UI hierarchy before evaluating assertions (implicit wait). Do NOT add `pages/delay.js` before `assertVisible`.
- **Handle transient toasts properly**: Some Android toasts dismiss within 2 seconds. When asserting transient toast text, place `assertVisible` immediately following the trigger action without intermediate commands.

