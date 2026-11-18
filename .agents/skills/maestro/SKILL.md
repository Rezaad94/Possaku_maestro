---
name: maestro
description: High-density, token-optimized Maestro mobile automation guidance for Android and iOS. Covers Page Object Model (POM), Risk-Based Testing (RBT), selector hierarchy, assertions, subflows, Maestro MCP server, and HTML reporting for Possaku POS.
---

# Maestro Mobile Automation Skill (Token-Optimized)

> **Philosophy**: High signal, zero token waste. Production-grade mobile testing patterns adapted for Maestro CLI v2.x and Possaku POS.

---

## ⚡ Golden Rules (Instant Reference)

1. **Locators**: `id` > `text` / regex > relative positioning (`below`, `above`). Avoid raw pixel coordinates.
2. **Auto-Waiting**: Never hardcode delays (`delay.js`). Rely on Maestro implicit waiting and `assertVisible`.
3. **Assertions**: Keep scenario validations in `flows/`, never inside `pages/` element dictionaries.
4. **Composition**: Import locators with `- runScript: pages/<domain>/<name>_page.js` and reusable subflows with `- runFlow`.
5. **RBT Tagging**: Every flow header must declare risk tags (`tags: [smoke, regression-p0, ...]`).
6. **Step Traceability**: Divide scenarios into numbered step comments (`# Step 1: ...`) for `inject_steps.py`.
7. **MCP Operation**: Use Maestro MCP tools (`inspect_screen`, `run`, `take_screenshot`) when driving live emulators.

---

## 📚 Deep-Dive References (Progressive Disclosure)

Only read specific reference files when deep implementation details are required:

| Topic | Reference File | Key Topics Covered |
| :--- | :--- | :--- |
| **Locators & Selectors** | [locators.md](references/locators.md) | `id`, `text`, regex matching, relative selectors, point taps |
| **Assertions & Verification** | [assertions.md](references/assertions.md) | `assertVisible`, `assertNotVisible`, `assertTrue` with JS expressions |
| **POM & Subflow Architecture**| [pom-and-flows.md](references/pom-and-flows.md) | JS locator objects, parameter passing via `env`, subflows |
| **RBT & Tagging** | [rbt-and-tagging.md](references/rbt-and-tagging.md) | Risk scoring matrix (P0-P3), CLI `--include-tags`, suite organization |
| **CI, Runner & Reporting** | [ci-and-debugging.md](references/ci-and-debugging.md) | `run_suite.sh`, `inject_steps.py`, HTML reports, debug output |
| **Maestro MCP Server** | [mcp-integration.md](references/mcp-integration.md) | Real-time device automation via MCP tools (`list_devices`, `run`) |

---

## 🚀 Quick Code Archetype

```yaml
# 1. Flow Definition (flows/kasir/sample_flow.yaml)
appId: ${APP_ID}
tags:
  - regression-p0
  - kasir
---
# Load Page Objects
- runScript:
    file: ../../pages/login/login_credential.js
- runScript:
    file: ../../pages/login/login_page.js
- runScript:
    file: ../../pages/kasir/kasir_page.js

# Step 1: Login to Application
- runFlow:
    file: ../../pages/login/login_flow.yaml
    env:
      phoneNumber: "${output.login_credential.dev.validPhoneNumber2}"
      PIN: "${output.login_credential.dev.validPIN}"
      expected1: ".*Selamat datang.*"

# Step 2: Open Kasir Catalog
- tapOn:
    text: "Mengerti"
    optional: true
- tapOn: "${output.kasir_page.kasirMenuButton}"

# Step 3: Add Item to Cart
- tapOn: "${output.kasir_page.productRegularText}"
- tapOn: "${output.kasir_page.variantReguler}"
- tapOn: "${output.kasir_page.variantSheetAdd}"

# Step 4: Validate Cart
- assertVisible: "Keranjang \\(1\\)"
```

