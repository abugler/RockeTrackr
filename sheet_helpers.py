"""
Returns the row number of the next blank row.
It is assumed that a blank row will not have anything in the first column.
"""
def next_blank_row(spreadsheet):
    newrow = 1
    ACells = spreadsheet.range('A1:A'+str(spreadsheet.row_count))
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
    SKUS = worksheet.range("A15:A"+str(worksheet.row_count))
    for SKUCell in SKUS:
        if int(SKUCell.value) == int(SKU):
            return worksheet.acell("B"+str(SKUCell.row))
    return False