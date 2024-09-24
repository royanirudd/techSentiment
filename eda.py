import os
import logging
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, OrderedDict
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
        ordered_sentiments = OrderedDict([('negative', sentiment_counts['negative']),
                                          ('neutral', sentiment_counts['neutral']),
                                          ('positive', sentiment_counts['positive'])])
        colors = ['#FF4136', '#FFDC00', '#2ECC40']  # Red, Yellow, Green
        bars = plt.bar(ordered_sentiments.keys(), ordered_sentiments.values(), color=colors)
        plt.title(f'Sentiment Distribution for {product}')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height}',
                     ha='center', va='bottom')
        filename = f"{product.replace(' ', '_')}_SentimentDistribution.png"
        plt.savefig(os.path.join(distribution_dir, filename))
        plt.close()

        # Sentiment Score Histogram
        scores = [result['score'] for result in sentiment_results]
        plt.figure(figsize=(10, 6))
        n, bins, patches = plt.hist(scores, bins=20, edgecolor='black')
        
        # color map
        cmap = plt.cm.get_cmap('coolwarm')
        # color each bar based on its center
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        # scale values to interval [0,1]
        col = (bin_centers - min(bin_centers)) / (max(bin_centers) - min(bin_centers))
        for c, p in zip(col, patches):
            plt.setp(p, 'facecolor', cmap(c))
        
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
