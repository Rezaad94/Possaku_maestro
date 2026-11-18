# Comprehensive Test Plan: (Lain - lain) Daftar Karyawan

## 1. Feature Overview
The **Daftar Karyawan** (Employee Directory & Staff Management) module enables business owners to manage store staff, assign role permissions (Kasir/Operator, Supervisor, Order Staff), configure employee salaries, upload payroll slips via camera or gallery, toggle salary visibility in list views, schedule automatic payroll recording into store expenses, manage login PINs, activate or deactivate staff access, purchase employee add-on packages, and operate in offline mode.

---

## 2. Test Architecture & Standards
- **Automation Framework**: Maestro CLI with `run_detailed_test.sh` per-step HTML reporting.
- **Target Device**: Android 11 (`emulator-5554`), App ID: `com.cloudiex.possaku`.
- **Page Object**: `pages/lain_lain/daftar_karyawan_page.js`.
- **Test ID Convention**: `[KARY-XX]`.
- **Assertion Strategy**: Real verification of employee lists, form inputs, bottom sheets, camera/gallery source dialogs, state changes, and offline resilience.

---

## 3. Test Cases Specification

| Test ID | Test Case Name | Preconditions | Test Steps | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[KARY-01]` | Navigasi & Onboarding Daftar Karyawan | User on Dashboard | 1. Tap Lain-Lain.<br>2. Tap Daftar Karyawan.<br>3. Dismiss onboarding guide if present. | Daftar Karyawan screen loads showing search bar, salary toggle, employee list, and FAB (+). | P0 |
| `[KARY-02]` | Search employee | On Daftar Karyawan | 1. Enter existing employee name ("uaua") into search bar.<br>2. Verify matching employee card is displayed.<br>3. Enter non-existent keyword ("zzzz").<br>4. Verify empty state text and "Tambahkan Karyawan" button.<br>5. Clear search. | Filtered list matches query accurately; empty state handles missing records; list restores upon clear. | P0 |
| `[KARY-03]` | View employee salary | On Daftar Karyawan | 1. Toggle switch "Tampilkan daftar gaji karyawan". | Employee card subtitle switches between status ("Aktif"/"Non Aktif") and salary format ("Gaji Bulanan Rp..."). | P1 |
| `[KARY-04]` | Add employee | On Daftar Karyawan | 1. Tap FAB (+).<br>2. Enter Nama Lengkap, Nomor HP, verify default PIN.<br>3. Tap Simpan.<br>4. Confirm "Ya" on dialog. | Employee successfully created, confirmation modal appears with login info, and employee is listed. | P0 |
| `[KARY-05]` | Edit employee | On Detail Karyawan | 1. Tap employee card.<br>2. Tap Update on Informasi Personal.<br>3. Edit employee details and tap Simpan.<br>4. Confirm "Ya". | Updated information is reflected on Detail Karyawan. | P0 |
| `[KARY-06]` | Employee activation | Employee is Non Aktif | 1. Open Detail Karyawan.<br>2. Tap top-right menu (...).<br>3. Tap "Aktifkan Karyawan".<br>4. Confirm "Ya". | Status Karyawan updates to "Aktif". | P0 |
| `[KARY-07]` | Employee deactivation | Employee is Aktif | 1. Open Detail Karyawan.<br>2. Tap top-right menu (...).<br>3. Tap "Non Aktifkan Karyawan".<br>4. Confirm "Ya". | Status Karyawan updates to "Non Aktif". | P0 |
| `[KARY-08]` | Change PIN | On Detail Karyawan | 1. Tap top-right menu (...).<br>2. Tap "Ubah Pin".<br>3. Verify Ubah PIN screen elements.<br>4. Tap Kembali to return. | Ubah PIN screen allows setting and retyping a new 6-digit staff security PIN. | P1 |
| `[KARY-09]` | Upload payslip from camera | Salary nominal configured | 1. Tap top-right menu (...).<br>2. Tap "Upload Slip Gaji".<br>3. Tap "Upload Foto".<br>4. Verify "Kamera" option in Ambil Gambar dialog.<br>5. Tap Kembali/Tutup. | Camera capture intent trigger is verified. | P1 |
| `[KARY-10]` | Upload payslip from gallery | Salary nominal configured | 1. In Ambil Gambar dialog, verify "Gallery" option.<br>2. Tap Kembali/Tutup. | Photo gallery selector intent trigger is verified. | P1 |
| `[KARY-11]` | See detail payslip & Automatic payroll schedule | On Detail Karyawan | 1. Scroll to "Informasi Gaji".<br>2. Verify payslip records.<br>3. Open Update -> verify "Gaji sebagai Pengeluaran Toko" automatic schedule toggle. | Payslip history is viewable and automatic expense recording schedule toggle is accessible. | P1 |
| `[KARY-12]` | Delete Employee | Additional employee exists | 1. Open Detail Karyawan.<br>2. Tap top-right menu (...).<br>3. Tap "Hapus Karyawan".<br>4. Confirm "Ya". | Employee is permanently removed from the directory. | P0 |
| `[KARY-13]` | Buy add on employee | User on Profil tab | 1. Navigate to Profil tab.<br>2. Tap "Paket Add-on".<br>3. Verify addon status modal / subscription options. | Displays active addon status or prompt to subscribe to additional staff seats. | P1 |
| `[KARY-14]` | Offline Mode | On Daftar Karyawan | 1. Enable Airplane mode.<br>2. Verify cached employee directory remains browsable.<br>3. Disable Airplane mode. | App remains functional in offline mode without crashing. | P1 |

---

## 4. Automation Execution Mapping
1. `flows/lain_lain/karyawan_management_flow.yaml`: Covers `[KARY-01]`, `[KARY-02]`, `[KARY-03]`, `[KARY-04]`, `[KARY-05]`, `[KARY-08]`, and `[KARY-12]`.
2. `flows/lain_lain/karyawan_salary_payslip_flow.yaml`: Covers `[KARY-06]`, `[KARY-07]`, `[KARY-09]`, `[KARY-10]`, and `[KARY-11]`.
3. `flows/lain_lain/karyawan_addon_offline_flow.yaml`: Covers `[KARY-13]` and `[KARY-14]`.
