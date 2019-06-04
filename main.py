# This is the main function of the code that runs all of the checks.
# So, we need to import all the tools we made to do checks.

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import new_addition
import cleanup
import change_detection
import new_removal
import move_location
import borrow_or_return
import low_quantity_detection
import slack_notif

# This is used to let Google know that we aren't accessing a document that we didn't have permission to edit.
"""Authentication"""
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets'
    , "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
key = "1aiCgR4WLJ158oFP6uj61B0pftav3zxtSrL6bWUPVQog"
SpreadSheet = client.open_by_key(key)

# These our all of the sheets we have in our Spreadsheet
InventorySheet = SpreadSheet.worksheet("Inventory")
TrackingHistory = SpreadSheet.worksheet("Inventory Tracking History")
RemovalHistory = SpreadSheet.worksheet("Inventory Removal History")
AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")
MovingHistory = SpreadSheet.worksheet("Moving Locations History")
LowQuantitySheet = SpreadSheet.worksheet("Low Quantities")

# This function deletes all the empty rows in each of the sheets we have in our Spreadsheet
def CleanAll():
    print("Starting Cleanup")
    cleanup.cleanup_rows(TrackingHistory)
    print("1/6 Cleanup Complete")
    cleanup.cleanup_rows(RemovalHistory)
    print("2/6 Cleanup Complete")
    cleanup.cleanup_rows(AdditionHistory)
    print("3/6 Cleanup Complete")
    cleanup.cleanup_rows(MovingHistory)
    print("4/6 Cleanup Complete")
    cleanup.cleanup_rows(InventorySheet)
    print("5/6 Cleanup Complete")
    cleanup.cleanup_rows(LowQuantitySheet)
    print("Finished Cleanup")

# Takes all the row entries that are in each sheet. This is our old data because we will be comparing this data with
# updated data that will be given later in the script.
OldAdditionData = AdditionHistory.get_all_records()
OldRemovalData = RemovalHistory.get_all_records()
OldMoveData = MovingHistory.get_all_records()
OldTrackingData = TrackingHistory.get_all_records()

