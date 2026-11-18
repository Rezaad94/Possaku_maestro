var ts = Date.now().toString().slice(-6);
output.employeeName = "Staf " + ts;
output.employeeNameEdit = "Edit " + ts;
output.employeePhone = "088" + Math.floor(100000000 + Math.random() * 900000000).toString();
