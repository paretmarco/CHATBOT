import os
import time
import logging
from datetime import datetime, timedelta
import googleapiclient.discovery
import google_sheets_helper as gsh

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')

# Set level of logging
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def fetch_and_store_video_info(api_key, channel_id, sheet_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Authenticate with Google Sheets
    last_row = len(gsh.read_data_from_sheet(sheet_id, "Sheet1")) + 1  # Get the last non-empty row

    # Load the start date from a file
    try:
        with open("last_processed_date.txt", "r") as f:
            end_date = datetime.fromisoformat(f.read().strip())
    except FileNotFoundError:
        logger.error("last_processed_date.txt not found. Using default end_date.")
        end_date = datetime(2018, 12, 30)  # Starting from this day if no file is found

    start_date = end_date - timedelta(days=300)  # Going back 300 days at a time

    while start_date >= datetime(2005, 4, 23):  # Until the launch of YouTube
        next_page_token = None

        while True:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
                publishedAfter=start_date.isoformat("T") + "Z",
                publishedBefore=end_date.isoformat("T") + "Z"
            )
            response = request.execute()

            # Make a list of the video IDs
            video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == "youtube#video"]

            # Fetch additional information about the videos
            video_request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids)
            )
            video_response = video_request.execute()

            # Store the video information into a list
            video_info = []
            for video_item in video_response['items']:
                video_id = video_item['id']
                video_title = video_item['snippet']['title']
                video_url = "https://www.youtube.com/watch?v=" + video_id
                published_date = video_item['snippet']['publishedAt']
                try:
                    description = video_item['snippet']['description']
                except KeyError:
                    logger.warning("Description not found for video: %s", video_id)
                    description = ""
                try:
                    tags = ",".join(video_item['snippet']['tags'])
                except KeyError:
                    logger.warning("Tags not found for video: %s", video_id)
                    tags = ""
                duration = video_item['contentDetails']['duration']
                view_count = video_item['statistics']['viewCount']
                try:
                    comment_count = video_item['statistics']['commentCount']
                except KeyError:
                    logger.warning("Comments not found for video: %s", video_id)
                    comment_count = '0'
                video_info.append([published_date, video_title, video_url, description, tags, duration, view_count, comment_count])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        # Write the video information into the Google Sheet
        for video in video_info:
            gsh.write_data_to_sheet(sheet_id, f'Sheet1!A{last_row}', [video])
            time.sleep(1)  # wait for 1 second before writing the next video
            last_row += 1  # Update the last row

        # Save the start date to a file
        with open("last_processed_date.txt", "w") as f:
            f.write(start_date.isoformat())

        end_date = start_date
        start_date = end_date - timedelta(days=300)

api_key = os.getenv('YOUTUBE_API_KEY')
channel_id = "UCnaiNHRkcrbw6WQ9s9pVgBA"  # Replace with your channel id
sheet_id = "1_dQ50_EeFz2X29KiLhEpYl05TzzA1Tx4LcmorCVwG9w"  # Replace with your sheet id

fetch_and_store_video_info(api_key, channel_id, sheet_id)
