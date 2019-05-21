NUSTARS Inventory Management

While this script is running, it will scrape the form history spreadsheets of the NUSTARS garage, and change the values on the NUSTARS Inventory Spreadsheet accordingly. 

To use, you will need to set up a new project with the Google Cloud Services, and enable the Google Drive and Google Sheets APIs. You will also need to generate Credentials for the Google Drive API, name it 'creds.json', and add it to this folder. The credentials will provide an email, and you should share the Inventory Sheet with that email.