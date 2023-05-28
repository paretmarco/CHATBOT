import os
import time
import googleapiclient.discovery
import google_sheets_helper as gsh

def fetch_and_store_video_info(api_key, channel_id, sheet_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    next_page_token = None
    video_info = []
    while True:
        # Fetch basic information about the videos in the channel
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
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
        for video_item in video_response['items']:
            video_id = video_item['id']
            video_title = video_item['snippet']['title']
            video_url = "https://www.youtube.com/watch?v=" + video_id
            published_date = video_item['snippet']['publishedAt']
            try:
                description = video_item['snippet']['description']
            except KeyError:
                description = ""
            try:
                tags = ",".join(video_item['snippet']['tags'])
            except KeyError:
                tags = ""
            duration = video_item['contentDetails']['duration']
            view_count = video_item['statistics']['viewCount']
            try:
                comment_count = video_item['statistics']['commentCount']
            except KeyError:
                comment_count = '0'
            video_info.append([published_date, video_title, video_url, description, tags, duration, view_count, comment_count])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    # Write the video information into the Google Sheet
    for i, video in enumerate(video_info, start=1):
        gsh.write_data_to_sheet(sheet_id, f'Sheet1!A{i}', [video])
        time.sleep(1)  # wait for 1 second before writing the next video

api_key = os.getenv('YOUTUBE_API_KEY')
channel_id = "UCnaiNHRkcrbw6WQ9s9pVgBA"  # Replace with your channel id
sheet_id = "1_dQ50_EeFz2X29KiLhEpYl05TzzA1Tx4LcmorCVwG9w"  # Replace with your sheet id

fetch_and_store_video_info(api_key, channel_id, sheet_id)