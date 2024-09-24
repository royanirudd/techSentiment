import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def analyze_sentiment(comments):
    try:
        # Download necessary NLTK data
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)

        sia = SentimentIntensityAnalyzer()
        stop_words = set(stopwords.words('english'))

        results = []
        for comment in comments:
            sentiment_scores = sia.polarity_scores(comment)
            sentiment = 'positive' if sentiment_scores['compound'] > 0 else 'negative' if sentiment_scores['compound'] < 0 else 'neutral'
            
            # Extract keywords
            words = word_tokenize(comment.lower())
            keywords = [word for word in words if word.isalnum() and word not in stop_words]

            results.append({
                'comment': comment,
                'sentiment': sentiment,
                'score': sentiment_scores['compound'],
                'keywords': keywords[:5]  # Top 5 keywords
            })

        logging.info(f"Sentiment analysis completed for {len(comments)} comments")
        return results

    except Exception as e:
        logging.error(f"An error occurred during sentiment analysis: {str(e)}")
        return []
