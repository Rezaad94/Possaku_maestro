# Implementation Plan: Elevating Possaku Maestro Automation Architecture to Match Hunt Standards

This plan outlines the architecture, directory structure, rules, semantic memory, and skill modules required to bring `/Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro` to the enterprise-grade automation standards established in `Hunt/hunt_automation_test`.

---

## 1. High-Level Architecture Comparison

| Capability | Hunt (`hunt_automation_test`) | Current Possaku (`Possaku_maestro`) | Target Possaku Standard |
| :--- | :--- | :--- | :--- |
| **Agent Directive** | Root `AGENTS.md` (400+ lines, strict zero-tolerance rules) | Subfolder `.agents/AGENTS.md` (basic POM overview) | **Root `AGENTS.md`** with full RBT matrix, AI rules, blueprints & links |
| **Framework Rules** | `.agents/rules/playwright-standards.md` | None | **`.agents/rules/maestro-standards.md`** |
| **Knowledge Skills** | `.agents/skills/playwright/` (SKILL.md + 6 references) | None | **`.agents/skills/maestro/`** (`SKILL.md` + 6 specialized references) |
| **Semantic Memory** | `.agents/memory/` (index.json, MEMORY.md, locators, domains, failure-patterns) | None | **`.agents/memory/`** (full registry, fast index, screen locators, domain rules, mobile failure patterns) |
| **MCP Integration** | Playwright MCP integration | None | **Maestro MCP guide & reference** (`list_devices`, `inspect_screen`, `run`, `take_screenshot`) |
| **Risk-Based Testing (RBT)** | Strict tags (`@smoke`, `@regression-p0`, `@regression-p1`, `@low`, `@quarantine`) | Untagged / rudimentary tags | **Strict RBT tags** across all `.yaml` flows with execution matrix |
| **Step Traceability** | `test.step` + trace debugging | `inject_steps.py` + HTML report | Formalized step naming standard optimized for `inject_steps.py` |

---

## 2. Directory Structure to Implement

```text
/Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro/
├── AGENTS.md                                    # [NEW] Root AI Directive & Engineering Guideline
├── .agents/
│   ├── rules/
│   │   └── maestro-standards.md                 # [NEW] Strict rules: zero sleep, POM, locator hierarchy
│   ├── skills/
│   │   └── maestro/
│   │       ├── SKILL.md                         # [NEW] Token-optimized Maestro QA skill
│   │       └── references/
│   │           ├── locators.md                  # [NEW] ID > Text > Regex > Relative locators
│   │           ├── assertions.md                # [NEW] assertVisible, assertTrue, negative checks
│   │           ├── pom-and-flows.md             # [NEW] Pages (JS/YAML) vs Flows (Scenarios) separation
│   │           ├── rbt-and-tagging.md           # [NEW] Risk scoring matrix (P0-P3) and Maestro tags
│   │           ├── ci-and-debugging.md          # [NEW] CLI runner, inject_steps.py, HTML reporting
│   │           └── mcp-integration.md           # [NEW] Maestro MCP workflow (inspect, run, debug)
│   └── memory/
│       ├── MEMORY.md                            # [NEW] Semantic Memory protocol & registry
│       ├── index.json                           # [NEW] Fast lookup keyword index
│       ├── ui-locators/
│       │   ├── auth.md                          # [NEW] Login, phone input, PIN pad locators
│       │   ├── kasir.md                         # [NEW] Catalog, products, cart modal, payments
│       │   ├── dashboard.md                     # [NEW] Metric cards, date filters, store status
│       │   ├── usahaku.md                       # [NEW] Store shifts, open/close store
│       │   ├── daftar-pelanggan.md              # [NEW] Customer list, search, add customer
│       │   └── lain-lain.md                     # [NEW] Settings, online store configuration
│       ├── domains/
│       │   ├── pos-catalog.md                   # [NEW] Catalog entities, decimal qty, variants
│       │   ├── cart-checkout.md                 # [NEW] Cart calculations, discounts, payment types
│       │   ├── store-shifts.md                  # [NEW] Cashier shift lifecycle, store open/closed states
│       │   └── auth-possaku.md                  # [NEW] Test accounts, credentials, OTP/PIN rules
│       └── failure-patterns/
│           ├── soft-keyboard-obstruction.md     # [NEW] Keyboard covering submit buttons
│           ├── device-connection.md             # [NEW] ADB disconnection & emulator restarts
│           ├── scroll-lazy-rendering.md         # [NEW] Off-screen recycler views & swipe boundaries
│           ├── step-traceability.md             # [NEW] Step comments & inject_steps.py integration
│           └── flakiness-and-timing.md          # [NEW] Zero hard sleep, dialog handling, retry logic
├── config/
│   └── env.yaml                                 # Existing environment variables
├── pages/                                       # Existing Page Objects (JS / YAML subflows)
├── flows/                                       # Existing Flows (To be aligned with RBT tags)
├── .maestro/
│   └── regression_suite.yaml                    # Main test suite entrypoint
├── inject_steps.py                              # Report step injection script
└── run_suite.sh                                 # Runner script
```

