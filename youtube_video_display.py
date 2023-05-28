from flask import Flask, jsonify, request
from llama_index import GPTSimpleVectorIndex
from flask_cors import CORS
import logging

# Create the Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set the logger to handle INFO and DEBUG logs as well
logging.basicConfig(level=logging.DEBUG)

# Load the youtube video index
# Loading the index:
logging.info('Loading index…')
index = GPTSimpleVectorIndex.load_from_disk('youtube_video_index/directory_index.json')

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
        
        # Perform similarity search
        response = index.query(query, similarity_top_k=2, verbose=True)
        sources = response.get_formatted_sources(length=200)
        video_url = response
        print(video_url)
        print(sources)
     
        if video_url:
            logging.info(f'URL is "{video_url}"')
        else:
            video_url = ''
        
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
