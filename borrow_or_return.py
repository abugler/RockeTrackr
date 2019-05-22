def borrow_return(TrackingSheet, InventorySheet, NewRowIndex):
    NewRow = TrackingSheet.range("A"+str(NewRowIndex)+":"+"H"+str(NewRowIndex))
    ChangedRow = None
    SKUCells = InventorySheet.range("A14:A"+str(InventorySheet.row_count))
    for cell in SKUCells:
        if int(cell.value) == int(NewRow[2].value):  # Compare each SKU cell to SKU
            ChangedRow = cell.row
            break

    if not ChangedRow:
        TrackingSheet.update_cell(NewRowIndex, 3, "INVALID SKU, INVENTORY SHEET UNCHANGED")
        return
    if str(NewRow[3].value) == 'Returning':
        EndValue =  int(InventorySheet.cell(ChangedRow, 4).value) + int(NewRow[4].value)
        MaxValue = int(InventorySheet.cell(ChangedRow, 3).value)
        if EndValue > MaxValue:
            EndValue = MaxValue
        InventorySheet.update_cell(ChangedRow, 4, EndValue)
    elif str(NewRow[3].value) == 'Borrowing':
        EndValue = int(InventorySheet.cell(ChangedRow, 4).value) - int(NewRow[5].value)
        if EndValue < 0:
            EndValue = 0
        InventorySheet.update_cell(ChangedRow, 4, EndValue)