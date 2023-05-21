import json
import requests

def create_drupal_article(title, content, language_code, session_token):
    # Load the configuration data
    with open("publishing_config.json", "r") as config_file:
        config = json.load(config_file)

    # Set up variables based on the configuration data
    base_url = config["drupal"]["base_url"]
    api_endpoint = config["drupal"]["api_endpoint"]

    # Set up the data for the new article
    data = {
        "title": [
            {
                "value": title
            }
        ],
        "body": [
            {
                "value": content,
                "format": "full_html"
            }
        ],
        "type": [
            {
                "target_id": "article"
            }
        ],
        "langcode": [
            {
                "value": language_code
            }
        ]
    }

# get token
def get_session_token(username, password):
    # Load the configuration data
    with open("publishing_config.json", "r") as config_file:
        config = json.load(config_file)

    base_url = config["drupal"]["base_url"]
    auth_url = f"{base_url}/user/login?_format=json"

    credentials = {
        "name": username,
        "pass": password
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(auth_url, json=credentials, headers=headers)

    if response.status_code == 200:
        session_token = response.headers["X-CSRF-Token"]
        return session_token
    else:
        print(f"Failed to authenticate. Response: {response.status_code} {response.text}")
        return None

    # Set up the headers for the request
    headers = {
        "Content-Type": "application/json",
        "X-CSRF-Token": session_token
    }

    # Send the request to create the article
    response = requests.post(f"{base_url}/{api_endpoint}/entity/node", json=data, headers=headers)

    # Check if the article was created successfully
    if response.status_code == 201:
        print(f"Article '{title}' created successfully.")
    else:
        print(f"Failed to create article '{title}'. Response: {response.status_code} {response.text}")
