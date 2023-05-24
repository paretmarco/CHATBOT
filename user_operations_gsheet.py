# user_operations_gsheet.py
# this file connects to app.py and it is is for saving to gsheet the saved answers
import logging
import google_sheets_helper as gsh

def save_edited_answer(user_email, project_name, answer):
    # Log the input parameters
    logging.info("save_edited_answer() called with user_email: %s, project_name: %s, answer: %s", user_email, project_name, answer)

    # Get or create the user spreadsheet
    user_spreadsheet_id = gsh.get_or_create_user_spreadsheet(user_email)

    # Get or create the project sheet
    project_sheet_id = gsh.get_or_create_project_sheet(user_spreadsheet_id, project_name)

    # Save the edited answer to the sheet
    gsh.save_answer_to_sheet(user_spreadsheet_id, project_sheet_id, answer)
    logging.info("Answer saved to sheet")