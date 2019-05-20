"""
Returns the row number of the next blank row.
It is assumed that a blank row will not have anything in the first column.
"""
def next_blank_row(spreadsheet):
    newrow = 1
    ACells = spreadsheet.range('A1:A'+str(spreadsheet.row_count))
    while True:
        if not ACells[newrow - 1].value:
            break
        newrow = newrow + 1
    return newrow