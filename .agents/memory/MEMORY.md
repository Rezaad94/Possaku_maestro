# Semantic Memory System for Possaku Mobile Automation

> **Purpose**: A persistent, structured semantic memory bank storing mobile domain knowledge, verified element mappings, mobile runtime failure resolutions, and test data semantics for Possaku POS (`com.cloudiex.possaku`).
> **Audience**: All AI agents (High-tier & Low-tier) & human automation engineers.

---

## 🧠 Memory Access Protocol for AI Agents

1. **Before Writing Any Test or Page Object**:
   - Check [ui-locators/](ui-locators/) to reuse verified, resilient locators instead of guessing.
   - Check [domains/](domains/) to align with valid product schemas, cart calculation rules, and store shift states.
2. **When Debugging a Failure**:
   - Check [failure-patterns/](failure-patterns/) to see if the error is a documented soft keyboard obstruction, ADB disconnection, or lazy-scroll issue.
3. **When a New Locator or Quirk is Discovered / Fixed**:
   - Immediately update or append the finding to the corresponding memory file.

---

## 📂 Semantic Memory Map

| Category | File | Description |
| :--- | :--- | :--- |
| **Kasir & Catalog** | [ui-locators/kasir.md](ui-locators/kasir.md) | Verified locators for catalog items, variants, cart modal, and payment options |
| **Auth & PIN** | [ui-locators/auth.md](ui-locators/auth.md) | Phone input, numeric keypad, welcome toast, error alerts |
| **Dashboard** | [ui-locators/dashboard.md](ui-locators/dashboard.md) | Sales widgets, transaction counters, date filter chips |
| **Usahaku & Shifts** | [ui-locators/usahaku.md](ui-locators/usahaku.md) | Open/close store triggers, cash drawer inputs, shift status |
| **Daftar Pelanggan** | [ui-locators/daftar-pelanggan.md](ui-locators/daftar-pelanggan.md) | Customer directory, search input, customer creation sheet |
| **Lain-lain & Settings**| [ui-locators/lain-lain.md](ui-locators/lain-lain.md) | Online store settings, printer connections, general app preferences |
| **POS Catalog Domain** | [domains/pos-catalog.md](domains/pos-catalog.md) | Product entities, regular products, decimal quantities, custom items |
| **Cart & Checkout Domain** | [domains/cart-checkout.md](domains/cart-checkout.md) | Cart totaling math, discounts, tax calculations, payment methods |
| **Store Shifts Domain** | [domains/store-shifts.md](domains/store-shifts.md) | Store lifecycle (Opened vs Closed), cashier balance tracking |
| **Auth Domain** | [domains/auth-possaku.md](domains/auth-possaku.md) | Test accounts, dev/staging credentials, session tokens |
| **Keyboard Obstruction** | [failure-patterns/soft-keyboard-obstruction.md](failure-patterns/soft-keyboard-obstruction.md) | Mitigating obscured action buttons caused by the Android soft keyboard |
| **ADB & Devices** | [failure-patterns/device-connection.md](failure-patterns/device-connection.md) | Handling ADB socket disconnects, emulator freezes, unauthorized bridges |
| **Scroll & Lazy Views** | [failure-patterns/scroll-lazy-rendering.md](failure-patterns/scroll-lazy-rendering.md) | Jetpack Compose and RecyclerView lazy-rendering swipe rules |
| **Step Traceability** | [failure-patterns/step-traceability.md](failure-patterns/step-traceability.md) | Flow step formatting and `inject_steps.py` report generation |
| **Timing & Auto-Wait** | [failure-patterns/flakiness-and-timing.md](failure-patterns/flakiness-and-timing.md) | Eliminating explicit sleep delays in favor of visibility conditions |

