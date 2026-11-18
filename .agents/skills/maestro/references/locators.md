# Maestro Locator & Selector Strategies

This guide covers resilient locator strategies in Maestro for Android applications like Possaku POS.

---

## 1. Hierarchy of Selectors

Always prefer selectors from top to bottom:

```text
Accessibility ID / Resource ID (id)
  └─ Text / Content Description (text / textRegex)
      └─ Relative Selectors (below, above, rightOf, leftOf)
          └─ Index Filtering (index: N)
              └─ Percentage Coordinates (point: "X%, Y%") [LAST RESORT ONLY]
```

### 1.1 Resource ID (`id`)
The most stable locator. Resistant to localization changes and copy updates:
```yaml
- tapOn:
    id: "btn_bayar"
```

### 1.2 Text Matching (`text` & Regular Expressions)
Used when IDs are absent or when asserting dynamic textual content:
```yaml
# Exact or substring match
- tapOn: "Kasir\n"

# Regex pattern match
- tapOn: "Keranjang.*"

# Optional element handling
- tapOn:
    text: "Mengerti"
    optional: true
```

### 1.3 Relative Positioning
When multiple elements share identical labels (e.g. repeated "+" buttons in a catalog list):
```yaml
- tapOn:
    text: "+"
    rightOf: "Produk Reguler"
```

```yaml
- tapOn:
    id: "btn_add"
    below: "Kategori Sembako"
```

### 1.4 Coordinate Points (Strict Rules)
Coordinate points (`point: "50%, 77%"`) should **only** be used when:
1. Interacting with a custom numeric PIN pad or signature canvas that lacks accessibility nodes.
2. Tapping outside a modal dialog to dismiss the backdrop.
3. Performing specialized gestures.

Whenever coordinates are necessary, express them in percentage strings (`"95%, 16%"`) rather than absolute pixels, ensuring stability across different emulator resolutions.

