# Possaku Kasir (POS) – Comprehensive Test Plan & Implementation Matrix

**Document Version:** 1.0  
**Target Module:** Kasir / Point of Sale (`com.cloudiex.possaku`)  
**Target Environment:** Android 11 (`android_11`)  
**Automation Engine:** Maestro Mobile UI Automation  
**Date:** 2026-11-11  

---

## 1. Executive Summary

The **Kasir (POS)** module is the transaction processing engine of the Possaku merchant application. It encompasses:
1. **Product Catalog & Scanning** (Product discovery, stock checking, barcode scanning, manual/custom items, sorting, and category filters).
2. **Cart Management & Customer Operations** (Quantity modifiers, item deletion, item re-adding from cart, customer selection, and new customer registration).
3. **Price Adjustments & Promotions** (Line-item discounts, order-level discounts, voucher redemption, and tax toggles).
4. **Tender & Payment Processing** (Multi-method checkout: Cash, PayLater/Hutang, QRIS/Transfer, Debit/Credit, exact vs. excess cash, back-date adjustment, and receipt validation).
5. **Special Business Rules** (Booked vs. unbooked BO products and Offline mode).

This plan maps all **42 required Kasir test cases** into automated Maestro flows adhering strictly to zero-sleep policies, Page Object Model (`pages/kasir/kasir_page.js`), and RBT tagging standards.

---

## 2. 42-Test-Case Traceability Matrix

| # | Test Case Description | Flow Implementation | Automation Status |
| :---: | :--- | :--- | :---: |
| **1** | Add product to cart from katalog | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **2** | Add product manualy (Produk Kostum) | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **3** | Increase qty in katalog | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **4** | Decrease qty in katalog | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **5** | Edit qty manualy in katalog | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **6** | Input decimal quantity | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **7** | Verify quantity added in cart button | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **8** | Verify other category shown | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **9** | Search product by text | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **10** | Search product by scanner | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **11** | Scan barcode by device camera | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **12** | Scan barcode by scanner | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **13** | Increase qty in cart | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **14** | Decrease qty in cart | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **15** | Edit qty manualy in cart | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **16** | Delete item in cart | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **17** | Add item from cart (`+ Tambah Produk`) | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **18** | Select customer in cart | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **19** | Add new customer | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **20** | Add nominal discount per item | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **21** | Add percentage discount per item | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **22** | Add nominal discount per transaction | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **23** | Add percentage discount per transaction | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **24** | Add valid voucher | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **25** | Add invalid voucher | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **26** | Verify total if tax active | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **27** | Verify total if tax inactive | `flows/kasir/cart_flow.yaml` | ✅ Automated |
| **28** | Finish transaction with Tunai method | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **29** | Finish transaction with Hutang method | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **30** | Finish transaction with Debit/Credit method | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **31** | Finish transaction with QRIS/Transfer method | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **32** | Pay with excess money | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **33** | Pay with exact money (`Uang Pas`) | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **34** | Select back date in cashier | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **35** | User see correct data in struck (receipt) | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **36** | Create transaction with not booked BO product | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **37** | Create transaction with booked BO product | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **38** | Offline Mode | `flows/kasir/payment_checkout_flow.yaml` | ✅ Automated |
| **39** | Sorting based on alphabet ascending | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **40** | Sorting based on alphabet descending | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **41** | Sorting based on stock ascending | `flows/kasir/catalog_flow.yaml` | ✅ Automated |
| **42** | Sorting based on stock descending | `flows/kasir/catalog_flow.yaml` | ✅ Automated |

---

## 3. Flow Architecture & Modularity

Rather than maintaining a fragile monolithic flow, the Kasir suite is partitioned into 3 cohesive, self-contained flows:

### 3.1 `flows/kasir/catalog_flow.yaml`
- **Focus:** Product selection, variants, custom manual product, search, scanner camera, categories, and sorting.
- **Key Assertions:** `Kasir`, `Keranjang (N)`, `Semua.*`, product names, search filtered lists.
- **Tagged:** `regression-p0`, `kasir`, `catalog`

### 3.2 `flows/kasir/cart_flow.yaml`
- **Focus:** Line item quantity editing, item deletion with confirmation, customer lookup and creation, item/transaction discounts, vouchers, and tax toggle.
- **Key Assertions:** Dynamic totals, customer modal, discount modals, delete confirmations.
- **Tagged:** `regression-p0`, `kasir`, `cart`

### 3.3 `flows/kasir/payment_checkout_flow.yaml`
- **Focus:** Multi-tender checkout (Cash, Hutang, Debit/Kredit, QRIS), back-date selection, exact cash vs excess cash, and receipt verification.
- **Key Assertions:** `Pembayaran`, `Metode Pembayaran`, `Transaksi Sukses`, `ID Trans`, `Pilih Printer`.
- **Tagged:** `regression-p0`, `kasir`, `payment`

---

## 4. Zero-Sleep Policy Compliance

In accordance with `.agents/rules/maestro-standards.md`:
- **No `pages/delay.js`**: All hardcoded loops and busy-waits have been replaced with declarative `assertVisible` conditions and `runFlow when` guards.
- **Coachmark handling**: Cart and catalog coachmarks (`Mengerti`) are handled conditionally:
  ```yaml
  - runFlow:
      when:
        visible: ".*Mengerti.*"
      commands:
        - back
  ```
