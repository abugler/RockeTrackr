import json
import requests
import sheet_helpers
# change this with the webhook_url for the requested slack app
webhook_url = 'https://hooks.slack.com/services/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'

def post(json_data):
    #  Takes json data, and makes a post request to slack
    response = requests.post(
        webhook_url, data=json.dumps(json_data),
        headers={'Content-Type': 'application/json'}
    )
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
    json_data = {
        "text": str(Name) + " has taken " + str(Quantity) + " " + str(Item) + " from the Garage. " +
                str(Name) + " plans to bring the item back before or on " + str(ReturnDate)
    }
    post(json_data)

def ReturnPost(Name, Quantity, Item):
    json_data = {
        "text": str(Name) + " has returned " + str(Quantity) + " " + str(Item) + " from the Garage. Thanks " +
                str(Name) + "!"
    }
    post(json_data)

def RemovalPost(Quantity, Item, Reason):
    json_data = {
        "text": str(Quantity) +" "+ str(Item) + " have been removed from the Garage, as they have been " + str(Reason) +"!"
    }
    post(json_data)

def AddedItemPost(Quantity, Item):
    json_data = {
        "text": str(Quantity) +" "+ str(Item) + " have been added to the Inventory."
    }
    post(json_data)

def MovingPost(Item, Location):
    json_data = {
        "text": str(Item) + "has been moved to "+ str(Location)+"."
    }
    post(json_data)