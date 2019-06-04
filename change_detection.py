"""
This function detects whether or not a change was detected between the two instances of a spreadsheet
If no change is detected, False is returned
If a change is detected, and List of changed rows will be returned
"""
def changed_rows(OldRecords, NewRecords):
    # Make an empty array to hold the list of rows that are in the new records but not in the old.
    list_of_rows = []

    # Checks to see if the length of old records is less than new records. If not, that means nothing has changed.
    if len(OldRecords) < len(NewRecords):
        # We are making row start at 2 to account for the fact that the first row is the labels and arrays in computer
        # science start with 0 and in real life, it starts with 1.
        row = 2
        # We are making a while loop to check through each item in the new records to see which rows are new.
        while row - 2 < len(NewRecords):
            # NewRow is a boolean variable that is True if it is a new row or not and False otherwise.
            NewRow = True
            # Checks each item in the old records to compare with a given item in new records to check if the that
            # new record is in the old records. If it is, then it is not a new row and the boolean gets changed to
            # false.
            for dict in OldRecords:
                # Compares by checking the time stamps
                if NewRecords[row - 2]["Timestamp"] == dict["Timestamp"]:
                    NewRow = False
            # If it is a new row, then we should add it to the list of new rows that we are returning.
            if NewRow:
                list_of_rows.append(row)
            # Adds one to the row variable to compare the next variable in the new records.
            row = row + 1

    # If there is nothing in the list of rows, we will be returning False to symbolize that there is no change.
    # Or else, we are returning the list of rows with items in it.
    if not list_of_rows:
        return False
    return list_of_rows
