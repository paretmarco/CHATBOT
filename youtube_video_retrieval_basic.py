import os
import googleapiclient.discovery
import google_sheets_helper as gsh

def fetch_and_store_video_info(api_key, channel_id, sheet_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Fetch basic information about the videos in the channel
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50
    )
    response = request.execute()

    # Store the video information into a list
    video_info = []
    for item in response['items']:
        if item['id']['kind'] == "youtube#video":
            video_title = item['snippet']['title']
            video_url = "https://www.youtube.com/watch?v=" + item['id']['videoId']
            published_date = item['snippet']['publishedAt']
            video_info.append([published_date, video_title, video_url])

    # Write the video information into the Google Sheet
    gsh.write_data_to_sheet(sheet_id, 'Sheet1!A1', video_info)

api_key = os.getenv('YOUTUBE_API_KEY')
channel_id = "UCnaiNHRkcrbw6WQ9s9pVgBA"  # Replace with your channel id
sheet_id = "1_dQ50_EeFz2X29KiLhEpYl05TzzA1Tx4LcmorCVwG9w"  # Replace with your sheet id

fetch_and_store_video_info(api_key, channel_id, sheet_id)
