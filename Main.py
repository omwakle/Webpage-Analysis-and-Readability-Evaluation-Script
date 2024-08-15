#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Read the URL file into a pandas DataFrame
df = pd.read_excel('Input.xlsx')

# Load stop words
stop_words = set(stopwords.words('english'))
for file in os.listdir('StopWords'):
    with open(os.path.join('StopWords', file), 'r', encoding='ISO-8859-1') as f:
        stop_words.update(f.read().splitlines())

# Load positive and negative words
pos = set()
neg = set()
for file in os.listdir('MasterDictionary'):
    with open(os.path.join('MasterDictionary', file), 'r', encoding='ISO-8859-1') as f:
        if 'positive' in file:
            pos.update(f.read().splitlines())
        else:
            neg.update(f.read().splitlines())

# Create a DataFrame to store results
columns = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]
results_df = pd.DataFrame(columns=columns)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']

    # Make a request to the URL
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Can't get response for {url_id}: {e}")
        continue

    # Create a BeautifulSoup object
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Can't parse page for {url_id}: {e}")
        continue

    # Find text
    article = ""
    try:
        for p in soup.find_all('p'):
            article += p.get_text()
    except Exception as e:
        print(f"Can't get text for {url_id}: {e}")
        continue

    # Process the text for analysis
    words = word_tokenize(article)
    filtered_text = [word for word in words if word.lower() not in stop_words]

    pos_words = [word for word in filtered_text if word.lower() in pos]
    neg_words = [word for word in filtered_text if word.lower() in neg]

    positive_score = len(pos_words)
    negative_score = len(neg_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(filtered_text) + 0.000001)

    # Calculate readability metrics
    sentences = re.split(r'[.!?]', article)
    num_sentences = len(sentences)
    num_words = len(filtered_text)
    avg_sentence_length = num_words / num_sentences

    complex_words = [word for word in filtered_text if sum(1 for letter in word if letter.lower() in 'aeiou') > 2]
    percent_complex_words = len(complex_words) / num_words
    fog_index = 0.4 * (avg_sentence_length + percent_complex_words)

    syllable_count = sum(1 for word in filtered_text for letter in word if letter.lower() in 'aeiou')
    avg_syllable_word_count = syllable_count / num_words

    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', article, re.I))
    avg_word_length = sum(len(word) for word in filtered_text) / num_words

    # Append results to DataFrame
    results_df = results_df.append({
        'URL_ID': url_id,
        'URL': url,
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percent_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length,
        'COMPLEX WORD COUNT': len(complex_words),
        'WORD COUNT': num_words,
        'SYLLABLE PER WORD': avg_syllable_word_count,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }, ignore_index=True)

# Save the DataFrame to CSV without index
results_df.to_csv('Output_Data.csv', index=False, float_format='%.15g')


# In[ ]:




