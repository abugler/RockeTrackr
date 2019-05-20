import gspread
import sheet_helpers

""""""
def new_addition(AdditionSheet, InventorySheet, newrow):


    sel = str(AdditionSheet.cell(newrow, 6).value)
    if str(AdditionSheet.cell(newrow, 6).value) == 'Adding a new item':
        # Find the Next Row in the InventorySheet
        nextrow = sheet_helpers.next_blank_row(InventorySheet)

        #Find next SKU using Location
        Location = AdditionSheet.cell(newrow, 5).value
        ItemCells = InventorySheet.range('A1:A14')
        NextSKUCell = None
        for cell in ItemCells:
            if Location is cell.value:
                NextSKUCell = cell
        SKU = InventorySheet.cell(NextSKUCell.row, 6).value

        # Add New Row
        InventorySheet.insert_row([
            SKU,
            AdditionSheet.cell(newrow, 3),
            AdditionSheet.cell(newrow, 4),
            AdditionSheet.cell(newrow, 4),
            Location
        ], index=newrow)

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
            return  # SKU not found, abort process

        # Update Rows
        InventorySheet.update_cell(nextrow, 3,
                                   int(InventorySheet.cell(nextrow, 3).value)
                                   + int(AdditionSheet.cell(newrow, 8).value))
        InventorySheet.update_cell(nextrow, 4,
                                   int(InventorySheet.cell(nextrow, 4).value)
                                   + int(AdditionSheet.cell(newrow, 8).value))





