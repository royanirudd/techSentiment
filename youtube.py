import os
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def read_priority_channels():
    if os.path.exists('channels.txt'):
        with open('channels.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    return []

def fetch_youtube_comments(api_key, product, max_results=150):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        priority_channels = read_priority_channels()
        
        comments = []
        
        # First, search for videos from priority channels
        for channel in priority_channels:
            channel_comments = fetch_channel_comments(youtube, product, channel, max_results - len(comments))
            comments.extend(channel_comments)
            if len(comments) >= max_results:
                break
        
        # If we still need more comments, search for general videos
        if len(comments) < max_results:
            general_comments = fetch_general_comments(youtube, product, max_results - len(comments))
            comments.extend(general_comments)

        logging.info(f"Successfully fetched {len(comments)} comments for {product}")
        return comments

    except HttpError as e:
        logging.error(f"An HTTP error occurred: {str(e)}")
        return []

def fetch_channel_comments(youtube, product, channel, max_results):
    comments = []
    try:
        # Search for videos from the specific channel
        search_response = youtube.search().list(
            q=product,
            type='video',
            channelId=channel,
            part='id,snippet',
            maxResults=10
        ).execute()

        for item in search_response['items']:
            video_id = item['id']['videoId']
            video_comments = fetch_video_comments(youtube, video_id, max_results - len(comments))
            comments.extend(video_comments)
            if len(comments) >= max_results:
                break

    except HttpError as e:
        logging.warning(f"Error fetching comments from channel {channel}: {str(e)}")

    return comments

def fetch_general_comments(youtube, product, max_results):
    comments = []
    try:
        search_response = youtube.search().list(
            q=product,
            type='video',
            part='id,snippet',
            maxResults=10
        ).execute()

        for item in search_response['items']:
            video_id = item['id']['videoId']
            video_comments = fetch_video_comments(youtube, video_id, max_results - len(comments))
            comments.extend(video_comments)
            if len(comments) >= max_results:
                break

    except HttpError as e:
        logging.warning(f"Error fetching general comments: {str(e)}")

    return comments

def fetch_video_comments(youtube, video_id, max_results):
    comments = []
    try:
        comments_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            order='relevance',
            maxResults=min(max_results, 15)
        ).execute()

        for comment in comments_response['items']:
            comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment_text)

    except HttpError as e:
        logging.warning(f"Unable to fetch comments for video {video_id}: {str(e)}")

    return comments
