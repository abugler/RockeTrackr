import sheet_helpers

def move_location(MoveSheet, InventorySheet, newrow):
    nextrow = None

    # Find the row corresponding with the SKU
    SKU = MoveSheet.cell(newrow, 2).value
    SKUCells = InventorySheet.range('A15:A' + str(InventorySheet.row_count))
    for cell in SKUCells:
        if int(cell.value) == int(SKU):
            nextrow = cell.row
            break
    if not nextrow:
        MoveSheet.update_cell(newrow, 2, "INVALID SKU, INVENTORY SHEET NOT CHANGED")
        return  # SKU not found, abort process

    # Find new SKU
    # Change this to reflect new doc info
    # Refer to new addition
    Location = MoveSheet.cell(newrow, 3).value
    Location_Inventory = InventorySheet.cell(nextrow, 5).value

    ItemCells = InventorySheet.range('B1:B14')
    NextSKUCell = None
    for cell in ItemCells:
        if Location == cell.value:
            NextSKUCell = cell
    NewSKU = InventorySheet.cell(NextSKUCell.row, 6).value

    if Location != Location_Inventory:
        InventorySheet.update_cell(nextrow, 1, NewSKU)
        InventorySheet.update_cell(nextrow, 5, Location)