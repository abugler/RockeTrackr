import gspread
from sheet_helpers import *

def new_addition(AdditionSheet, InventorySheet):
    #Find newest row in AdditionSheet
    newrow = next_blank_row(AdditionSheet) - 1

    #Find the Next Row in the InventorySheet
    nextrow = next_blank_row(InventorySheet)

    #Find the Next SKU number to be used
    if AdditionSheet.cell(newrow, 6) is "Adding a new item":
        Location = AdditionSheet.cell(newrow, 5).value
        NextSKUCell = InventorySheet.find(Location)
        SKU = InventorySheet.cell(NextSKUCell.row, 6).value
    elif AdditionSheet.cell(newrow, 6) is "Restocking an item":
        SKU = AdditionSheet.cell(newrow, 7)
        SKUs = InventorySheet.values_get('A:A')
        if SKU not in SKUs:
            return #aborting process if SKU is not found in Inventory Spreadsheet

