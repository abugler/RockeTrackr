import gspread
import time

"""
Deletes all empty rows
Be careful with this one
"""
def cleanup_rows(sheet):
    while sheet.row_count > 1000:
        sheet.delete_row(3)
        print("An old row has been deleted")
        time.sleep(1)
    row = sheet.row_count
    # This loop runs until we reach the last two rows, which is just the labels.
    while row > 2:
        time.sleep(1)
        # Wait a second, so Sheets API doesn't crash and throw an error
        # If there is no value in the rows, leave it alone, else delete that row and let the user know that the row
        # is deleted.
        if not sheet.cell(row, 1).value:
            sheet.delete_row(row)
            print("Row " + str(row) + " is deleted")
        # Subtract one to the row to check the next row above.
        row = row - 1

