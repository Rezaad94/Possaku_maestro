# Failure Pattern: Android Soft Keyboard Obstruction & Flutter Modals

- **Symptom**: Bottom action buttons (`Simpan`, `Bayar`, `Terapkan`, `Bayar Nanti`) are obscured by the soft keyboard, `inputText` drops characters during sheet rebuilds, or `hideKeyboard` unexpectedly exits the modal/screen.
- **Root Cause**: Possaku (Flutter) dynamically rebuilds bottom sheets when fields gain focus, and Android `hideKeyboard` dispatches `KEYCODE_BACK` if the IME is closed or transitioning.

---

## Verified Resolutions

### 1. Prefer `pressKey: "enter"` Over `hideKeyboard` on Bottom Sheets
Calling `hideKeyboard` when focus failed or after `enter` already closed the IME sends `KEYCODE_BACK` and pops the bottom sheet or exits Cart/Kasir:
```yaml
- inputText: "1000"
- pressKey: "enter"
```

### 2. Two-Tap Focus Pattern for Rebuilding Flutter Bottom Sheets
`Edit Produk Keranjang`, `Diskon Transaksi`, and `Voucher` swap into a compact focus-only widget tree on first tap, moving the `EditText` to a new coordinate. Always tap twice (initial position &rarr; rebuilt position) before `inputText`:
```yaml
# Edit Produk Keranjang
- tapOn:
    point: "${output.kasir_page.itemEditAmountInputPoint}" # 540,1175
- tapOn:
    point: "540,1487" # Rebuilt compact EditText
- inputText: "1000"
- pressKey: "enter"
```

### 3. Full-Screen Modal `Tutup` Backdrop Trap
Flutter `Konfirmasi` alerts (`Info Pajak Anda berhasil diperbarui`, `Masalah koneksi`) wrap `[0,63][1080,1794]` in their accessibility node. Matching `".*Tutup.*"` taps the center backdrop (`540,928`) instead of the button. Target the blue `Tutup` button explicitly at `point: "540,1160"`.

### 4. `Buat Pelanggan` Keyboard Obstruction
When typing `Nama Lengkap` (`540,755`), the sticky `Simpan` footer covers `Nomor handphone`. Press `enter` before tapping `Nomor handphone` (`540,980`).
