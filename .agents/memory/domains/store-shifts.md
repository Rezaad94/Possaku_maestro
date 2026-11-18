# Domain Intelligence: Store Shifts & Lifecycle

- **Domain**: Store Operational Status (Buka / Tutup) & Cashier Shifts
- **Context**: Possaku Point of Sale System

---

## 1. Store Lifecycle States

```text
[Tutup / Closed]  ── (Buka Usaha / Input Modal Awal) ──>  [Buka / Open]
       ▲                                                        │
       └──────── (Tutup Usaha / Rekap Kas Akhir) ───────────────┘
```

1. **Closed (`Tutup`)**:
   - Cashier cannot initiate catalog sales or process transactions.
   - If a cashier navigates to Kasir, Possaku displays a warning banner:
     `bukaUsahaWarningText: "(?s)Buka usaha dulu untuk menggunakan fitur ini.*"`
   - Opening requires setting initial drawer cash (`modal_awal`).

2. **Open (`Buka`)**:
   - Full catalog and checkout operations are unlocked.
   - Total transactions and revenue aggregate in the `Dashboard` overview.

---

## 2. Shift Reconciliation
- Closing a shift prompts a summary modal displaying total cash intake, card payments, and discrepancy checks before confirming closure with `confirmYesButton`.

