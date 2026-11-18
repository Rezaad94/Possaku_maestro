# CI/CD Execution, Step Traceability & Debugging

This guide describes how to run tests, generate enriched HTML reports, and troubleshoot failed Maestro executions.

---

## 1. Test Suite Execution (`run_suite.sh`)

We provide a runner script at the root of the project:
```bash
./run_suite.sh
```

### Script Workflow:
1. Loads environment variables from `config/env.yaml` (e.g. `APP_ID=com.cloudiex.possaku`).
2. Extracts flow files defined in `.maestro/regression_suite.yaml`.
3. Runs Maestro with HTML report and flattened debug outputs:
   ```bash
   maestro test --format html --output report.html --debug-output debug_out --flatten-debug-output $ENV_ARGS $FLOW_FILES
   ```
4. Executes `python3 inject_steps.py` to enrich `report.html` with detailed, per-command executed test steps.
5. Cleans up temporary `debug_out/` artifacts.

---

## 2. Step Traceability via `inject_steps.py`

`inject_steps.py` inspects Maestro's debug execution logs (`debug_out/`) and injects formatted step labels into `report.html`.

### How to Write Flows for Optimal Step Reporting:
Always format step comments cleanly in your YAML flows:
```yaml
# Step 1: Login with valid cashier PIN
- runFlow:
    file: ../../pages/login/login_flow.yaml
    ...

# Step 2: Open Kasir Catalog
- tapOn: "${output.kasir_page.kasirMenuButton}"

# Step 3: Add Regular Product to Cart
- tapOn: "${output.kasir_page.productRegularText}"
```
This enables test engineers and stakeholders to view clear, human-readable step timelines in `report.html`.

---

## 3. Diagnostic Commands

### Check Syntax:
Always pre-validate YAML flows before running full executions:
```bash
maestro check-syntax flows/kasir/catalog_qty_flow.yaml
```

### Inspect Live View Hierarchy:
Print the current screen's UI tree:
```bash
maestro hierarchy
```

### List Connected Emulators/Devices:
```bash
maestro list-devices
```

