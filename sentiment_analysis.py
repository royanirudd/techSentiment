import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(comments):
    try:
        # Download necessary NLTK data
        nltk.download('vader_lexicon', quiet=True)

        sia = SentimentIntensityAnalyzer()

        results = []
        for comment in comments:
            sentiment_scores = sia.polarity_scores(comment)
            sentiment = 'positive' if sentiment_scores['compound'] > 0 else 'negative' if sentiment_scores['compound'] < 0 else 'neutral'
            results.append({'comment': comment, 'sentiment': sentiment, 'score': sentiment_scores['compound']})

        logging.info(f"Sentiment analysis completed for {len(comments)} comments")
        return results

    except Exception as e:
        logging.error(f"An error occurred during sentiment analysis: {str(e)}")
        return []
