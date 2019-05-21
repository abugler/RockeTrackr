import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import new_addition
import cleanup
import change_detection

"""Authentication"""
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets'
    ,"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

SpreadSheet = client.open_by_key("1aiCgR4WLJ158oFP6uj61B0pftav3zxtSrL6bWUPVQog")
InventorySheet = SpreadSheet.worksheet("Inventory")
TrackingHistory = SpreadSheet.worksheet("Inventory Tracking History")
RemovalHistory = SpreadSheet.worksheet("Inventory Removal History")
AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")
MovingHistory = SpreadSheet.worksheet("Moving Locations History")

def CleanAll():
    print("Starting Cleanup")
    cleanup.cleanup_rows(TrackingHistory)
    print("1/5 Cleanup Complete")
    cleanup.cleanup_rows(RemovalHistory)
    print("2/5 Cleanup Complete")
    cleanup.cleanup_rows(AdditionHistory)
    print("3/5 Cleanup Complete")
    cleanup.cleanup_rows(MovingHistory)
    print("4/5 Cleanup Complete")
    cleanup.cleanup_rows(InventorySheet)
    print("Finished Cleanup")


OldAdditionData = AdditionHistory.get_all_records()

cleanup_counter = 240
print("Sheet Scraping Cycle Beginning")
while True:
    # check every 30 seconds, and hopefully Google Sheets API doesn't scream
    time.sleep(30)
    print("Now we check!")

    # Handle Addition
    # find the changed rows
    changed = change_detection.changed_rows(OldAdditionData, AdditionHistory.get_all_records())

    # If a history has been cleared, don't do anything
    if AdditionHistory.row_count < 3:
        print("Addition Sheet is Empty. Maybe cause it got recently cleared :(")
    elif changed:  # if rows are changed, something has been added
        for row in changed:
            new_addition.new_addition(AdditionHistory, InventorySheet, row)
            print("Items added to inventory!")
    else:
        print("No addition requests submitted")

    # every 2 hours wipe the empty rows out
    if cleanup_counter == 0:
        CleanAll()
        cleanup_counter = 240
    else:
        cleanup_counter = cleanup_counter - 1

    # Load old data for a later comparison
    OldAdditionData = AdditionHistory.get_all_records()
    AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")