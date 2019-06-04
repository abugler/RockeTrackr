import sheet_helpers
import slack_notif

def borrow_return(TrackingSheet, InventorySheet, NewRowIndex):
    # NewRow has: [TimeStamp(0), Name(1), SKU(2), Returning/Borrowing(3), ReturningQty(4), BorrowingQty(5), Gmail(6), Return Date(7)]
    # Gets us a row of row number "NewRowIndex" of the fields above.
    NewRow = TrackingSheet.range("A"+str(NewRowIndex)+":"+"H"+str(NewRowIndex))
    # By using the SKU, we find the row number in the inventory sheet of the item that is going to be changed.
    ChangedRow = sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[2].value))

    # If changed row isn't a number by now, that means we weren't able to find a row with that given SKU. That means the
    # SKU is invalid and the process should be aborted.
    if not ChangedRow:
        TrackingSheet.update_cell(NewRowIndex, 3, "INVALID SKU, INVENTORY SHEET UNCHANGED")
        return
    # Check if the intention of the user is to return an item.
    if str(NewRow[3].value) == 'Returning':
        # Finds the sum of how many items there currently is and how many they are returning.
        EndValue = int(InventorySheet.cell(ChangedRow, 4).value) + int(NewRow[4].value)
        # Find the quantity of that given item that exists in total (currently in stock and being borrowed).
        MaxValue = int(InventorySheet.cell(ChangedRow, 3).value)
        # The EndValue shouldn't be greater the the MaxValue because you can't return an item such that the total is
        # more than what already exists. So, we make sure the EndValue isn't more than the MaxValue.
        if EndValue > MaxValue:
            EndValue = MaxValue
        # We update the quantity of the item to be whatever the EndValue turns out to be.
        InventorySheet.update_cell(ChangedRow, 4, EndValue)
        # Confirm to the user that they have successfully returned an item.
        slack_notif.ReturnPost([1].value, NewRow[3].value,
                               sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[2].value)).value)
    # Check if the intention of the user is to borrow an item.
    elif str(NewRow[3].value) == 'Borrowing':
        # Finds how many items there will be when they check out the item.
        EndValue = int(InventorySheet.cell(ChangedRow, 4).value) - int(NewRow[5].value)
        # The number of items there will be should not be less than 0 because that is not possible, so we will make it
        # equal to zero is it ever goes less than zero.
        if EndValue < 0:
            EndValue = 0
        # We update the quantity of the item to be whatever the EndValue turns out to be.
        InventorySheet.update_cell(ChangedRow, 4, EndValue)
        # Confirm to the user that they have successfully checked out an item.
        slack_notif.BorrowPost(NewRow[1].value, NewRow[4].value,
                               sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[2].value)).value, NewRow[7])
