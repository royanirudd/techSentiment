import os
import logging
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def perform_eda(sentiment_results, product):
    try:
        base_output_dir = 'output'
        score_dir = os.path.join(base_output_dir, 'score')
        distribution_dir = os.path.join(base_output_dir, 'distribution')
        wordcloud_dir = os.path.join(base_output_dir, 'wordCloud')

        create_directory(score_dir)
        create_directory(distribution_dir)
        create_directory(wordcloud_dir)

        sentiments = [result['sentiment'] for result in sentiment_results]
        sentiment_counts = Counter(sentiments)

        # Sentiment Distribution Bar Chart
        plt.figure(figsize=(10, 6))
        plt.bar(sentiment_counts.keys(), sentiment_counts.values())
        plt.title(f'Sentiment Distribution for {product}')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        filename = f"{product.replace(' ', '_')}_SentimentDistribution.png"
        plt.savefig(os.path.join(distribution_dir, filename))
        plt.close()

        # Sentiment Score Histogram
        scores = [result['score'] for result in sentiment_results]
        plt.figure(figsize=(10, 6))
        plt.hist(scores, bins=20, edgecolor='black')
        plt.title(f'Sentiment Score Distribution for {product}')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        filename = f"{product.replace(' ', '_')}_ScoreDistribution.png"
        plt.savefig(os.path.join(score_dir, filename))
        plt.close()

        # Word Cloud
        all_keywords = [keyword for result in sentiment_results for keyword in result['keywords']]
        
        # Remove product name and its variations from keywords
        product_words = set(product.lower().split())
        filtered_keywords = [word for word in all_keywords if word.lower() not in product_words]
        
        if filtered_keywords:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_keywords))
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Keyword Cloud for {product}')
            filename = f"{product.replace(' ', '_')}_WordCloud.png"
            plt.savefig(os.path.join(wordcloud_dir, filename))
            plt.close()
        else:
            print("No keywords remaining after filtering. Word cloud not generated.")

        # Calculate average sentiment score
        avg_score = sum(result['score'] for result in sentiment_results) / len(sentiment_results)

        print("\nEDA Results:")
        print(f"Total comments analyzed: {len(sentiment_results)}")
        print(f"Positive comments: {sentiment_counts['positive']}")
        print(f"Neutral comments: {sentiment_counts['neutral']}")
        print(f"Negative comments: {sentiment_counts['negative']}")
        print(f"Average sentiment score: {avg_score:.2f}")
        print(f"\nVisualization files have been saved in the following directories:")
        print(f"- Sentiment Distribution: {distribution_dir}")
        print(f"- Score Distribution: {score_dir}")
        print(f"- Word Cloud: {wordcloud_dir}")

        logging.info("EDA completed successfully")

    except Exception as e:
        logging.error(f"An error occurred during EDA: {str(e)}")
