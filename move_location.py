import sheet_helpers
import slack_notif

def move_location(MoveSheet, InventorySheet, NewRowIndex):
    #Newrow: [TimeStamp(0), SKU(1), NewLocation(2), Email(3)
    NewRow = MoveSheet.range("A"+str(NewRowIndex)+":D"+str(NewRowIndex))
    ItemCell = sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[1]))
    nextrow = ItemCell.row
    if not nextrow:
        MoveSheet.update_cell(NewRowIndex, 2, "INVALID SKU, INVENTORY SHEET NOT CHANGED")
        return  # SKU not found, abort process

    # Find new SKU
    # Change this to reflect new doc info
    # Refer to new addition
    Location = NewRow[2]
    Location_Inventory = InventorySheet.cell(nextrow, 5).value


    ItemCells = InventorySheet.range('B1:B14')
    NextSKUCell = None
    for cell in ItemCells:
        if Location == cell.value:
            NextSKUCell = cell
    #NextSKUCell should NOT be None at this point

    NewSKU = InventorySheet.cell(NextSKUCell.row, 7).value

    if Location != Location_Inventory:
        InventorySheet.update_cell(nextrow, 1, NewSKU)
        InventorySheet.update_cell(nextrow, 5, Location)
    slack_notif.MovingPost(ItemCell.value, Location)