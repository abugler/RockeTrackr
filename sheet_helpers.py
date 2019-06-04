"""
Returns the row number of the next blank row.
It is assumed that a blank row will not have anything in the first column.
"""
def next_blank_row(spreadsheet):
    # We start with row 1.
    newrow = 1
    # We then get a list of all the rows of the first column in that spreadsheet.
    ACells = spreadsheet.range('A1:A'+str(spreadsheet.row_count))
    # We run a loop to check through each row of that first column, when we find the first row that is empty, we return
    # that row number.
    while newrow <= spreadsheet.row_count:
        if not ACells[newrow - 1].value:
            break
        newrow = newrow + 1
    return newrow


"""
Finds the item name from the SKU.
worksheet = gspread worksheet objectc
SKU = int
"""
def find_item_from_sku(worksheet, SKU):
    # Gets a list of SKUs in the worksheet.
    ItemCellsCount = 0
    InventoryRecords = worksheet.get_all_records()
    for row in InventoryRecords:
        if str(row["Name of item"]) == "SKU Generator":
            ItemCellsCount = ItemCellsCount + 1
        else:
            break
    FirstItemRow = ItemCellsCount + 2
    SKUS = worksheet.range("A"+str(FirstItemRow)+":A"+str(worksheet.row_count))
    # Runs a loop through the SKUs to see if a given SKU in the list matches with the one we are finding.
    for SKUCell in SKUS:
        if int(SKUCell.value) == int(SKU):
            # Since we are going through that list, it's the same as going through each row. When we find a match,
            # we take that row (that's the row where the SKUs match) and look at column B, which is the name of the item
            # and we return that.
            return worksheet.acell("B"+str(SKUCell.row))
    # If we can't find a match, that means the SKU that we are looking for isn't in that worksheet and we return false.
    return False