import sheet_helpers

"""
This function edits the InventorySheet, using the New Row from the AdditionSheet
This should be called for every new row in the AdditionSheet
"""
def new_removal(RemovalSheet, InventorySheet, newrow):
        nextrow = None

        # Find the row corresponding with the SKU
        SKU = RemovalSheet.cell(newrow, 3).value
        SKUCells = InventorySheet.range('A15:A'+str(InventorySheet.row_count))
        for cell in SKUCells:
            if int(cell.value) == int(SKU):
                nextrow = cell.row
                break
        if not nextrow:
            return  # SKU not found, abort process

        # Update Rows
        InventorySheet.update_cell(nextrow, 4,
                                   max(0, int(InventorySheet.cell(nextrow, 4).value) - int(RemovalSheet.cell(newrow, 4).value)))