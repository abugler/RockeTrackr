"""
This function detects whether or not a change was detected between the two instances of a spreadsheet
If no change is detected, False is returned
If a change is detected, and List of changed rows will be returned
"""
def changed_rows(OldRecords, NewRecords):
    row = len(OldRecords)
    list_of_rows = []

    # i'm literally just checking length
    # while row < len(NewRecords):
    #    list_of_rows.append(row)
    #    row = row + 1

    # checking length is stupid, instead we should check the actual items
    if len(OldRecords) < len(NewRecords):
        row = 2
        while row - 1 < len(NewRecords):
            NewRow = True
            for dict in OldRecords:
                if NewRecords[row - 1]["Timestamp"] == dict["Timestamp"]:
                    NewRow = False
            if NewRow:
                list_of_rows.append(row)
            row = row + 1

    if not list_of_rows:
        return False;
    return list_of_rows
