import os
import logging
import matplotlib.pyplot as plt

def perform_eda(sentiment_results, product):
    try:
        sentiments = [result['sentiment'] for result in sentiment_results]
        sentiment_counts = {
            'positive': sentiments.count('positive'),
            'neutral': sentiments.count('neutral'),
            'negative': sentiments.count('negative')
        }

        # Create output directory if it doesn't exist
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(sentiment_counts.keys(), sentiment_counts.values())
        plt.title(f'Sentiment Distribution for {product}')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        
        # Save the chart with the product name in the filename
        filename = f"{product.replace(' ', '_')}_BarChart.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath)
        plt.close()

        # Calculate average sentiment score
        avg_score = sum(result['score'] for result in sentiment_results) / len(sentiment_results)

        print("\nEDA Results:")
        print(f"Total comments analyzed: {len(sentiment_results)}")
        print(f"Positive comments: {sentiment_counts['positive']}")
        print(f"Neutral comments: {sentiment_counts['neutral']}")
        print(f"Negative comments: {sentiment_counts['negative']}")
        print(f"Average sentiment score: {avg_score:.2f}")
        print(f"\nA bar chart '{filename}' has been saved in the '{output_dir}' directory.")

        logging.info("EDA completed successfully")

    except Exception as e:
        logging.error(f"An error occurred during EDA: {str(e)}")