---

## 3. Detailed Component Specifications

### 3.1 Root `AGENTS.md`
- **AI Agent Directive & Skill Integration**: On-demand navigation to `.agents/skills/maestro/` and `.agents/memory/`.
- **Strict Zero-Tolerance Rules for AI**:
  1. *NEVER use hard delays/sleeps* (`delay.js` / arbitrary wait pauses) — rely on Maestro's implicit wait and condition assertions.
  2. *NEVER put scenario-level assertions inside Page Objects* — pages only hold locators and component interactions.
  3. *NEVER hardcode raw UI locators inside flows* — import from `pages/`.
  4. *STRICT RBT TAGGING* — Every flow must define `tags: [smoke, regression-p0, ...]` in its metadata.
  5. *MANDATORY STEP NUMBERING* — Every logical section in a flow must have explicit step comments (`# Step 1: ...`, `# Step 2: ...`) to enable granular step tracing via `inject_steps.py`.
  6. *MANDATORY SEMANTIC MEMORY USAGE* — Always verify locators in `.agents/memory/ui-locators/` before writing code; update memory immediately when new elements are mapped.
  7. *NO UNTRACKED TEMPORARY ARTIFACTS* — Clean up ad-hoc test flows, screen dumps, or temporary APKs.
- **Risk-Based Testing (RBT) Framework**: Risk score formula ($RS = P \times I$), classification matrix, CI triggers.
- **Domain Symmetry**: 1-to-1 mapping between mobile app bottom navigation / drawer (`Kasir`, `Dashboard`, `Usahaku`, `Pelanggan`, `Lainnya`), `pages/`, and `flows/`.
- **Copy-Paste Blueprints**: Standard YAML flow blueprint, Page Object JS blueprint, reusable dialog subflow blueprint.
- **Pre-Flight Self-Verification Checklist**: Checklist for human and AI before merging/running flows.

### 3.2 `.agents/rules/maestro-standards.md`
A dedicated, high-density ruleset covering:
- Naming conventions (`snake_case` for files and locators, `_page.js` / `_flow.yaml` suffixes).
- Selector priority order (`id` / Accessibility ID > `text` / Content Description > relative positioning `below`/`above`/`rightOf` > bounded coordinates as last resort).
- Dynamic variable resolution via `output.<page>.<element>` and `${env.<VAR>}`.
- State isolation (`- clearState` on standalone E2E flows, modular teardown).

### 3.3 `.agents/skills/maestro/`
- **`SKILL.md`**: Primary entry point for AI models with instant reference golden rules.
- **`references/locators.md`**: Android View Hierarchy targeting, regex matching, child selectors, coordinate tapping best practices.
- **`references/assertions.md`**: `assertVisible`, `assertNotVisible`, `assertTrue` with JS expressions, condition polling.
- **`references/pom-and-flows.md`**: Dual-layer architecture (`runScript: pages/..._page.js` + `runFlow`).
- **`references/rbt-and-tagging.md`**: Maestro CLI tagging flags (`--include-tags`, `--exclude-tags`), regression suite grouping.
- **`references/ci-and-debugging.md`**: Running headless, `inject_steps.py` report generation, ADB logs, hierarchy dumps.
- **`references/mcp-integration.md`**: Operating live emulators via the Maestro MCP server (`list_devices`, `inspect_screen`, `run`, `take_screenshot`).

