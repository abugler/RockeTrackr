import gspread

def cleanup_rows(sheet):
    row = sheet.row_count
    while row > 1:
        if sheet.cell(row, 1) is None:
            sheet.delete_row(row)
        row = row - 1
