import time
"""
Finds the low quantities in the Inventory worksheet, and
sets 'Running Low?' value to yes if the corresponding row in the Low Quantity Worksheet
"""
def low_quantity_checker(InventorySheet, LowQuantitySheet):
    InventoryRecords = InventorySheet.get_all_records()
    LowQuantityRecords = LowQuantitySheet.get_all_records()

    MonitoredSKUs = [];
    MonitoredRows = [];
    for row in LowQuantityRecords:
        MonitoredSKUs.append(row["SKU"])
        MonitoredRows.append(row)

    RowIndex = 2;
    for row in InventoryRecords:
        if row["SKU"] in MonitoredSKUs and int(row["SKU"]) % 10000:
            for QuantityRow in MonitoredRows:
                if QuantityRow["SKU"] == row["SKU"] and int(QuantityRow["Minimum Quantity"]) > int(row["Quantity in garage"]):
                    InventorySheet.update_cell(RowIndex, 6, "Yes")
                    time.sleep(2)
                elif QuantityRow["SKU"] == row["SKU"]:
                    InventorySheet.update_cell(RowIndex, 6, "No")
                    time.sleep(2)
        RowIndex = RowIndex + 1