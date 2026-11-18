# Risk-Based Testing (RBT) & Tagging Matrix

This guide details how to categorize, tag, and execute Maestro flows based on business risk.

---

## 1. Risk Scoring Formula

$$\text{Risk Score (RS)} = \text{Probability of Failure (1-5)} \times \text{Business Impact (1-5)}$$

- **Probability (P)**: Code churn, dependency fragility, device-specific layout quirks.
- **Impact (I)**: Direct financial loss, blocked cashier transactions, data corruption, severe usability blockage.

---

## 2. Standard Tag Definitions

Every flow file must declare appropriate tags:

```yaml
appId: ${APP_ID}
tags:
  - regression-p0
  - kasir
  - checkout
---
```

### Risk Tiers:
| Tag | Risk Score | Scope / Focus | Trigger |
| :--- | :--- | :--- | :--- |
| `smoke` | $20 - 25$ | Absolute critical happy path (Cashier login, Add to cart, Pay) | Every build / PR |
| `regression-p0` | $20 - 25$ | Core transactions and business-critical operations | Pre-release |
| `regression-p1` | $12 - 19$ | High-risk features (Discounts, Shifts, Cart alterations) | Nightly run |
| `regression-p2` | $6 - 11$ | Medium-risk features (Customer CRUD, Date filters, Settings) | Weekly run |
| `low` | $1 - 5$ | Static pages, non-blocking cosmetic checks | On-demand |
| `quarantine` | N/A | Flaky or under-investigation flows (7-day SLA) | Excluded from CI |

---

## 3. CLI Tag Filtering

Maestro allows targeting specific suites via tags:

```bash
# Run only smoke flows
maestro test --include-tags smoke flows/

# Run P0 regression excluding quarantined tests
maestro test --include-tags regression-p0 --exclude-tags quarantine flows/
```