# This counter is made so that every 4 hours, the code that cleans up the blank rows runs. This is done because the
# rows can cause bugs.
cleanup_counter = 240
seconds_to_wait = 2
print("Sheet Scraping Cycle Beginning")
while True:
    try:
        # check every 100 seconds, and hopefully Google Sheets API doesn't scream
        time.sleep(seconds_to_wait)

        # Let the user know that we are checking updates on any of the sheets.
        print("Now we check!")

        # Handle Addition
        # find the changed rows
        AdditionHistory = SpreadSheet.worksheet("Inventory Addition History")
        AdditionData = AdditionHistory.get_all_records()
        # Find if there is any changed rows in the Addition Sheet. It there is, that means someone filled out the form to
        # add an item and there were items added to the inventory. The Addition Sheet doubles as a history of what people
        # added to the inventory. Changed_addition either results in false if there is nothing that was updated or a list
        # if there are items that are new.
        AdditionChanged = change_detection.changed_rows(OldAdditionData, AdditionData)
        OldAdditionData = AdditionData

        InventorySheet = SpreadSheet.worksheet("Inventory")
        # If a history has been cleared, don't do anything
        if AdditionHistory.row_count < 3:
            print("Addition Sheet is Empty. Maybe cause it got recently cleared :(")
        # This is only true is there are items in the list of new rows. If there are items in the list of new rows, that
        # means rows are changed and something has been added.
        elif AdditionChanged:
            for row in AdditionChanged:
                new_addition.new_addition(AdditionHistory, InventorySheet, row)
                print("Items added to inventory!")
        # If there are no new rows and the history is not cleared that means nothing will be updated.
        else:
            print("No addition requests submitted")

        time.sleep(seconds_to_wait)

        # The logic for checking the spread is roughly the same as the addition checks
        # Handle Removal
        # find the removed rows
        RemovalHistory = SpreadSheet.worksheet("Inventory Removal History")
        RemovalData = RemovalHistory.get_all_records()
        RemovalChanged = change_detection.changed_rows(OldRemovalData, RemovalData)
        OldRemovalData = RemovalData

        InventorySheet = SpreadSheet.worksheet("Inventory")
        if RemovalHistory.row_count < 3:
            print("Removal Sheet is Empty. Maybe cause it got recently cleared :(")
        elif RemovalChanged:  # if rows are changed, something has been added
            for row in RemovalChanged:
                new_removal.new_removal(RemovalHistory, InventorySheet, row)
                print("Items removed from inventory!")
        else:
            print("No removal requests submitted")

        time.sleep(seconds_to_wait)

        MovingHistory = SpreadSheet.worksheet("Moving Locations History")
        MoveData = MovingHistory.get_all_records()
        MovingChanged = change_detection.changed_rows(OldMoveData, MoveData)
        OldMoveData = MoveData

        InventorySheet = SpreadSheet.worksheet("Inventory")
        if MovingHistory.row_count < 3:
            print("Moving Sheet is Empty. Maybe cause it got recently cleared :(")
        elif MovingChanged:  # if rows are changed, something has been added
            for row in MovingChanged:
                move_location.move_location(MovingHistory, InventorySheet, row)
                print("Items moved in inventory!")
        else:
            print("No move requests submitted")

        time.sleep(seconds_to_wait)

        TrackingHistory = SpreadSheet.worksheet("Inventory Tracking History")
        TrackingData = TrackingHistory.get_all_records()
        TrackingChanged = change_detection.changed_rows(OldTrackingData, TrackingData)
        OldTrackingData = TrackingData

        if TrackingHistory.row_count < 3:
            print("Tracking Sheet is Empty. Maybe cause it got recently cleared :(")
        elif TrackingChanged:  # if rows are changed, something has been added
            for row in TrackingChanged:
                 borrow_or_return.borrow_return(TrackingHistory, InventorySheet, row)
        else:
            print("No tracking requests submitted")

        time.sleep(seconds_to_wait)
        # check low_quantities
        InventorySheet = SpreadSheet.worksheet("Inventory")
        LowQuantitySheet = SpreadSheet.worksheet("Low Quantities")
        low_quantity_detection.low_quantity_checker(InventorySheet, LowQuantitySheet)

        # sometime between 3:00am and 4:00am wipe the empty rows out
        if time.struct_time.tm_hour == 3 and cleanup_counter == 0:
            CleanAll()
            cleanup_counter = 240
        else:  # cleanup counter exists so the cleanup is only ran once a day
            cleanup_counter = cleanup_counter - 1
    except gspread.exceptions.CellNotFound:
        error_text = "This is an error.  An cell that was trying to be accessed could not be found."
        print(error_text)
        slack_notif.SendErrorToSlack(error_text)
    except gspread.exceptions.WorksheetNotFound:
        error_text = "This is an error. We tried to access a worksheet that doesn't exist. Did someone accidentally change the name of the worksheet? RockeTracker will wait ten minutes for the spreadsheet names to be changed."
        print(error_text)
        slack_notif.SendErrorToSlack(error_text)
        time.sleep(600)
        spreadsheet = client.open_by_key(key)
    except gspread.exceptions.APIError, Argument:
        error_text = "This is an error. Something happened with the Google Sheets API.  Maybe too many API calls occurred, or maybe Google returned a server error.  It could also be neither of these things.  RockeTracker will wait two minutes for our API calls to replenish, or for Google's servers to go back up.  The details of the error can be found below."
        error_text += "\n"+str(Argument);
        print(error_text)
        slack_notif.SendErrorToSlack(error_text)
        time.sleep(120)
    except gspread.exceptions.GSpreadException, Argument:
        error_text = "This is an error. A generic Gspread error occurred. Below are the details for the error."
        error_text += "\n" + str(Argument)
        slack_notif.SendErrorToSlack(error_text)
        print(error_text)
    except Exception, e:
        error_text = "This is an error.  An error that the developer is not foresee has occurred. The details of the error can be found below."
        error_text += "\n" + str(Argument)
        print(error_text)
        slack_notif.SendErrorToSlack(error_text)

