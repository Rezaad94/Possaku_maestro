var q = parseInt(qty);
var p = parseInt(price);

// Read optional discount inputs
var item_disc_val = (typeof itemDiscount !== 'undefined') ? parseInt(itemDiscount) : 0;
var item_disc_type = (typeof itemDiscountType !== 'undefined') ? itemDiscountType : "nominal";
var tx_disc_val = (typeof txDiscount !== 'undefined') ? parseInt(txDiscount) : 0;
var tx_disc_type = (typeof txDiscountType !== 'undefined') ? txDiscountType : "nominal";

// 1. Calculate unit price after item discount
var unit_price = p;
if (item_disc_val > 0) {
    if (item_disc_type === "percentage") {
        unit_price = p - (p * item_disc_val / 100);
    } else {
        unit_price = p - item_disc_val;
    }
}

// 2. Calculate subtotal
var subtotal = q * unit_price;

// 3. Calculate final total after transaction discount
var total = subtotal;
if (tx_disc_val > 0) {
    if (tx_disc_type === "percentage") {
        total = subtotal - (subtotal * tx_disc_val / 100);
    } else {
        total = subtotal - tx_disc_val;
    }
}

function formatRupiah(amount) {
    var str = amount.toString();
    var result = "";
    var count = 0;
    for (var i = str.length - 1; i >= 0; i--) {
        result = str.charAt(i) + result;
        count++;
        if (count % 3 === 0 && i !== 0) {
            result = "." + result;
        }
    }
    return "Rp" + result;
}

output.expectedTotal = formatRupiah(total);
output.rawTotal = total.toString();
output.expectedSubtotal = formatRupiah(subtotal);

// The original subtotal before any discounts is q * p
var total_discount = (q * p) - total;
if (total_discount > 0) {
    output.expectedDiscount = "(" + formatRupiah(total_discount) + ")";
} else {
    output.expectedDiscount = "Rp0";
}

// Format the item description line (e.g. 2Pcs x Rp12.000)
output.expectedItemLine = q.toString() + "Pcs x " + formatRupiah(p);
