output.kasir_page = {
  // Navigation / Dashboard
  kasirMenuButton: "Kasir\\n.*",

  // Catalog / Products
  searchIconPoint: "848,270", // Tap to open search bar
  searchFieldPoint: "477,274", // EditText search field
  searchCloseButton: "Tutup",
  searchFieldHint: "Cari produk",
  scanBarcodeButton: "Scan Barcode",
  customProductButton: "Produk Kostum",
  productRegularText: "BO\\nberas oye\\n1 Varian",
  productRegularTextAlt: "O1\\no1\\nRp12.000\\n1 Varian",
  productDecimalText: "PD\\nproduk desimal\\nRp25.000\\n2 Varian",
  variantReguler: "Reguler.*",
  variantSheetAdd: "Tambahkan",
  variantSheetClose: "Tutup",
  variantSheetQtyMinusPoint: "785,1230",
  variantSheetQtyPlusPoint: "996,1230",
  variantSheetQtyInputPoint: "891,1230",

  // Sorting
  sortButtonPoint: "975,270", // Tap to open sort modal
  sortAlphabetAsc: "Alfabet A-Z",
  sortAlphabetDesc: "Alfabet Z-A",
  sortStockAsc: "Stok Terendah",
  sortStockDesc: "Stok Terbanyak",

  // Categories
  categorySemua: "Semua.*",
  categoryAlatTulis: "Alat Tulis.*",
  categorySembako: "Sembako.*",
  categoryMakananRingan: "Makanan Ringan.*",

  // Custom Product Dialog
  customNameField: "Masukkan Nama Produk",
  customPriceField: "Masukkan Harga",
  customQtyField: "Masukkan Jumlah",
  customSaveButton: "Tambah",

  // Cart
  cartButtonRegex: "Keranjang.*",
  cartItemPlusPoint: "953,354",
  cartItemMinusPoint: "744,354",
  cartItemQtyInputPoint: "849,354",
  cartItemSwipeStart: "900,354",
  cartItemSwipeEnd: "200,354",
  cartItemEditPencilPoint: "808,354",
  cartItemDeleteTrashPoint: "954,354",
  cartTopTrashPoint: "980,137",
  cartTopCustomerPoint: "754,137",
  cartBottomDiscountPoint: "169,1667",
  cartBottomQueuePoint: "423,1667",
  cartAddItemButton: "\\+ Tambah Produk",
  cartPayButton: "Bayar",

  // Discount & Voucher Sheet
  discountTabDiskon: "Diskon",
  discountTabVoucher: "Voucher",
  discountNominalButton: "Nominal",
  discountPersenButton: "Persen",
  discountInputPoint: "540,1487",
  discountApplyButton: "Terapkan",
  voucherInputField: "Tentukan kode voucher",
  voucherCheckButton: "Cek Kode",

  // Item Edit Sheet (from swipe pencil)
  itemEditSheetTitle: "Edit Produk Keranjang",
  itemEditNominalPoint: "300,929",
  itemEditPersenPoint: "784,929",
  itemEditAmountInputPoint: "540,1175",
  itemEditApplyButton: "Terapkan",

  // Customer Sheet
  customerSearchField: "Cari pelanggan",
  customerAddButton: "Tambah Pelanggan Baru",
  customerDrawerAddPoint: "996,660",
  customerFormTitle: "Buat Pelanggan",

  // Queue / Booked (BO)
  queueBayarSekarang: "Bayar Sekarang",
  queueBayarNanti: "Bayar Nanti",

  // Payments Screen
  payMethodTunai: "Tunai",
  payMethodHutang: "Hutang",
  payMethodDebitCredit: "Debit/Kredit",
  payMethodQrisTransfer: "QRIS/Transfer",
  payExactCashButton: "Uang Pas",
  payExcessCashButton: "Rp50.000",
  payExcessCashSuggestion100: "Rp100.000",
  payFinishButton: "Bayar",
  paySuccessButton: "Pembayaran Berhasil",

  // Date Picker
  dateSelector: ".*202[0-9].*",
  dateTargetBackDatePoint: "255,1164", // 10 Nov
  dateApplyButton: "Terapkan",

  // Receipt / Struk
  receiptTitle: "Transaksi Sukses",
  receiptCloseButton: "Transaksi Baru",
  receiptPrintButton: "Pilih Printer",

  // Tax Settings (Usahaku -> Atur Pajak)
  usahakuTabButton: "Usahaku\\n.*",
  homeTabButton: "Home\\n.*",
  pajakMenuRegex: "Pajak.*",
  pajakSwitchPoint: "985,231",
  pajakPercentInputPoint: "540,349",
  pajakSaveButton: "Simpan",

  // Customer Directory (Daftar Pelanggan)
  daftarPelangganMenu: "Daftar\\nPelanggan",
  tambahPelangganButton: "Tambahkan Pelanggan",
  customerNameFieldPoint: "540,700",
  customerPhoneFieldPoint: "540,990",
  customerSaveButton: "Simpan"
};

output.kasir_utils = {
  parseRp: function(str) {
    var m = String(str).match(/Rp\s*([0-9.]+)/);
    if (!m) return 0;
    return parseInt(m[1].replace(/\./g, ''), 10) || 0;
  },
  formatRpRegex: function(num) {
    var s = Math.round(num).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return "Rp" + s.replace(/\./g, '\\.');
  },
  parseCount: function(str) {
    var m = String(str).match(/(\d+)/);
    return m ? parseInt(m[1], 10) : 0;
  },
  getBackDateInfo: function() {
    var d = new Date();
    var targetDay = d.getDate() > 1 ? d.getDate() - 1 : 1;
    var monthsId = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"];
    var mm = ("0" + (d.getMonth() + 1)).slice(-2);
    var dd = ("0" + targetDay).slice(-2);
    var yyyy = d.getFullYear();
    return {
      pickerPattern: "^" + targetDay + ", .*",
      shortDateRegex: targetDay + " " + monthsId[d.getMonth()] + ".*",
      receiptDateRegex: dd + "/" + mm + "/" + yyyy + ".*"
    };
  }
};
