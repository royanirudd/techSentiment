import os
import logging
from dotenv import load_dotenv
from youtube import fetch_youtube_comments
from sentiment_analysis import analyze_sentiment
from eda import perform_eda
from utils import prompt_user

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get YouTube API key
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            raise ValueError("YouTube API key not found in .env file")

        # Prompt user for product
        product = prompt_user()

        # Fetch YouTube comments
        comments = fetch_youtube_comments(api_key, product)

        # Perform sentiment analysis
        sentiment_results = analyze_sentiment(comments)

        # Perform EDA
        perform_eda(sentiment_results)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
