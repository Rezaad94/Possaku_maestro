# Maestro Mobile Automation Standards & Conventions

This project strictly adheres to **Risk-Based Testing (RBT)**, **Page Object Model (POM) via JavaScript Locators & Reusable Subflows**, and **Standardized File Naming**.

---

## 1. File Naming Rules
- **Format**: Strict `snake_case` with explicit dot-notated suffix (`<name>_<role>.<ext>`).
- **Page Element Objects**: `pages/<domain>/<name>_page.js` (Object registered on `output.<name>_page`).
- **Reusable Subflows**: `pages/<domain>/<name>_flow.yaml`.
- **Test Scenarios**: `flows/<domain>/<name>_flow.yaml`.
- **Helpers / Utilities**: `pages/helpers/<name>.js`.

---

## 2. Risk-Based Testing (RBT) Tagging
Every test flow MUST include risk tier tags in its header block:
```yaml
appId: ${APP_ID}
tags:
  - regression-p0
  - kasir
  - catalog
---
```
- `smoke` / `regression-p0`: Critical path (Score 20-25) — runs on every build ($<5$ min target).
- `regression-p1` / `core`: High risk (Score 12-19) — runs on nightly regression suite.
- `regression-p2` / `extended`: Medium risk (Score 6-11) — runs weekly.
- `low`: Low risk (Score 1-5) — runs ad-hoc.
- `quarantine`: Flaky flows under active investigation (7-day SLA).

---

## 3. Selector Priority Order (Android POS UI)
1. **Accessibility ID / Resource ID (`id`)**: Highest reliability (e.g. `id: "btn_checkout"`).
2. **Text / Content Description (`text`)**: Use clean string or regex matching (e.g. `text: "Kasir\\n"` or `text: "Keranjang.*"`).
3. **Relative Positioning**: Use `below`, `above`, or `rightOf` when targeting repeating elements in catalog grids or tables.
4. **Coordinate Points (`point: "X%, Y%"`)**: Strictly forbidden as a primary selector. Use only for unexposed PIN keypads or swipe boundaries.

---

## 4. Maestro Coding Standards (Token & Execution Efficient)
1. **Zero Sleep Policy**: Never use `pages/delay.js` or manual sleep steps. Rely on Maestro's implicit wait and `assertVisible`.
2. **No Assertions in Page Objects**: Keep `assertVisible` and `assertTrue` in `flows/`. Page objects only define locators or atomic interaction steps.
3. **Semantic Memory Pre-Check**: Consult `.agents/memory/ui-locators/` and `.agents/memory/domains/` before adding new locators.
4. **Standardized Test Case & Step Naming**: Follow `.agents/rules/test-case-naming.md`. Always structure test actions with standardized headers (`# [PREFIX-XX] <Title>`, `# [SETUP] <Title>`) so `inject_steps.py` generates accurate per-test-case metrics in HTML reports.
5. **State Hygiene & Session Reuse**: Auth flows (`flows/login/`) manage cold state explicitly (`clearState: true` via `login_flow.yaml`). Feature flows (`flows/kasir/`, `flows/dashboard/`, etc.) MUST use `pages/login/ensure_logged_in.yaml` (`clearState: false`) for fast session reuse.
6. **Dynamic Assertions**: Never hardcode prices, cart badge counts, or back-dates in assertions. Read live UI text via `copyTextFrom` (`maestro.copiedText`) and compute expected values dynamically via `output.kasir_utils` (`parseRp`, `formatRpRegex`, `parseCount`, `getBackDateInfo`).

