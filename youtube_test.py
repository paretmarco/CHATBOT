import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Create a file handler
handler = logging.FileHandler('youtube_api.log')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logging.getLogger().addHandler(handler)

def is_key_valid(api_key, video_id):
    base_url = "https://www.googleapis.com/youtube/v3"
    endpoint = "/videos"
    
    url = f"{base_url}{endpoint}"
    
    # Define the parameters
    parameters = {
        'part': 'snippet',
        'id': video_id,
        'key': api_key
    }

    try:
        # Make the request
        response = requests.get(url, parameters)
        
        # Check if the request was successful
        if response.status_code == 200:
            logging.info('API key is valid.')
            return True, response.json()
        else:
            logging.error('API key is invalid.')
            return False, None
    except Exception as e:
        logging.error(f'Error occurred while trying to verify the API key: {e}')
        return False, None


# Replace 'YOUR_API_KEY' and 'YOUR_VIDEO_ID' with your actual API key and the video ID you want to get info about.
api_key = 'AIzaSyChU8IUT3fS2lWDnnWVyeIYJbQOP185MFc'
video_id = 'vOI2w-aRBN0'
is_valid, video_info = is_key_valid(api_key, video_id)

if is_valid:
    # Get the title of the video
    title = video_info['items'][0]['snippet']['title']
    logging.info(f'The title of the video is "{title}"')
    print(f'The API key is valid. The title of the video is "{title}"')
else:
    print('The API key is invalid.')
