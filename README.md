# YouTube Sentiment Analyzer

This project analyzes sentiment and performs exploratory data analysis (EDA) on YouTube video comments for specified channels.

<details>
<summary>Features</summary>

- Fetches recent video comments from specified YouTube channels
- Performs sentiment analysis on the comments
- Generates visualizations including:
  - Sentiment distribution bar chart
  - Sentiment score histogram
  - Keyword word cloud
- Outputs summary statistics

</details>

<details>
<summary>Setup</summary>

1. Clone this repository:

git clone https://github.com/your-username/youtube-sentiment-analyzer.git
cd youtube-sentiment-analyzer


2. Install required dependencies:

pip install -r requirements.txt


3. Obtain a YouTube Data API key from the [Google Developers Console](https://console.developers.google.com/).

4. Create a `config.py` file in the project root and add your API key:
```python
API_KEY = 'YOUR_API_KEY_HERE'

    Create a channels.txt file in the project root and add YouTube channel URLs, one per line:

    https://www.youtube.com/channel/CHANNEL_ID_1
    https://www.youtube.com/channel/CHANNEL_ID_2
```
</details>
Usage

    Run the main script:

    python main.py

    Check the output directory for generated visualizations and logs.

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
License

This project is licensed under the MIT License - see the LICENSE file for details.
