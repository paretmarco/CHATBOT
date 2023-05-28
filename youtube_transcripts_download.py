import googleapiclient.discovery
import os
import logging
from youtube_transcript_api import YouTubeTranscriptApi

# Set up logging
logging.basicConfig(level=logging.INFO)

def save_transcripts_urls_desc(api_key, channel_id, output_dir, target_num_videos):
    logging.info(f"Using API key: {api_key}")

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    downloaded_count = 0

    next_page_token = None
    while downloaded_count < target_num_videos:
        search_response = youtube.search().list(part="id,snippet", channelId=channel_id, maxResults=50, pageToken=next_page_token).execute()
        videos = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append((search_result["id"]["videoId"], search_result["snippet"]["title"], search_result["snippet"]["description"]))
                
        next_page_token = search_response.get("nextPageToken")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for video_id, video_title, video_description in videos:
            safe_title = "".join([c for c in video_title if c.isalnum() or c.isspace()]).rstrip()
            if os.path.exists(os.path.join(output_dir, f"{safe_title}.txt")):
                continue
            
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])  # assuming English transcripts
                with open(os.path.join(output_dir, f"{safe_title}.txt"), "w") as file:
                    for entry in transcript:
                        file.write(entry['text'] + ' ')
                    file.write('\n\nURL: ' + 'https://www.youtube.com/watch?v=' + video_id)
                    file.write('\n\nDescription: ' + video_description)
                logging.info(f"Transcript, URL, and description saved for {safe_title}")
                downloaded_count += 1

                if downloaded_count >= target_num_videos:
                    break
            except Exception as e:
                logging.error(f"Error fetching transcript for video ID {video_id} ({video_title}): {str(e)}")
        
        if not next_page_token:
            break

api_key = os.getenv('YOUTUBE_API_KEY')
logging.info(f"Retrieved API key: {api_key}")

channel_id = "UCnaiNHRkcrbw6WQ9s9pVgBA"
output_dir = "youtube_transcripts"
target_num_videos = 100

save_transcripts_urls_desc(api_key, channel_id, output_dir, target_num_videos)
