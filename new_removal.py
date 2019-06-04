import slack_notif
import sheet_helpers

"""
This function edits the InventorySheet, using the New Row from the AdditionSheet
This should be called for every new row in the AdditionSheet
"""
def new_removal(RemovalSheet, InventorySheet, newrow):
    # Initialize the variable that gets us the row that has the corresponding SKU in the inventory.
    nextrow = None

    # Get the SKU of the item that we are trying to remove a given quantity of.
    SKU = RemovalSheet.cell(newrow, 3).value
    # Get a list of SKUs that are in the inventory sheet.
    SKUCells = InventorySheet.range('A15:A'+str(InventorySheet.row_count))
    # Runs a loop through each of the SKUs until we get a match. When we do get a match, we save the row number where
    # that SKU is at in the inventory sheet into the variable nextrow.
    for cell in SKUCells:
        if int(cell.value) == int(SKU):
            nextrow = cell.row
            break
    # If there is no match, that means the SKU is invalid and thus, we should abort the process.
    if not nextrow:
        return  # SKU not found, abort process

    # Update the quantity of the item in the garage and overall based on how much of the given item they are
    # removing.
    InventorySheet.update_cell(nextrow, 3,
                                max(0, int(InventorySheet.cell(nextrow, 4).value) -
                                    int(RemovalSheet.cell(newrow, 4).value)))
    InventorySheet.update_cell(nextrow, 4,
                               max(0, int(InventorySheet.cell(nextrow, 4).value) -
                                   int(RemovalSheet.cell(newrow, 4).value)))

    # Send user a notification confirming that we successfully removed their given item.
    slack_notif.RemovalPost(RemovalSheet.cell(newrow, 4).value,
                            sheet_helpers.find_item_from_sku(InventorySheet, int(SKU)).value,
                            RemovalSheet.cell(newrow, 5).value)