### 3.4 `.agents/memory/`
- **`MEMORY.md` & `index.json`**: Indexing system for instant retrieval of verified screens, domain definitions, and failure resolutions.
- **`ui-locators/`**: Populated with verified locators extracted from the existing codebase:
  - `kasir.md`: Full catalog selectors, custom product modals, cart buttons, quantity adjusters, checkout payment options.
  - `auth.md`: Phone number inputs, PIN keypad coordinates/text, welcome toasts, error banners.
  - `dashboard.md`: Date filters, revenue widgets, order counts.
  - `usahaku.md`: Open/close store triggers, shift modal locators.
  - `daftar-pelanggan.md`: Search bar, customer cards, add customer modal fields.
  - `lain-lain.md`: Settings toggles, online store configurations.
- **`domains/`**: Business rules for Possaku POS:
  - `pos-catalog.md`: Product catalog pricing rules, decimal quantities, product variants.
  - `cart-checkout.md`: Cart total calculation logic, discounts, vouchers, taxes.
  - `store-shifts.md`: Shift start/end states, cash in drawer validations.
  - `auth-possaku.md`: Test credentials, test accounts for dev/staging.
- **`failure-patterns/`**: Field-tested mobile flakiness mitigations:
  - `soft-keyboard-obstruction.md`: How to dismiss Android keyboards before asserting or tapping bottom buttons.
  - `device-connection.md`: Diagnosing and recovering from broken ADB bridges.
  - `scroll-lazy-rendering.md`: Handling Android Jetpack Compose / RecyclerView lazy loading via programmatic swipe.
  - `step-traceability.md`: Structuring YAML steps so `inject_steps.py` can generate detailed per-step HTML reports.
  - `flakiness-and-timing.md`: Replacing explicit `delay.js` sleep scripts with Maestro visibility assertions.

### 3.5 Existing Flows Alignment
- Update existing flows in `flows/` to include standardized RBT tags:
  - `flows/login/valid_login_flow.yaml`: `@smoke`, `@regression-p0`, `@auth`
  - `flows/login/invalid_login_flow.yaml`: `@regression-p1`, `@auth`
  - `flows/kasir/catalog_qty_flow.yaml`: `@regression-p0`, `@kasir`, `@catalog`
  - `flows/kasir/cart_qty_flow.yaml`: `@regression-p0`, `@kasir`, `@cart`
  - `flows/usahaku/open_close_store_flow.yaml`: `@regression-p1`, `@usahaku`
  - `flows/dashboard/overview_flow.yaml`: `@regression-p1`, `@dashboard`
  - `flows/dashboard/filter_flow.yaml`: `@regression-p2`, `@dashboard`
  - `flows/lain_lain/online_store_setting_flow.yaml`: `@regression-p2`, `@settings`
- Review existing flows for numbered step comments (`# Step 1: ...`, `# Step 2: ...`) to maximize the fidelity of `report.html`.

---

## 4. Execution Steps

1. **Step 1: Scaffold `.agents` Architecture**
   - Create directories: `.agents/rules/`, `.agents/skills/maestro/references/`, `.agents/memory/ui-locators/`, `.agents/memory/domains/`, `.agents/memory/failure-patterns/`.

2. **Step 2: Generate Core Directives & Standards**
   - Author root `AGENTS.md` adapted for Possaku + Maestro.
   - Author `.agents/rules/maestro-standards.md`.

3. **Step 3: Create Maestro Skill & References**
   - Author `.agents/skills/maestro/SKILL.md`.
   - Author reference files: `locators.md`, `assertions.md`, `pom-and-flows.md`, `rbt-and-tagging.md`, `ci-and-debugging.md`, `mcp-integration.md`.

4. **Step 4: Build Semantic Memory Bank**
   - Author `.agents/memory/MEMORY.md` and `.agents/memory/index.json`.
   - Populate `ui-locators/` (`auth.md`, `kasir.md`, `dashboard.md`, `usahaku.md`, `daftar-pelanggan.md`, `lain-lain.md`).
   - Populate `domains/` (`pos-catalog.md`, `cart-checkout.md`, `store-shifts.md`, `auth-possaku.md`).
   - Populate `failure-patterns/` (`soft-keyboard-obstruction.md`, `device-connection.md`, `scroll-lazy-rendering.md`, `step-traceability.md`, `flakiness-and-timing.md`).

5. **Step 5: Align Existing Flows with RBT Tagging & Step Traceability**
   - Add risk tags to header blocks of flow files.
   - Ensure step comments match the reporting structure.

6. **Step 6: Verification & Syntax Validation**
   - Run `maestro check-syntax` across all modified flows to ensure 100% syntax validity.
   - Validate JSON syntax of `index.json`.
