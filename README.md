## README: Text Analysis and Readability Script

This script analyzes text scraped from websites and calculates readability metrics.

**What it does:**

* Reads a list of URLs from an Excel file named `Input.xlsx`.
* For each URL:
    * Fetches the webpage content using `requests`.
    * Parses the HTML using `BeautifulSoup`.
    * Extracts text from paragraphs.
    * Performs sentiment analysis using pre-defined positive and negative word lists.
    * Calculates readability metrics like average sentence length, FOG index, and personal pronouns.
* Saves the results as a CSV file named `Output_Data.csv`.

**Requirements:**

* Python 3 (tested with 3.x)
* Libraries:
    * `requests`
    * `beautifulsoup4`
    * `pandas`
    * `nltk`
* NLTK data: `punkt` and `stopwords` (downloaded automatically by the script)
* Text files with positive and negative words in a folder named `MasterDictionary` (e.g., `positive.txt`, `negative.txt`).
* (Optional) Additional stop words in separate text files within a folder named `StopWords` (e.g., custom_stopwords.txt).

**How to use:**

1. Install the required libraries: `pip install requests beautifulsoup4 pandas nltk`
2. Download the NLTK data: `python -m nltk.downloader punkt stopwords` (this is done by the script as well)
3. Place your list of URLs in an Excel file named `Input.xlsx`.
4. Ensure you have positive and negative word lists in the `MasterDictionary` folder.
5. (Optional) Add additional stop words to separate text files in the `StopWords` folder.
6. Run the script: `python analyze_text.py`

**Output:**

* A CSV file named `Output_Data.csv` containing the analyzed data for each URL, including sentiment scores, readability metrics, and word counts.

**Notes:**

* This script focuses on basic text analysis and readability. Sentiment analysis is based on pre-defined word lists and might not be accurate for complex language.
* Error handling is implemented to gracefully handle website fetching and parsing issues.
* You can modify the script to customize the analysis and calculations based on your needs.
