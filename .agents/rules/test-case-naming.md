# Rule: Test Case & Step Naming Conventions

This rule standardizes test case IDs, flow naming, and in-flow step comment conventions across all Maestro YAML flows in Possaku.

---

## 1. Domain Prefixes
Every module has a unique uppercase prefix:

| Module / Domain | Prefix | Example TC ID |
| :--- | :---: | :--- |
| **Authentication & Session** | `AUTH` | `AUTH-01`, `AUTH-02` |
| **Dashboard** | `DASH` | `DASH-01`, `DASH-02` |
| **Kasir (POS, Cart, Payments)** | `KASIR` | `KASIR-01`, `KASIR-28` |
| **Atur Produk (Catalog, Categories)** | `PROD` | `PROD-01`, `PROD-15` |
| **Usahaku (Store Settings & Tax)** | `USAHA` | `USAHA-01`, `USAHA-05` |
| **Lain-Lain (Online Store, etc.)** | `LAIN` | `LAIN-01`, `LAIN-04` |

---

## 2. In-Flow Test Case Naming Format
Every test section in a Maestro YAML flow MUST start with a standardized comment header matching:
```yaml
# [PREFIX-XX] <Action or Expectation Summary>
```
Examples:
- `# [AUTH-01] Login with valid phone number (+6285...)`
- `# [KASIR-13] Increase quantity in cart`
- `# [KASIR-28] Finish transaction with Tunai method`
- `# [PROD-05] Search product by keyword`
- `# [DASH-01] Open and close store via dashboard slider`

### Setup & Teardown Comments
Non-test setup/teardown steps MUST use:
- `# [SETUP] Ensure Logged In`
- `# [SETUP] Navigate to Kasir menu from Dashboard`
- `# [TEARDOWN] Reset tax settings to default`

---

## 3. Flow File Naming Conventions
- Test flow files: `flows/<domain>/<feature_or_scenario>_flow.yaml` (snake_case)
- Page object files: `pages/<domain>/<name>_page.js`
- Subflow files: `pages/<domain>/<name>_flow.yaml`

---

## 4. Integration with HTML Reporting (`inject_steps.py`)
`inject_steps.py` automatically parses YAML comments and groups steps into test case cards. The bracketed format `[PREFIX-XX]` ensures:
1. Every test case appears cleanly in the HTML summary matrix table with its exact ID and description.
2. Setup and teardown steps are separated from test case metrics.
3. Test case pass/fail badges, duration rollups, and screenshot lightboxes align with the official test documentation.

