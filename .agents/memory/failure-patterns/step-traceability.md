# Failure Pattern: Step Traceability & inject_steps.py

- **Symptom**: `report.html` displays generic flow executions without granular step-by-step breakdown or fails to identify which logical action caused a test failure.
- **Root Cause**: YAML flow lacks clear section partitions or `inject_steps.py` cannot correlate raw debug commands with business test steps.

---

## 🛠️ Verified Resolutions

### 1. Mandatory Numbered Step Comments
In every test flow, wrap logical action clusters with numbered step comments:
```yaml
# Step 1: Initialize app and authenticate
- runFlow:
    file: ../../pages/login/login_flow.yaml

# Step 2: Open Kasir catalog and filter Sembako
- tapOn: "${output.kasir_page.kasirMenuButton}"
- tapOn: "${output.kasir_page.categorySembako}"

# Step 3: Add product and verify cart update
- tapOn: "${output.kasir_page.productRegularText}"
- tapOn: "${output.kasir_page.variantSheetAdd}"
- assertVisible: "Keranjang \\(1\\)"
```

### 2. Enable Flattened Debug Output
`run_suite.sh` passes `--debug-output debug_out --flatten-debug-output` to Maestro, which outputs execution logs that `inject_steps.py` parses to build expandable step trees in `report.html`.

