# Failure Pattern: Lazy-Rendering & Off-Screen Elements

- **Symptom**: `assertVisible` or `tapOn` fails on catalog items or customer entries that are lower down the screen, even though they exist in database.
- **Root Cause**: Jetpack Compose `LazyColumn` or Android `RecyclerView` does not render view nodes until they enter the active viewport.

---

## 🛠️ Verified Resolutions

### 1. Programmatic Swipe / Scroll
Scroll down to bring off-screen elements into the hierarchy:
```yaml
- scroll
```
Or targeted directional swipe:
```yaml
- swipe:
    direction: "UP"
```

### 2. Relative Scrolling Until Visible
Scroll toward a specific target:
```yaml
- scrollUntilVisible:
    element:
      text: "Produk Sembako 5"
    direction: "DOWN"
```

### 3. Avoid Fixed Coordinate Swiping
Avoid hardcoded pixel swipes like `swipe: { from: 500, 1000, to: 500, 200 }`. Use percentage swipes or Maestro's directional keywords to preserve device-agnostic execution.

