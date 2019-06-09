import json
import requests
import sheet_helpers
# change this with the webhook_url for the requested slack app
webhook_url = 'https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXx'

def post(json_data):
    # Takes json data, and makes a post request to slack
    # Makes a post request given our url, data, and header.
    response = requests.post(
        webhook_url, data=json.dumps(json_data),
        headers={'Content-Type': 'application/json'}
    )
    # Checks if the request failed or not. If it did, throw an error based on what it is saying.
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

# DONE: Make Slack Notifications a thing for each type

"""
Send a Notification to a Slack App with the most recent borrow.
"""
def BorrowPost(Name, Quantity, Item, ReturnDate):
    # Make a message saying that someone has borrowed an item in JSON data format.
    json_data = {
        "text": str(Name) + " has taken " + str(Quantity) + " " + str(Item) + " from the Garage. " +
                str(Name) + " plans to bring the item back before or on " + str(ReturnDate)
    }
    # Send a notification over to Slack App with the message we just made.
    post(json_data)

"""
Send a Notification to a Slack App with the most recent return.
"""
def ReturnPost(Name, Quantity, Item):
    # Make a message saying that someone has returned an item in JSON data format.
    json_data = {
        "text": str(Name) + " has returned " + str(Quantity) + " " + str(Item) + " from the Garage. Thanks " +
                str(Name) + "!"
    }
    # Send a notification over to Slack App with the message we just made.
    post(json_data)

"""
Send a Notification to a Slack App with the most recent removal.
"""
def RemovalPost(Quantity, Item, Reason):
    # Make a message saying that someone has removed an item in JSON data format.
    json_data = {
        "text": str(Quantity) + " " + str(Item) + " have been removed from the Garage, as they have been " + str(Reason) +"!"
    }
    # Send a notification over to Slack App with the message we just made.
    post(json_data)

"""
Send a Notification to a Slack App with the most recent add.
"""
def AddedItemPost(Quantity, Item):
    # Make a message saying that someone has added an item in JSON data format.
    json_data = {
        "text": str(Quantity) + " " + str(Item) + " have been added to the Inventory."
    }
    # Send a notification over to Slack App with the message we just made.
    post(json_data)

"""
Send a Notification to a Slack App with the most recent move.
"""
def MovingPost(Item, Location):
    # Make a message saying that someone has borrowed an item in JSON data format.
    json_data = {
        "text": str(Item) + " has been moved to " + str(Location)+"."
    }
    # Send a notification over to Slack App with the message we just made.
    post(json_data)

def SendErrorToSlack(ErrorText):
    json_data = {
        "text": ErrorText + "\nIt's likely that the last action you took was not completed. "
    }
    post(json_data)
