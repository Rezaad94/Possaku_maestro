# Domain Intelligence: Cart & Checkout Calculations

- **Domain**: Transaction Totals, Discounts & Tender Rules
- **Context**: Possaku Point of Sale System (`com.cloudiex.possaku`)

---

## 1. Transaction Math Formula

$$\text{Final Total} = \sum (\text{Qty}_i \times \text{Price}_i - \text{Discount}_{\text{item}, i}) - \text{Discount}_{\text{order}} + \text{Tax}$$

- **Line Item Discount**: Accessed by swiping left on a cart item (`83%,19%` &rarr; `18%,19%`) and tapping the green pencil (`808,354`) to open `Edit Produk Keranjang` (`Nominal` or `Persen`). Use `"Hapus Diskon"` to clear before applying another discount.
- **Transaction Discount & Voucher**: Accessed via the bottom-left discount badge (`169,1667`) opening `Tambah Potongan Harga` (`Voucher` / `Diskon`).
- **Tax (`Pajak`)**: Configured globally under `Usahaku -> Atur Pajak` (not inside Cart). When active, Cart displays `*Sudah termasuk pajak` and Checkout displays `Sudah termasuk pajak <X>%`.
- **Dynamic Assertions**: Never hardcode prices, counts, or dates. Read live values via `copyTextFrom` and compute expected totals with `output.kasir_utils` (`parseRp`, `formatRpRegex`, `parseCount`, `getBackDateInfo`).

---

## 2. Cart Quantity & Customer Rules
- **Increment/Decrement**: Use exact stepper points (`953,354` for `+`, `744,354` for `-`), or edit `849,354` and submit via `pressKey: "enter"` so Flutter recalculates `Total`.
- **Line Removal**: Swipe left and tap the red trash button (`954,354`), then confirm `"Ya"` on `Hapus <item> dari keranjang?`. Top-bar trash (`980,137`) clears the entire cart.
- **Customer Selection & Creation**: Tap top-bar Person+ (`754,137`) to open the `Pilih Pelanggan` drawer, tap right-edge `Pilih` (`920,1650`) to select, or tap the `+` icon (`rightOf: "Pilih Pelanggan"`, `above: "Cari pelanggan"`) inside the drawer to create a new customer directly from Kasir.

---

## 3. Tender Methods & Booked Orders
- **Cash (`Tunai`)**: Supports exact (`Uang Pas`), excess suggestion chips (`Rp50.000`), and back-dating via calendar picker.
- **Pay Later / Debt (`Hutang`)**: Requires an attached customer, `Masa Hutang` (e.g. `7` Hari), and `Uang Muka` (e.g. `Rp5.000`), confirmed via `"Selanjutnya"` &rarr; `"Ya"`.
- **Debit/Kredit**: Requires 16-digit card entry (`Masukkan Nomor Kartu`) before `"Pembayaran Berhasil"` activates.
- **QRIS/Transfer**: Completed via `"Pembayaran Berhasil"`; receipt displays payment method as `"TRANSFER"`.
- **Booked BO Orders (`Antrian -> Bayar Nanti`)**: Creates an open pending order in `Daftar Pesanan` and reserves stock under `Terpesan`. Available stock = `Stok - Terpesan`; if 0, adding the product triggers `"Pesanan Anda sudah masuk ke halaman Daftar Pesanan"`.
