import sheet_helpers
import slack_notif

def borrow_return(TrackingSheet, InventorySheet, NewRowIndex):
    # NewRow has: [TimeStamp(0), Name(1), SKU(2), Returning/Borrowing(3), ReturningQty(4), BorrowingQty(5), Gmail(6), Return Date(7)]
    NewRow = TrackingSheet.range("A"+str(NewRowIndex)+":"+"H"+str(NewRowIndex))
    ChangedRow = None
    ChangedRow = sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[2].value))

    if not ChangedRow:
        TrackingSheet.update_cell(NewRowIndex, 3, "INVALID SKU, INVENTORY SHEET UNCHANGED")
        return
    if str(NewRow[3].value) == 'Returning':
        EndValue = int(InventorySheet.cell(ChangedRow.row, 4).value) + int(NewRow[4].value)
        MaxValue = int(InventorySheet.cell(ChangedRow.row, 3).value)
        if EndValue > MaxValue:
            EndValue = MaxValue
        InventorySheet.update_cell(ChangedRow, 4, EndValue)
        slack_notif.ReturnPost(NewRow[1].value, NewRow[3].value,
                               sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[2].value)).value)
    elif str(NewRow[3].value) == 'Borrowing':
        EndValue = int(InventorySheet.cell(ChangedRow.row, 4).value) - int(NewRow[5].value)
        if EndValue < 0:
            EndValue = 0
        InventorySheet.update_cell(ChangedRow.row, 4, EndValue)
        slack_notif.BorrowPost(NewRow[1].value, NewRow[4].value,
                               sheet_helpers.find_item_from_sku(InventorySheet, int(NewRow[2].value)).value, NewRow[7])
