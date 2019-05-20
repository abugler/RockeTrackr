import unittest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sheet_helpers

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
        self.assertTrue(sheet_helpers.next_blank_row(InventorySheet) is 68)

if __name__ == '__main__':
    unittest.main()