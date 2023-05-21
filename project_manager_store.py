import os
from google_sheets_helper import (
    get_or_create_user_spreadsheet,
    get_or_create_project_sheet,
    write_data_to_sheet,
    read_data_from_sheet,
)

drafts_folder_path = os.path.join(os.getcwd(), "drafts")
folder_id = "1heJkgPaR4eFGgY1GsaEqNLWV086Dumfd"
user_name = "Marco Paret"
project_name = "Weight Loss"

def store_drafts_data(project_sheet_id, drafts_folder_path):
    file_names = [
        "draft_summary.txt",
        "book_title.txt",
        "draft_text.txt",
        "target_public.txt",
        "best_questions.txt",
        "best_questions_2.txt",
        "keywords.txt",
        "Structure.txt",
    ]

    data = []
    for file_name in file_names:
        file_path = os.path.join(drafts_folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        data.append(content)

    # Read config.json from the root folder
    config_file_path = os.path.join(os.getcwd(), "config.json")
    with open(config_file_path, "r", encoding="utf-8") as f:
        config_content = f.read()
    data.append(config_content)

    # Check if a project with the same book title already exists
    book_title = data[1]
    existing_projects = read_data_from_sheet(project_sheet_id, "B2:B")
    row_to_update = None

    if existing_projects is None:
        existing_projects = []



    for index, row in enumerate(existing_projects):
        if row[0] == book_title:
            row_to_update = index + 2
            break

    if row_to_update is None:
        # If the project doesn't exist, create a new one
        row_to_update = len(existing_projects) + 2

    for index, content in enumerate(data):
        # Write the file content to the corresponding cell in the project sheet
        write_data_to_sheet(project_sheet_id, f"{chr(65 + index)}2", [[content.strip()]])

# Get or create the user's spreadsheet
user_spreadsheet_id = get_or_create_user_spreadsheet(user_name, folder_id)

# Get or create the project sheet within the user's spreadsheet
sheet_name = f"{user_name} - {project_name}"
project_sheet_id = get_or_create_project_sheet(user_spreadsheet_id, project_name)

# Store the draft data in the project sheet
store_drafts_data(project_sheet_id, drafts_folder_path)
