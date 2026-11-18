var ts = Date.now().toString().slice(-6);
output.branchName = "Cabang " + ts;
output.branchDesc = "Uji Otomasi Maestro " + ts;
output.branchEmployeeName = "Kasir " + ts;
output.branchEmployeePhone = "087" + Math.floor(100000000 + Math.random() * 900000000).toString();
