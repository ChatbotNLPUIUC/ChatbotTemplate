from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import pandas as pd
import joblib

SYMBOLS = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n,—'"
STOP_WORDS = stopwords.words('english')
LEMMATIZER = WordNetLemmatizer()
STEMMER = SnowballStemmer("english")


def remove_symbols(text):
    for symbol in SYMBOLS:
        text = text.replace(symbol, '')
    return text

def remove_stop_words(vocabulary):
    valid_words = [x for x in vocabulary if x not in STOP_WORDS and x.isalpha()]
    return valid_words


def stem_and_lemmatize(vocabulary):
    stemmed_lemmatized_words = [STEMMER.stem(LEMMATIZER.lemmatize(x)) for x in vocabulary]
    return stemmed_lemmatized_words

def clean_text(sentence):
    sentence = sentence.lower()
    sentence = remove_symbols(sentence)
    vocabulary = word_tokenize(sentence)
    vocabulary = remove_stop_words(vocabulary)
    stemmed_lemmatized_words = stem_and_lemmatize(vocabulary)
    cleaned_sentences = " ".join(stemmed_lemmatized_words)
    return cleaned_sentences

class CleanText(BaseEstimator, TransformerMixin):
    def __init__(self):
        return 
    
    #Return self nothing else to do here    
    def fit(self, X, y=None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform(self, X, y=None):
        return [clean_text(x) for x in X]

dataset = pd.read_csv("./model2_dataset.csv")
X = dataset["sentence"]
y = dataset["label"]

text_clf = Pipeline([
    ('clean', CleanText()),
    ('vect', CountVectorizer(ngram_range=(1,2))),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])

text_clf.fit(X, y)

joblib.dump(text_clf, './model2.pkl', compress=9)