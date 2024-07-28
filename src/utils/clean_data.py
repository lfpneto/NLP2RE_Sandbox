import string
import re
import os
import json
import nltk
import pprint
from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
from collections import defaultdict
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer


from utils.utils import load_parameters

wn = nltk.WordNetLemmatizer()
ps = nltk.PorterStemmer()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
en_stop = set(stopwords.words('english'))

try:
    # Attempt to load parameters
    params = load_parameters('config.json')
    N_GRAM_MIN = params['data_preparation']['tokenization']['n_gram_min']
    N_GRAM_MAX = params['data_preparation']['tokenization']['n_gram_max']
    REMOVE_STOPWORDS = params['data_preparation']['stopwords']['remove_stopwords']
    STOPWORD_STATIC = params['data_preparation']['stopwords']['stopword_static']
    STOPWORD_DYNAMIC = params['data_preparation']['stopwords']['stopword_dynamic']
    STOPWORD_DYNAMIC_SOURCE = params['data_preparation']['stopwords']['stopword_dynamic_source']
    PORTER_STEMMER = params['data_preparation']['porter_stemmer']
    LEMMA = params['data_preparation']['lemma']
    STEMMA = params['data_preparation']['stemma']

except Exception as e:
    # Catch-all for any other unexpected exceptions
    print(f"An error occurred: {str(e)}")
    # FIXME: Jupyter notebooks kernel is not using the same enviorment
    N_GRAM_MIN = 1
    N_GRAM_MAX = 1
    REMOVE_STOPWORDS = False
    STOPWORD_STATIC = False
    STOPWORD_DYNAMIC = False
    STOPWORD_DYNAMIC_SOURCE = False
    PORTER_STEMMER = False
    LEMMA = False
    STEMMA = False


def data_preparation(text,
                     n_gram_min=N_GRAM_MIN,
                     n_gram_max=N_GRAM_MAX,
                     remove_stopwords=REMOVE_STOPWORDS,
                     stopword_static=STOPWORD_STATIC,
                     stopword_dynamic=STOPWORD_DYNAMIC,
                     stopword_dynamic_source=STOPWORD_DYNAMIC_SOURCE,
                     lemma=LEMMA,
                     stemma=STEMMA,
                     porter_stemmer=PORTER_STEMMER):
    """
    Input  : Single string representing a document, optional parameters for N-gram range,
             stopword removal, lemmatization, stemming, and custom stopwords.
    Purpose: Preprocess text with tokenization, optional stopword removal, and either lemmatization or stemming.
    Output : Preprocessed text as a list of tokens
    """

    # Tokenize
    tokens = tokenize(text)

    # stopword removal
    if remove_stopwords:
        tokens = [word for word in tokens if word not in en_stop]

        if stopword_dynamic:
            en_stop.update(stopword_dynamic_source)

    # Choose either lemmatization, stemming, or neither
    if lemma:
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
    elif stemma:
        tokens = [stemmer.stem(word) for word in tokens]
    return tokens


def remove_punct(text):
    # FIXME: the '-' caracter is deleted
    # FIXME: multiple whitespaces are not deleted
    text_nopunct = "".join(
        [char for char in text if char not in string.punctuation])
    return text_nopunct


def tokenize(text):
    # FIXME: Missing n-grams implementation
    if True:
        # option 1
        # Decided to use gensim tokenizer
        tokens = list(re.split('\W+', text))

    elif False:
        # option 2
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text.lower())

    return tokens


def lemmatizing(tokenized_text):
    """
    Lemmatizes each word in the tokenized text using WordNetLemmatizer.

    Parameters:
    - tokenized_text (list of str): The list of words to be lemmatized, as tokens.

    Returns:
    - lemmatized_text (list of str): The lemmatized list of words.
    """
    # Initialize WordNetLemmatizer
    # Lemmatize each word in the tokenized text
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = [lemmatizer.lemmatize(word) for word in tokenized_text]

    return lemmatized_text


def clean_text_original(text):
    en_stop = set(stopwords.words('english'))
    text = "".join([word.lower()
                   for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = " ".join([ps.stem(word)
                    for word in tokens if word not in en_stop])
    return text


def clean_text(text, remove_punct=True, remove_stopwords=True):
    """
    Clean the input text by removing punctuation, stopwords, and performing tokenization.

    Parameters:
    - text (str): The input text to be cleaned.
    - remove_punct (bool): Flag to indicate whether to remove punctuation or not. Default is True.
    - remove_stopwords (bool): Flag to indicate whether to remove stopwords or not. Default is True.

    Returns:
    - cleaned_text (list of str): The cleaned list of tokens.
    """

    # FIXME:  V1.0 tokenized as "v1","0"
    en_stop = set(stopwords.words('english'))

    # Remove punctuation
    if remove_punct:
        text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenize the text using regular expression
    tokens = re.findall(r'\b\w+(?:-\w+)*\b', text.lower())

    # Remove stopwords if required
    if remove_stopwords:
        tokens = [word for word in tokens if word not in en_stop]

    return tokens


def join_list_to_string(attribute):
    if isinstance(attribute, list):
        return ' '.join(attribute)
    else:
        return str(attribute)


def clean_and_lemm_text(text):
    text_clean = clean_text(text, False, False)
    text_lemm = lemmatizing(text_clean)
    list_2_word = join_list_to_string(text_lemm)

    return list_2_word

# N-Grams needs a string, not a list o strings
# meaning that after tokenizing it will join the tokens again as a string


def clean_text_2string(text):
    en_stop = set(stopwords.words('english'))

    text = "".join([word.lower()
                   for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = " ".join([ps.stem(word)
                    for word in tokens if word not in en_stop])
    return text


def clean_text_2stem(text):
    en_stop = set(stopwords.words('english'))
    text = "".join([word.lower()
                   for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in en_stop]
    return text


def preprocess_data_list(list_string, custom_stopwords={}):
    """
    Input  : Document list, a set data type with custom_stopwords
    Purpose: Preprocess text (tokenize, remove stopwords, and stemming)
    Output : Preprocessed text

    DevNotes: This is an alternative to clean text
    """
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = set(stopwords.words('english'))
    en_stop.update(custom_stopwords)
    p_stemmer = PorterStemmer()
    texts = []

    for text in list_string:
        raw = text.lower()
        tokens = tokenizer.tokenize(raw)
        stopped_tokens = [word for word in tokens if word not in en_stop]
        stemmed_tokens = [p_stemmer.stem(word) for word in stopped_tokens]
        texts.append(stemmed_tokens)

    return texts


def df_tokenize(df_column, min_word_freq=1):
    """
    Process a DataFrame attribute containing a list of tokenized data.

    Parameters:
    - df_column (pandas.Series): DataFrame column containing a list of tokenized data.
    - min_word_freq (int): minimum word frequency

    Returns:
    - processed_corpus (list of lists): Processed corpus after filtering based on word frequencies.
    """
    # Count word frequencies
    from collections import defaultdict
    frequency = defaultdict(int)

    # Count word frequencies
    for text_list in df_column:
        for token in text_list:
            frequency[token] += 1

    # Only keep words that appear more than once
    df_tokenized = [[token for token in text_list if frequency[token]
                     > min_word_freq] for text_list in df_column]

    return df_tokenized
