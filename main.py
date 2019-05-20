import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import new_addition
from cleanup import cleanup_rows

"""Authentication"""
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

SpreadSheet = client.open_by_key("1aiCgR4WLJ158oFP6uj61B0pftav3zxtSrL6bWUPVQog")
InventorySheet = SpreadSheet.worksheet("Inventory")
#TrackingHistory = SpreadSheet.worksheet("Inventory Tracking History")
#RemovalHistory = SpreadSheet.worksheet("Inventory Removal History")
AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")
#MovingHistory = SpreadSheet.worksheet("Moving Locations History")


OldAdditionData = AdditionHistory


while True:
    time.sleep(300)
    """Handle Addition"""
    """If a history has been cleared"""
    if AdditionHistory.row_count < 2:
        OldAdditionData = AdditionHistory
    elif AdditionHistory.row_count > OldAdditionData.row_count:
        new_addition(AdditionHistory)
    else:
        OldAdditionData = AdditionHistory
        AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")


