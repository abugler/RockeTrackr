import time

"""
This function edits the InventorySheet, using the New Row from the AdditionSheet
This should be called for every new row in the AdditionSheet
"""
def new_addition(AdditionSheet, InventorySheet, newrow):
    sel = str(AdditionSheet.cell(newrow, 6).value)
    if str(AdditionSheet.cell(newrow, 6).value) == 'Adding a new item':
        #Find next SKU using Location
        Location = AdditionSheet.cell(newrow, 5).value
        ItemCells = InventorySheet.range('B1:B14')
        NextSKUCell = None
        for cell in ItemCells:
            if Location == cell.value:
                NextSKUCell = cell
        SKU = InventorySheet.cell(NextSKUCell.row, 6).value

        # Add New Row
        InventorySheet.append_row([
            int(SKU),
            AdditionSheet.cell(newrow, 3).value,
            int(AdditionSheet.cell(newrow, 4).value),            int(AdditionSheet.cell(newrow, 4).value),
            Location
        ])

    elif str(AdditionSheet.cell(newrow, 6).value) == 'Restocking an item':
        nextrow = None

        # Find the row corresponding with the SKU
        SKU = AdditionSheet.cell(newrow, 7).value
        SKUCells = InventorySheet.range('A15:A'+str(InventorySheet.row_count))
        for cell in SKUCells:
            if int(cell.value) == int(SKU):
                nextrow = cell.row
                break
        if not nextrow:
            AdditionSheet.update_cell(newrow, 7, "INVALID SKU, INVENTORY SHEET NOT CHANGED")
            # TODO: send the user an email if the SKU is invalid
            return  # SKU not found, abort process

        # Update Rows
        InventorySheet.update_cell(nextrow, 3,
                                   int(InventorySheet.cell(nextrow, 3).value)
                                   + int(AdditionSheet.cell(newrow, 8).value))
        InventorySheet.update_cell(nextrow, 4,
                                   int(InventorySheet.cell(nextrow, 4).value)
                                   + int(AdditionSheet.cell(newrow, 8).value))