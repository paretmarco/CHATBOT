from celery import Celery
import requests
import json
import logging

app = Celery('celery_worker', broker='redis://localhost:6379/0')

@app.task
def process_request(user_input):
    app_script_url = "https://script.google.com/macros/s/AKfycbz16VATRFuVyma_K8wFSSpLeQteUCCslSxG3Km65oRO3EVL0vB3V8jC5psjjC-Yr4Pdqw/exec"
    try:
        logging.info(f"Submitting request to Google Script")
        response = requests.post(app_script_url, json={"user_input": user_input})
        logging.info(f"Response from Google Script: {response.text}")
        if response.text.startswith('<!doctype'):
            raise ValueError("Invalid JSON response received")
        if response.status_code != 200:
            logging.error(f"Unexpected status code from Google Script: {response.status_code}")
            raise ValueError(f"Unexpected status code from Google Script: {response.status_code}")
        json_response = json.loads(response.text)  # Parse the JSON response
        return json_response  # Return the parsed JSON object
    except Exception as e:
        logging.error(f"Error during external script request: {e}")
        raise
