# Domain Intelligence: POS Product Catalog

- **Domain**: Catalog Entities & Inventory Rules
- **Context**: Possaku Point of Sale System

---

## 1. Product Types

1. **Regular Products (`productRegularText`)**:
   - Single or multi-variant items sold by integer units.
   - Example: `O1 / o1 / Rp12.000 / 1 Varian`.
   - Adding to cart prompts a variant selection bottom sheet if variants exist (`variantReguler`).

2. **Decimal Products (`productDecimalText`)**:
   - Products measured in fractional weights or custom decimals (e.g. 0.5 kg, 1.25 L).
   - Example: `PD / produk desimal / Rp25.000 / 2 Varian`.
   - Quantity input supports decimal delimiters.

3. **Custom / Ad-Hoc Products (`customProductButton`)**:
   - Manually keyed items created on the fly during a transaction.
   - Fields: Name (`customNameField`), Price (`customPriceField`), Quantity (`customQtyField`).
   - Does not impact persistent catalog inventory.

---

## 2. Category Organization
Products are filtered by horizontal category tabs:
- `Semua`: Global catalog view (unfiltered).
- `Alat Tulis`: Stationery products.
- `Sembako`: Groceries and staple goods.
- `Makanan Ringan`: Snack foods.

