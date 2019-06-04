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
    row = sheet.row_count
    while row > 2:
        time.sleep(1)  # Wait a second, so Sheets API doesn't reeee at me
        if not sheet.cell(row, 1).value:
            sheet.delete_row(row)
            print("Row " + str(row) + " is deleted")
        row = row - 1
