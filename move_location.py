import sheet_helpers
import slack_notif

def move_location(MoveSheet, InventorySheet, NewRowIndex):
    #Newrow: [TimeStamp(0), SKU(1), NewLocation(2), Email(3)
    NewRow = MoveSheet.range("A"+str(NewRowIndex)+":D"+str(NewRowIndex))
    # Gets us the item name that has the SKU in NewRow.
    ItemCell = sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[1]))
    # Gets us the row that has that item name.
    nextrow = ItemCell.row
    if not nextrow:
        MoveSheet.update_cell(NewRowIndex, 2, "INVALID SKU, INVENTORY SHEET NOT CHANGED")
        return  # SKU not found, abort process

    # Find new SKU
    # Change this to reflect new doc info
    # Refer to new addition
    Location = NewRow[2]
    Location_Inventory = InventorySheet.cell(nextrow, 5).value

    # Getting a list of all the possible locations
    # Change this if you are changing the number of locations by adjusting the range to match the cells where you
    # put all the locations in (one cell per location).
    ItemCells = InventorySheet.range('B1:B14')
    # Initializing the variable that will hold the next SKU row number.
    NextSKUCell = None
    # Goes through each location and if there is a match with the location that want to move it to, it will find the
    # cell with that location value in the Inventory Spreadsheet.
    for cell in ItemCells:
        if Location == cell.value:
            NextSKUCell = cell
    # NextSKUCell should NOT be None at this point
    # It will get the new SKU of that moved item by accessing the value of the next available SKU in that row we just
    # found. We need a new SKU because SKU values reflect the location of the item.
    NewSKU = InventorySheet.cell(NextSKUCell.row, 7).value

    # If the locations aren't the same, update that item's SKU and Location. If they are the same, leave it be; nothing
    # needs to be updated
    if Location != Location_Inventory:
        InventorySheet.update_cell(nextrow, 1, NewSKU)
        InventorySheet.update_cell(nextrow, 5, Location)
    slack_notif.MovingPost(ItemCell.value, Location)