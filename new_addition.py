import time
import slack_notif
import sheet_helpers
"""
This function edits the InventorySheet, using the New Row from the AdditionSheet
This should be called for every new row in the AdditionSheet
"""
def new_addition(AdditionSheet, InventorySheet, NewRowIndex):
    # NewRow has: [TimeStamp(0), Email(1), Name Of Item(2), Qty Added(3), Location(4), Location(5), Restocking/Adding(6), Qty Restocking(7)]
    # Gets us a row of row number "NewRowIndex" of the fields above.
    NewRow = AdditionSheet.range("A"+str(NewRowIndex)+":H"+str(NewRowIndex))
    # Check if the intention of the user is to add.
    if str(NewRow[5].value) == 'Adding a new item':
        #Find next SKU using Location
        Location = NewRow[4].value
        # Getting a list of all the possible locations
        # Change this if you are changing the number of locations by adjusting the range to match the cells where you
        # put all the locations in (one cell per location).
        ItemCells = InventorySheet.range('B1:B14')
        NextSKUCell = None

        # Goes through each location and if there is a match with the location that want to move it to, it will find the
        # cell with that location value in the Inventory Spreadsheet.
        for cell in ItemCells:
            if Location == cell.value:
                NextSKUCell = cell
        SKU = InventorySheet.cell(NextSKUCell.row, 7).value

        # Add New Row
        InventorySheet.append_row([
            int(SKU),
            NewRow[2].value,
            int(NewRow[3].value),
            int(NewRow[3].value),
            Location,
            "No"
        ])
        slack_notif.AddedItemPost(NewRow[3].value, NewRow[4].value)

    # Check if the intention of the user is to restock.
    elif str(NewRow[5].value) == 'Restocking an item':
        nextrow = None
        # Find the row corresponding with the SKU
        SKU = NewRow[6].value
        SKUCells = InventorySheet.range('A15:A'+str(InventorySheet.row_count))
        # Loop through each SKU until we found match. When we do find a match, we take the row with the matching SKU in
        # the inventory and store it in nextrow.
        for cell in SKUCells:
            if int(cell.value) == int(SKU):
                nextrow = cell.row
                break
        # If we don't find a match, that is because that SKU doesn't exist in the inventory sheet. So, we will update
        # that restocked row to say that the SKU is invalid
        if not nextrow:
            AdditionSheet.update_cell(NewRow, 7, "INVALID SKU, INVENTORY SHEET NOT CHANGED")
            # We notify the user that they inputted an invalid SKU.
            return  # SKU not found, abort process

        # Update Rows
        InventorySheet.update_cell(nextrow, 3,
                                   int(InventorySheet.cell(nextrow, 3).value)
                                   + int(AdditionSheet.cell(NewRowIndex, 8).value))
        InventorySheet.update_cell(nextrow, 4,
                                   int(InventorySheet.cell(nextrow, 4).value)
                                   + int(AdditionSheet.cell(NewRowIndex, 8).value))
        # Send user a notification confirming that we successfully restocked their given item.
        slack_notif.AddedItemPost(NewRow[7].value, sheet_helpers.find_item_from_sku(InventorySheet, SKU).value)