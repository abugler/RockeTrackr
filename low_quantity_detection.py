import time
"""
Finds the low quantities in the Inventory worksheet, and
sets 'Running Low?' value to yes if the corresponding row in the Low Quantity Worksheet
"""
def low_quantity_checker(InventorySheet, LowQuantitySheet):
    # Get the list of entries in the inventory sheet.
    InventoryRecords = InventorySheet.get_all_records()
    # Get the list of entries in the low quantity sheet.
    LowQuantityRecords = LowQuantitySheet.get_all_records()

    # Initializes the list of SKUs that need to be monitored for if they are running low.
    MonitoredSKUs = [];
    # Initializes the list of entries of items that we need to monitor.
    MonitoredRows = [];
    # Store the SKUs of each item that need to be monitored in the list and store the rows in "Low Quantity" sheet of
    # each entry that needs to be monitored in the list.
    for row in LowQuantityRecords:
        MonitoredSKUs.append(row["SKU"])
        MonitoredRows.append(row)

    # Start with row 2 because row 1 is the column labels of the Inventory sheet. RowIndex keeps track of the row number
    # value of the given item we are looking at in the inventory.
    RowIndex = 2;
    # Runs a loop through each row in the inventory
    for row in InventoryRecords:
        # Checks if the SKU of a given item the in inventory is one of the SKUs that we are monitoring and if the SKU
        # doesn't end with four zeros. We need to check this because an SKU always has a non-zero value for the last
        # four digits, which means an SKU that ends with four zeros doesn't correspond to an item.
        if row["SKU"] in MonitoredSKUs and int(row["SKU"]) % 10000:
            # Runs a loop through all the entries that we are monitoring
            for QuantityRow in MonitoredRows:
                # Checks if a given SKU in the inventory matches with a given SKU in the list of SKUs we are monitoring
                # and if the quantity of the items that we have in the garage is lower than the threshold that we
                # established.
                if QuantityRow["SKU"] == row["SKU"] and int(QuantityRow["Minimum Quantity"]) > int(
                        row["Quantity in garage"]):
                    # Update the sheet to notify people that that given item located in row number "RowIndex" is running
                    # low in quantity.
                    InventorySheet.update_cell(RowIndex, 6, "Yes")
                    # Wait for two seconds so the script doesn't crash.
                    time.sleep(2)
                # Else, that means that the quantity of the items that we have in the garage is not lower than the
                # threshold that we established, but we can only check this if the SKUs match, so the SKUs still need to
                # match
                elif QuantityRow["SKU"] == row["SKU"]:
                    # Update the sheet to notify people that that given item located in row number "RowIndex" is not
                    # running low in quantity.
                    InventorySheet.update_cell(RowIndex, 6, "No")
                    # Wait for two seconds so the script doesn't crash.
                    time.sleep(2)
        # Update the row number, since we are looking at the next item, which is one row number after the one we are
        # currently on.
        RowIndex = RowIndex + 1
