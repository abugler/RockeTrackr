"""
Returns the row number of the next blank row.
It is assumed that a blank row will not have anything in the first column.
"""
def next_blank_row(sheet):
    newrow = 1
    ACells = sheet.range('A:A')
    while True:
        if ACells[newrow - 1] is None:
            print(newrow)
            break
        newrow = newrow + 1
        print(newrow)
    return newrow