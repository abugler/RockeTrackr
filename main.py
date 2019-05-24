import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import new_addition
import cleanup
import change_detection

import new_removal
import move_location

import borrow_or_return

"""
DONE: Checking out items
DONE: Moving items
TODO: Slack Notifications
TODO: Color coding/email/slack when qty is low
TODO: Multiple Items input
TODO: Instructions for contact
    - Lambda
    - FERPA
    - General Understanding of how it works
    - Limits of Google Sheets API
TODO: Draft List of Materials/Tools
TODO: Delete Inventory Row
"""

"""Authentication"""
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets'
    , "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
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
OldRemovalData = RemovalHistory.get_all_records()
OldMoveData = MovingHistory.get_all_records()
OldTrackingData = TrackingHistory.get_all_records()


cleanup_counter = 240
print("Sheet Scraping Cycle Beginning")
while True:

    # check every 30 seconds, and hopefully Google Sheets API doesn't scream
    time.sleep(30)

    # check every 100 seconds, and hopefully Google Sheets API doesn't scream
    time.sleep(100)
    AdditionData = AdditionHistory.get_all_records()
    AdditionChanged = change_detection.changed_rows(OldAdditionData, AdditionData)
    OldAdditionData = AdditionData
    AdditionData = SpreadSheet.worksheet("Inventory Addition History")

    print("Now we check!")

    # Handle Addition
    # find the changed rows
    AdditionData = AdditionHistory.get_all_records()
    AdditionChanged = change_detection.changed_rows(OldAdditionData, AdditionData)
    AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")
    OldAdditionData = AdditionData


    InventorySheet = SpreadSheet.worksheet("Inventory")
    # If a history has been cleared, don't do anything
    if AdditionHistory.row_count < 3:
        print("Addition Sheet is Empty. Maybe cause it got recently cleared :(")
    elif AdditionChanged:  # if rows are changed, something has been added
        for row in AdditionChanged:
            new_addition.new_addition(AdditionHistory, InventorySheet, row + 1)
            print("Items added to inventory!")
    else:
        print("No addition requests submitted")

        # This is for removal

    # Handle Removal
    # find the removed rows
    RemovalData = RemovalHistory.get_all_records()
    RemovalChanged = change_detection.changed_rows(OldRemovalData, RemovalData)
    RemovalHistory = SpreadSheet.worksheet("Inventory Removal History")
    OldRemovalData = RemovalData

    InventorySheet = SpreadSheet.worksheet("Inventory")
    if RemovalHistory.row_count < 3:
        print("Removal Sheet is Empty. Maybe cause it got recently cleared :(")
    elif RemovalChanged:  # if rows are changed, something has been added
        for row in RemovalChanged:
            new_removal.new_removal(RemovalHistory, InventorySheet, row + 1)
            print("Items removed from inventory!")
    else:
        print("No removal requests submitted")

    MoveData = MovingHistory.get_all_records()
    MovingChanged = change_detection.changed_rows(OldMoveData, MoveData)
    MovingHistory = SpreadSheet.worksheet("Moving Locations History")
    OldMoveData = MoveData

    InventorySheet = SpreadSheet.worksheet("Inventory")
    if MovingHistory.row_count < 3:
        print("Moving Sheet is Empty. Maybe cause it got recently cleared :(")
    elif MovingChanged:  # if rows are changed, something has been added
        for row in MovingChanged:
            move_location.move_location(MovingHistory, InventorySheet, row + 1)
            print("Items moved in inventory!")
    else:
        print("No move requests submitted")

    TrackingData = TrackingHistory.get_all_records()
    TrackingChanged = change_detection.changed_rows(OldTrackingData, TrackingData)
    TrackingData = SpreadSheet.worksheet("Inventory Tracking History")
    OldTrackingData = TrackingData

    if TrackingData.row_count < 3:
        print("Tracking Sheet is Empty. Maybe cause it got recently cleared :(")
    elif TrackingChanged:  # if rows are changed, something has been added
        for row in TrackingChanged:
             borrow_or_return.borrow_return(TrackingHistory, InventorySheet, row)
    else:
        print("No tracking requests submitted")

    # every 2 hours wipe the empty rows out
    if cleanup_counter == 0:
        CleanAll()
        cleanup_counter = 240
    else:
        cleanup_counter = cleanup_counter - 1