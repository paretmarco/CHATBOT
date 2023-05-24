# web_app.py - its goal is to connect to google sheet

from flask import Flask, render_template, request, jsonify
import requests
import time
import uuid
from flask_caching import Cache
import redis
import logging
import json
import os
from flask import Flask
from flask_cors import CORS
from celery_worker import process_request, app as celery_app  # Import the Celery task and instance

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Set the log file path depending on the OS
log_dir = "logs"
log_file = "web_app.log"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if os.name == "nt":  # Windows
    log_path = os.path.join(log_dir, log_file)
else:
    log_path = f'/{os.path.join(log_dir, log_file)}'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_path, mode='a'), logging.StreamHandler()])

app = Flask(__name__)
redis_url = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379')  # Default to localhost if no env var
cache = Cache(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': redis_url})

# Now, If you want to run it on a server like Digital Ocean, you just have to set the CACHE_REDIS_URL environment variable to the correct URL before starting your application. You can set it in the command line like this: bash export CACHE_REDIS_URL=redis://your_redis_server_url:6379/0 Replace 'redis://your_redis_server_url:6379/0' with the actual Redis URL for your server. set CACHE_REDIS_URL=redis://64.226.96.78:6379/0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()

    # Check if 'user_input' key is present in the request data
    if 'user_input' not in data:
        logging.error("Missing 'user_input' key in request data")
        return jsonify({"status": "error", "message": "Missing 'user_input' key in request data"}), 400

    user_input = data['user_input']
    user_uuid = str(uuid.uuid4())

    logging.info(f"Submit request received: {user_input}")

    cache_key = f"{user_input}"
    cached_response = cache.get(cache_key)

    if cached_response is not None:
        logging.info(f"Cache hit for: {cache_key}")
        return jsonify({"status": "completed", "response": cached_response})

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
            logging.info(f"Parsed request JSON: {data}")
            return json_response  # Return the parsed JSON object
        except Exception as e:
            logging.error(f"Error during external script request: {e}")
            raise

    from celery_worker import process_request

    # Offload the processing to the Celery worker
    response_text = process_request.delay(user_input)
    logging.info(f"Received response from process_request: {response_text}")
    cache.set(cache_key, response_text, timeout=None)
    cache.set(user_uuid, response_text, timeout=None)
    logging.info(f"Cache miss, storing result for: {cache_key}")
    return jsonify({"status": "submitted", "uuid": user_uuid})

@app.route('/api/check_status', methods=['POST'])
def check_status():
    data = request.get_json()
    user_uuid = data["uuid"]

    logging.info(f"Check status request received: {user_uuid}")

    task_id = cache.get(user_uuid)  # Get the task ID from cache
    if task_id is None:
        return jsonify({"status": "not_found"})

    task = celery_app.AsyncResult(task_id)  # Use AsyncResult on Celery instance, not on task function

@app.route('/test')
def test():
    return "Test route is working!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
