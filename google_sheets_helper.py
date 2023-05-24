# google_sheets_helper.py - THIS FILE IS FOR CONNECTING TO GOOGLE SHEET
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import os

# Update the path to the JSON file containing your API key
current_directory = os.path.dirname(os.path.realpath(__file__))
credential_file = os.path.join(current_directory, "complete-agency-270710-4c41875347c4.json")
creds = service_account.Credentials.from_service_account_file(credential_file)
sheets_service = build('sheets', 'v4', credentials=creds)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def write_data_to_sheet(sheet_id, range_name, values):
    try:
        # Additional log
        logging.info(f"Attempting to write to sheet: {sheet_id}")
        # values is expected to be a list of lists
        # Each sub-list is expected to contain two elements: the user_id and the value to write
        body = {
            'values': values
        }
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption='RAW', body=body).execute()
        logging.info(f"{result.get('updatedCells')} cells updated.")
    except HttpError as error:
        logging.error(f"An error occurred: {error}")

def read_data_from_sheet(sheet_id, range_name):
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=range_name).execute()
        return result.get('values', [])
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return None

def create_google_sheet(sheet_title, folder_id):
    # Initialize the Sheets API
    service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Create a new Google Sheet with the specified title
    sheet_metadata = {
        'properties': {'title': sheet_title},
        'sheets': [{'properties': {'title': 'Sheet1', 'sheetType': 'GRID'}}],
    }
    sheet = service.spreadsheets().create(body=sheet_metadata).execute()

    # Move the new Google Sheet to the specified folder
    file_id = sheet['spreadsheetId']
    file = drive_service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    file = drive_service.files().update(fileId=file_id, addParents=folder_id, removeParents=previous_parents, fields='id, parents').execute()

    return file_id

def find_sheet_by_title(sheet_title, folder_id):
    # Initialize the Sheets API
    service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Search for the sheet by title
    query = f"name = '{sheet_title}' and mimeType = 'application/vnd.google-apps.spreadsheet' and '{folder_id}' in parents"
    results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        return None

    return items[0]['id']

def find_sheet_id_by_title(spreadsheet_id, sheet_title):
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet['sheets']
    
    for sheet in sheets:
        if sheet['properties']['title'] == sheet_title:
            return sheet['properties']['sheetId']
    return None

# added in prevision of user managements

def get_or_create_user_spreadsheet(user_name, folder_id):
    spreadsheet_title = f"{user_name} Projects"
    spreadsheet_id = find_sheet_by_title(spreadsheet_title, folder_id)
    if spreadsheet_id is None:
        spreadsheet_id = create_google_sheet(spreadsheet_title, folder_id)
    return spreadsheet_id

def get_or_create_project_sheet(user_spreadsheet_id, project_name):
    # Check if the project sheet exists
    sheet_id = find_sheet_id_by_title(user_spreadsheet_id, project_name)

    if sheet_id is None:
        # Create a new sheet within the user's spreadsheet
        body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': project_name
                        }
                    }
                }
            ]
        }
        sheets_service.spreadsheets().batchUpdate(spreadsheetId=user_spreadsheet_id, body=body).execute()
        # Get the sheet id of the newly created sheet
        sheet_id = find_sheet_id_by_title(user_spreadsheet_id, project_name)

    return sheet_id

def store_drafts_data(project_sheet_id, drafts_folder_path):
    file_names = [
        "best_questions.txt",
        "best_questions_2.txt",
        "book_distribute_faq.py",
        "book_title.txt",
        "draft_summary.txt",
        "draft_text.txt",
        "keywords.txt",
        "Structure.txt",
        "target_public.txt"
    ]

    for index, file_name in enumerate(file_names):
        file_path = os.path.join(drafts_folder_path, file_name)
        with open(file_path, "r") as f:
            content = f.read()

        # Write the file content to the corresponding cell in the project sheet
        write_data_to_sheet(project_sheet_id, f"A{index + 1}", [[content]])