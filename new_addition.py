import time
import slack_notif
import sheet_helpers
"""
This function edits the InventorySheet, using the New Row from the AdditionSheet
This should be called for every new row in the AdditionSheet
"""
def new_addition(AdditionSheet, InventorySheet, NewRowIndex):
    # NewRow has: [TimeStamp(0), Email(1), Name Of Item(2), Qty Added(3), Location(4), Location(5), Restocking/Adding(6), Qty Restocking(7)]
    NewRow = AdditionSheet.range("A"+str(NewRowIndex)+":H"+str(NewRowIndex))
    if str(NewRow[5].value) == 'Adding a new item':
        #Find next SKU using Location
        Location = NewRow[4].value
        ItemCells = InventorySheet.range('B1:B14')
        NextSKUCell = None
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
    elif str(NewRow[5].value) == 'Restocking an item':
        nextrow = None
        # Find the row corresponding with the SKU
        SKU = NewRow[6].value
        SKUCells = InventorySheet.range('A15:A'+str(InventorySheet.row_count))
        for cell in SKUCells:
            if int(cell.value) == int(SKU):
                nextrow = cell.row
                break
        if not nextrow:
            AdditionSheet.update_cell(NewRow, 7, "INVALID SKU, INVENTORY SHEET NOT CHANGED")
            # TODO: send the user an email if the SKU is invalid
            return  # SKU not found, abort process

        # Update Rows
        InventorySheet.update_cell(nextrow, 3,
                                   int(InventorySheet.cell(nextrow, 3).value)
                                   + int(AdditionSheet.cell(NewRowIndex, 8).value))
        InventorySheet.update_cell(nextrow, 4,
                                   int(InventorySheet.cell(nextrow, 4).value)
                                   + int(AdditionSheet.cell(NewRowIndex, 8).value))
        slack_notif.AddedItemPost(NewRow[7].value, sheet_helpers.find_item_from_sku(InventorySheet, SKU).value)