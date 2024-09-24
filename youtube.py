import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def fetch_youtube_comments(api_key, product):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        # TODO: Implement comment fetching logic
        # This is a placeholder function
        comments = ["Sample comment 1", "Sample comment 2"]

        logging.info(f"Successfully fetched {len(comments)} comments for {product}")
        return comments

    except HttpError as e:
        logging.error(f"An HTTP error occurred: {str(e)}")
        return []
