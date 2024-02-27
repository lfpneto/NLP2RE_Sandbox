import string
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
wn = nltk.WordNetLemmatizer()
ps = nltk.PorterStemmer()
lemmatizer = WordNetLemmatizer()


def remove_punct(text):
    # FIXME: the '-' caracter is deleted
    # FIXME: multiple whitespaces are not deleted
    text_nopunct = "".join(
        [char for char in text if char not in string.punctuation])
    return text_nopunct


def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens


def lemmatizing(tokenized_text):
    # Initialize WordNetLemmatizer
    # Lemmatize each word in the tokenized text
    text = [lemmatizer.lemmatize(word) for word in tokenized_text]

    return text


def clean_text_original(text):
    text = "".join([word.lower()
                   for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = " ".join([ps.stem(word)
                    for word in tokens if word not in stopwords])
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

    # Remove punctuation
    if remove_punct:
        text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenize the text using regular expression
    tokens = re.findall(r'\b\w+(?:-\w+)*\b', text.lower())

    # Remove stopwords if required
    if remove_stopwords:
        tokens = [word for word in tokens if word not in stopwords]

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
    text = "".join([word.lower()
                   for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = " ".join([ps.stem(word)
                    for word in tokens if word not in stopwords])
    return text


def clean_text_2stem(text):
    text = "".join([word.lower()
                   for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords]
    return text
