# Possaku Mobile Automation Framework

> **Automated End-to-End Testing Suite for Possaku Android Point of Sale (`com.cloudiex.possaku`)**  
> Powered by **Maestro CLI**, **Page Object Model (POM)**, and **Playwright-Style HTML Reporting**.

[![Maestro](https://img.shields.io/badge/Maestro-2.x-blue.svg)](https://maestro.mobile.dev)
[![Platform](https://img.shields.io/badge/Platform-Android%2011%20%7C%20emulator--5554-green.svg)](https://developer.android.com)
[![Architecture](https://img.shields.io/badge/Architecture-Page%20Object%20Model%20(POM)-orange.svg)](AGENTS.md)
[![Reporting](https://img.shields.io/badge/Reporting-Playwright--Style%20HTML-22c55e.svg)](reports/)

---

## 📋 Table of Contents
1. [Overview](#-overview)
2. [Architecture & Directory Structure](#-architecture--directory-structure)
3. [Prerequisites & Setup](#-prerequisites--setup)
4. [Running Tests](#-running-tests)
5. [Playwright-Style Test Reporting](#-playwright-style-test-reporting)
6. [Feature Modules Covered](#-feature-modules-covered)
7. [Test Standards & AI Directives](#-test-standards--ai-directives)
8. [Continuous Integration (GitHub Actions)](#-continuous-integration-github-actions)

---

## 🎯 Overview
This repository contains the complete automated mobile regression testing framework for the **Possaku** Android application. Tests are authored using declarative Maestro YAML flows and clean JavaScript Page Objects, enabling rapid, robust, and headless execution on Android emulators and real devices.

### Key Highlights
- **100% Page Object Model (POM)**: Complete separation of UI locators (`pages/`) from test assertions and scenarios (`flows/`).
- **Risk-Based Testing (RBT)**: Prioritized test classification (`smoke`, `regression-p0`, `regression-p1`, `regression-p2`).
- **Playwright-Style HTML Reports**: Rich, self-contained HTML test reports featuring live filtering, search (`/`), per-step execution logs, and full-screen lightbox screenshot galleries.
- **Single Source of AI Directives**: Standardized guidelines and semantic memory bank documented in [AGENTS.md](AGENTS.md).

---

## 🏗 Architecture & Directory Structure

```text
Possaku_maestro/
├── README.md                                    # Project documentation & quick start
├── AGENTS.md                                    # Canonical AI directive, architecture & RBT rules
├── .agents/                                     # Machine intelligence & knowledge base
│   ├── rules/                                   # Enforced Maestro rules & naming conventions
│   ├── skills/maestro/                          # Maestro automation reference manuals
│   └── memory/                                  # Semantic memory (UI locators, domain rules, failure fixes)
├── config/
│   └── env.yaml                                 # Test environment variables, app credentials & App ID
├── pages/                                       # Page Object Model Layer (Locators, JS helpers & subflows)
│   ├── login/                                   # Authentication locators & ensure_logged_in subflow
│   ├── kasir/                                   # Catalog, variant picker, cart & tender locators
│   ├── dashboard/                               # Overview KPI cards & date filter locators
│   ├── usahaku/                                 # Shift management (Buka/Tutup Usaha) locators
│   ├── daftar_pelanggan/                        # Customer directory & debt locators
│   ├── daftar_pesanan/                          # Order list, status filter & queue locators
│   ├── keuangan/                                # Financial books & expense locators
│   ├── atur_produk/                             # Product catalog CRUD & variant locators
│   └── lain_lain/                               # Menu Lain-Lain per-feature Page Objects
│       ├── cetak_struk/                         # Receipt printing & discount locators
│       ├── toko_online/                         # Online store share link & hours locators
│       ├── daftar_karyawan/                     # Employee management & payslip locators
│       └── multi_usaha/                         # Branch store management locators
├── flows/                                       # Executable Test Scenario Flows
│   ├── login/
│   ├── kasir/
│   ├── dashboard/
│   ├── usahaku/
│   ├── daftar_pelanggan/
│   ├── daftar_pesanan/
│   ├── keuangan/
│   ├── atur_produk/
│   └── lain_lain/                               # Per-feature scenario subdirectories
│       ├── cetak_struk/                         # 4 flows (smoke, product, discount, preview)
│       ├── toko_online/                         # 3 flows (link/QR, settings, store)
│       ├── daftar_karyawan/                     # 2 flows (management, salary/payslip/offline)
│       └── multi_usaha/                         # 3 flows (branch setup, modules, cashier/delete/addon)
├── test_plans/                                  # Comprehensive feature test plans (.md)
│   └── lain_lain/                               # Test plans for Lain-Lain features
├── reports/                                     # Self-contained Playwright-style HTML test reports
├── inject_steps.py                              # Report enricher & Playwright HTML generator
├── run_detailed_test.sh                         # Primary test runner script with reporting
└── run_suite.sh                                 # Batch test runner script
```

---

## ⚡ Prerequisites & Setup

### 1. Requirements
- **macOS** or **Linux**
- **Android SDK & ADB**: Target device or Android Emulator running Android 11 (`emulator-5554`)
- **Node.js** (v18+)
- **Python** (v3.9+)
- **Maestro CLI** (v2.x):
  ```bash
  curl -FsSL "https://get.maestro.mobile.dev" | bash
  ```

### 2. Verify Connected Device
Ensure the Android emulator or device is running and visible via ADB:
```bash
adb devices
# Output:
# List of devices attached
# emulator-5554    device
```

### 3. Environment & Credential Configuration
Credentials and environment configurations follow a hierarchical priority:

1. **Base Configuration**: [config/env.yaml](file:///Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro/config/env.yaml)
   ```yaml
   APP_ID: "com.cloudiex.possaku"
   ```
2. **Local Overrides (Ignored by Git)**: Copy the template to `config/env.local.yaml`:
   ```bash
   cp config/env.example.yaml config/env.local.yaml
   ```
   Add personal phone number or PIN without committing credentials to Git:
   ```yaml
   PHONE_NUMBER: "081234567890"
   PIN: "222222"
   ```
3. **Dynamic Script Resolution**: [pages/login/login_credential.js](file:///Users/reza/Documents/Reza/PossakuAuto/Possaku_maestro/pages/login/login_credential.js) dynamically resolves phone numbers to both Indonesian formats (`08...` and `+628...`) and binds to CLI `-e PHONE_NUMBER=...` or CI secrets automatically with standard fallbacks.

---

## 🚀 Running Tests

### Run a Single Flow with Detailed Playwright Report
Execute any individual flow using `./run_detailed_test.sh`. The script runs Maestro with debug output, captures step logs and screenshots, and generates a rich HTML report:

```bash
# Toko Online Link & QR Flow
./run_detailed_test.sh flows/lain_lain/toko_online/toko_online_link_qr_flow.yaml reports/toko_online_link_qr_report.html

# Multi Usaha Branch Setup Flow
./run_detailed_test.sh flows/lain_lain/multi_usaha/multi_usaha_branch_flow.yaml reports/multi_usaha_branch_report.html

# Daftar Karyawan Salary & Payslip Flow
./run_detailed_test.sh flows/lain_lain/daftar_karyawan/karyawan_salary_payslip_flow.yaml reports/karyawan_salary_payslip_report.html
```

### Run an Entire Feature Directory
```bash
./run_detailed_test.sh flows/kasir/
```

### Run Full Regression Suite
Runs the multi-flow regression suite defined in `.maestro/regression_suite.yaml` (or an optional target directory) and generates the **exact same detailed Playwright-style HTML report** with per-step actions and screenshots:
```bash
# Run default full regression suite (all core flows) -> reports/regression_suite_report.html
./run_suite.sh

# Run a specific feature directory via suite runner
./run_suite.sh flows/lain_lain/multi_usaha/
```

### Re-Polish Existing Reports to Playwright Format
To re-render all HTML reports in `reports/` with the latest Playwright UI styling:
```bash
python3 inject_steps.py --repolish-all
```

### Network Safety Guard & Restoring Internet
All test runner scripts (`run_detailed_test.sh`, `run_suite.sh`) enforce an automatic network guard (`trap ensure_online EXIT INT TERM`). This ensures Airplane Mode is always turned **OFF** and Wi-Fi/cellular data are re-enabled both before and after test execution—even if a flow fails or is aborted mid-test.

To manually restore network connectivity on the emulator at any time:
```bash
./restore_internet.sh
```

---

## 📊 Playwright-Style Test Reporting

All test runs generate self-contained HTML reports styled identically to **Playwright Test Runner**:

- **Playwright Navbar (`#18181b`)**: Displays suite title, test status pills, execution duration, and localized timestamps.
- **Instant Search (`/`)**: Live text filtering across test case names, tags, and actions.
- **KPI Dashboard**: Cards for Total Test Cases, Passed, Failed, Pass Rate (%), Total Actions, and Target Device.
- **Tabs inside each flow**:
  - **`Steps` Tab**: Collapsible test cases (`# [PREFIX-XX]`) showing discrete action calls (`tap`, `fill`, `expectVisible`, etc.) with monospace locators and execution durations.
  - **`Screenshots` Tab**: Interactive gallery with click-to-zoom Lightbox modal and <kbd>Esc</kbd> dismissal.
  - **`Metadata & Info` Tab**: Complete run properties (Device, App ID, Flow file path, Start Time).

---

## 📱 Feature Modules Covered

| Module | Sub-Features & Test Scenarios | Status | Test Plan |
| :--- | :--- | :--- | :--- |
| **Kasir (POS)** | Catalog search, variant picker, quantity stepper, cart calculations, discounts, payment tenders (Cash, QRIS). | ✅ 100% Passed | [kasir_comprehensive_test_plan.md](test_plans/kasir_comprehensive_test_plan.md) |
| **Dashboard** | Overview cards (Total Penjualan, Transaksi, Produk), date filter (Hari ini, Minggu ini, Bulan ini), shift alerts. | ✅ 100% Passed | [dashboard_comprehensive_test_plan.md](test_plans/dashboard_comprehensive_test_plan.md) |
| **Atur Produk** | Product catalog CRUD, variant creation, category management, product search & sort. | ✅ 100% Passed | [atur_produk_comprehensive_test_plan.md](test_plans/atur_produk_comprehensive_test_plan.md) |
| **Daftar Pelanggan** | Customer CRUD, customer debt inquiry, debt settlement (at once / by transaction), offline mode. | ✅ 100% Passed | [daftar_pelanggan_comprehensive_test_plan.md](test_plans/daftar_pelanggan_comprehensive_test_plan.md) |
| **Daftar Pesanan** | Order status filters (All, Paid, Unpaid), period filters, queue reset, print receipt & bill. | ✅ 100% Passed | [daftar_pesanan_comprehensive_test_plan.md](test_plans/daftar_pesanan_comprehensive_test_plan.md) |
| **Keuangan** | Saku Utama & Saku Lainnya (Pro), Laporan Penjualan, Laba Rugi, Pajak, Hutang, Voucher, Pengeluaran. | ✅ 100% Passed | [keuangan_comprehensive_test_plan.md](test_plans/keuangan_comprehensive_test_plan.md) |
| **(Lain-Lain) Cetak Struk** | Catalog product, custom product, quantity adjustment, transaction/item discounts, receipt preview, print. | ✅ 100% Passed | [cetak_struk_comprehensive_test_plan.md](test_plans/lain_lain/cetak_struk/cetak_struk_comprehensive_test_plan.md) |
| **(Lain-Lain) Toko Online** | Copy store link, share link, update phone number, operating hours & days, view QR code. | ✅ 100% Passed | [toko_online_comprehensive_test_plan.md](test_plans/lain_lain/toko_online/toko_online_comprehensive_test_plan.md) |
| **(Lain-Lain) Daftar Karyawan** | Employee CRUD, view salary toggle, activate/deactivate, camera/gallery payslip upload, PIN change, add-on, offline mode. | ✅ 100% Passed | [daftar_karyawan_comprehensive_test_plan.md](test_plans/lain_lain/daftar_karyawan/daftar_karyawan_comprehensive_test_plan.md) |
| **(Lain-Lain) Multi Usaha (Pro)** | Branch store creation, first employee setup, quota paywall handling, branch module switching, cashier login, branch deletion inspection. | ✅ 100% Passed | [multi_usaha_comprehensive_test_plan.md](test_plans/lain_lain/multi_usaha/multi_usaha_comprehensive_test_plan.md) |
| **Riwayat** | Category tabs (Semua, Online Order, Penjualan, Pengeluaran, Angsuran Hutang, QRIS, Transfer, Batal, Debit/Kredit), period/invoice search, online order accept/reject, receipt print/share, transaction cancellation & stock replenishment check. | ✅ 100% Passed | [riwayat_comprehensive_test_plan.md](test_plans/riwayat_comprehensive_test_plan.md) |
| **Usahaku** | Store status (Buka/Tutup), store profile edits, tax activation/deactivation, QRIS/bank account management, custom receipt personalization & preview, business tag curation. | ✅ 100% Passed | [usahaku_comprehensive_test_plan.md](test_plans/usahaku_comprehensive_test_plan.md) |

---

## 📜 Test Standards & AI Directives

All test authoring and maintenance must strictly adhere to the rules defined in **[AGENTS.md](AGENTS.md)**:

1. **Test Case ID Prefix Standard**: Every test case step comment must declare its formal test ID (`# [PREFIX-XX] <Title>`) so `inject_steps.py` groups actions accurately.
2. **Page Object Model**: Never hardcode selectors inside flows; always import and reference `pages/<module>/<module>_page.js`.
3. **No Brittle Delays**: Never use hardcoded sleeps; rely on Maestro's conditional waiting and `assertVisible`.
4. **Semantic Memory**: Consult `.agents/memory/ui-locators/` and `.agents/memory/failure-patterns/` for established selectors and reliable workarounds.

---

## 🚀 Continuous Integration (GitHub Actions)

This framework is optimized to run seamlessly in **GitHub Actions CI/CD** pipelines.

### Workflow Configuration: `.github/workflows/maestro_regression.yml`

The workflow automatically:
1. Provisions an **Android 11 (API level 30)** hardware-accelerated headless emulator using `reactivecircus/android-emulator-runner@v2` on **Linux (`ubuntu-latest`)** with KVM hardware acceleration.
2. Restores network connectivity using `restore_internet.sh` before and after test execution.
3. Installs Maestro CLI and injects credentials dynamically via environment variables / GitHub Secrets.
4. Executes the targeted flow or regression suite via `./run_suite.sh`.
5. Enriches execution data with Playwright-style step-by-step reports using `inject_steps.py`.
6. Generates a rich **Markdown Step Summary** in the GitHub Actions run summary via `generate_ci_summary.py`.
7. Uploads the complete HTML test report (with embedded base64 screenshots) to **Workflow Artifacts** (`maestro-playwright-report`).

### Configuring GitHub Secrets
Add the following secrets under **Settings > Secrets and variables > Actions**:
- `POSSAKU_PHONE_NUMBER`: Phone number used to log into the test environment.
- `POSSAKU_PIN`: 6-digit PIN code used for authentication.

### Manual Workflow Dispatch (Interactive Dropdown & CLI)
When running the workflow manually from the GitHub UI (**Actions > Maestro Mobile Test Automation > Run workflow**), an interactive **Target Flow dropdown** is provided:
- **Full Suite**: `.maestro/regression_suite.yaml` (All 50 flows across all modules)
- **Module Folders**: `flows/kasir/`, `flows/dashboard/`, `flows/atur_produk/`, `flows/lain_lain/`, etc.
- **Individual Scenarios**: Select any specific `.yaml` test flow from the list.

You can also trigger it from the command line using the GitHub CLI:
```bash
# Run the full regression suite (Default)
gh workflow run maestro_regression.yml -f target_flow=".maestro/regression_suite.yaml"

# Run a specific feature module
gh workflow run maestro_regression.yml -f target_flow="flows/kasir/"

# Run an individual scenario with an external APK from Google Drive
gh workflow run maestro_regression.yml \
  -f target_flow="flows/lain_lain/toko_online/toko_online_link_qr_flow.yaml" \
  -f apk_url="https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing"
```

> [!NOTE]
> **Google Drive Requirements**:
> If providing a Google Drive link, ensure the file sharing setting is set to **"Anyone with the link can view"** (public access). The workflow's `download_apk.sh` automatically bypasses virus scan confirmation prompts and validates the APK binary before installation.
