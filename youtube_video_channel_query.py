from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from googleapiclient.discovery import build
import os

# Create the Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set the logger to handle INFO and DEBUG logs as well
logging.basicConfig(level=logging.DEBUG)

api_key = os.getenv('YOUTUBE_API_KEY')  # you should replace it with your actual API key
youtube = build('youtube', 'v3', developerKey=api_key)

@app.route('/api/video', methods=['POST', 'OPTIONS'])
def video_api():
    if request.method == 'OPTIONS':
        # This is an example response to an OPTIONS request.
        # You should modify it according to your application's requirements.
        response = app.make_default_options_response()
        # Allow cross-origin requests from any domain.
        # Adjust this if you want to limit which domains can access your API.
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    logging.info("function: video_api")
    try:
        logging.info("Received video API request")
        query = request.json['query']  # extract the query
        logging.info(f'Searching videos for "{query}"...')
        
        # Perform search
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=1,
            type="video",
            channelId="UCnaiNHRkcrbw6WQ9s9pVgBA"  # replace with your channel id
        ).execute()

        video_url = ''
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                video_id = search_result["id"]["videoId"]
                video_url = f'https://www.youtube.com/watch?v={video_id}'
        logging.info(f'URL is "{video_url}"')
        
        return jsonify({'video_url': video_url})
    except Exception as e:
        logging.error(f"Error searching for videos for '{query}': {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(port=5003)
