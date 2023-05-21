# create_articles_from_google_sheet.py
import json
from google_sheets_helper import read_data_from_sheet
from create_drupal_article import create_drupal_article

def create_articles_from_google_sheet(sheet_id, range_name):
    # Load the configuration data
    with open("publishing_config.json", "r") as config_file:
        config = json.load(config_file)

    # Retrieve Drupal credentials
    drupal_username = config["drupal"]["username"]
    drupal_password = config["drupal"]["password"]

    # Get the session token
    session_token = get_session_token(drupal_username, drupal_password)
    if session_token is None:
        print("Failed to authenticate with Drupal. Aborting.")
        return

    # Read the article data from the Google Sheet
    article_data = read_data_from_sheet(sheet_id, range_name)

    # Create articles on the Drupal site using the article data
    for row in article_data:
        title, content, language_code = row
        create_drupal_article(title, content, language_code, session_token)



