import json
import pandas as pd

import nltk
import numpy as np
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

recipes_ingredients = pd.read_csv('recipes_ingredients.csv')
f = open('recipes_corpus.txt')
Recipes_Corpus = f.read()
f.close()



def preprocess_data(docs):
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    docs_clean = []
    punc = str.maketrans('', '', string.punctuation)
    for doc in docs:
        doc_no_punc = doc.translate(punc)
        words = doc_no_punc.lower().split()
        words = [lemmatizer.lemmatize(word, 'v')
                 for word in words if word not in stop_words]
        docs_clean.append(' '.join(words))

    return docs_clean





