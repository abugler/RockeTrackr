import unittest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sheet_helpers
import new_addition

class TestingMethods(unittest.TestCase):

    # InventorySheet = SpreadSheet.worksheet("Inventory")
    # TrackingHistory = SpreadSheet.worksheet("Inventory Tracking History")
    # RemovalHistory = SpreadSheet.worksheet("Inventory Removal History")
    # AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")
    # MovingHistory = SpreadSheet.worksheet("Moving Locations History")

    def get_spread_sheet(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)

        return client.open_by_key("1aiCgR4WLJ158oFP6uj61B0pftav3zxtSrL6bWUPVQog")

    def test_next_row(self):
        InventorySheet = self.get_spread_sheet().worksheet("Inventory")
        #This test case has to be changed over time
        self.assertTrue(sheet_helpers.next_blank_row(InventorySheet) is 71)

    def test_add_restock(self):
        # get spreadsheets
        Spreadsheet = self.get_spread_sheet()
        InventorySheet = Spreadsheet.worksheet("Inventory")
        AdditionSheet = Spreadsheet.worksheet("Inventory Addition History")

        # find the row
        newrow = 4;
        SKU = AdditionSheet.cell(newrow, 7).value
        SKUCells = InventorySheet.range('A15:A'+str(InventorySheet.row_count))
        blank_row = sheet_helpers.next_blank_row(InventorySheet)
        for cell in SKUCells:
            if cell.row >= blank_row:
                self.assertTrue(False)
            if int(cell.numeric_value) == int(SKU):
                editingrow = cell.row
                break
        initial_quantity = int(InventorySheet.cell(editingrow, 3).value)

        new_addition.new_addition(AdditionSheet, InventorySheet, newrow)
        self.assertTrue(initial_quantity == (int(InventorySheet.cell(editingrow, 3).value) -
                                             int(AdditionSheet.cell(newrow, 8).value)))

if __name__ == '__main__':
    unittest.main()