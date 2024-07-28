import json
import os
import re

from gensim.parsing.preprocessing import STOPWORDS
from nltk.corpus import stopwords
from utils.utils import load_parameters

# Access the parameters
params = load_parameters('config.json')
CUSTOM_STOPWORDS = params["data_preparation"]["stopwords"]['stopword_dynamic_source']
en_stop = set(stopwords.words('english'))


def remove_static_stopwords(tokens):

    # Regex pattern to match tokens that are only single numbers
    pattern = r'^\d+$'

    # Filter tokens, keeping only those that don't match the pattern
    tokens = [token for token in tokens if not re.match(pattern, token)]

    # Remove stopwords
    tokens = [word for word in tokens if word not in en_stop]
    return tokens


def write_custom_stopwords_to_json(stopwords, filename=CUSTOM_STOPWORDS):
    """
    Initializes a list of custom stopwords to a JSON file.

    :param stopwords: List of custom stopwords to be written to the JSON file.
    :param filename: The name of the JSON file (default is CUSTOM_STOPWORDS).
    """
    # Create a dictionary to hold the stopwords
    data = {
        "stopwords": stopwords
    }

    # Write the stopwords to the JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Stopwords written to {filename}")


def add_custom_stopwords_to_json(new_stopwords, filename=CUSTOM_STOPWORDS):
    """
    Adds new stopwords to an existing list in a JSON file.

    :param new_stopwords: List of custom stopwords to be added to the JSON file.
    :param filename: The name of the JSON file (default is CUSTOM_STOPWORDS).
    """
    # Check if the file exists
    if os.path.exists(filename):
        # Load existing stopwords from the JSON file
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        # Get existing stopwords or initialize an empty list if not present
        existing_stopwords = data.get("stopwords", [])
    else:
        # If the file doesn't exist, start with an empty list
        existing_stopwords = []

    # Add new stopwords to the existing list
    for word in new_stopwords:
        if word not in existing_stopwords:
            existing_stopwords.append(word)

    # Sort stopwords for better management (optional)
    existing_stopwords.sort()

    # Write the updated stopwords list back to the JSON file
    with open(filename, 'w') as json_file:
        json.dump({"stopwords": existing_stopwords}, json_file, indent=4)

    print(f"New stopwords added to {filename}")


def remove_dynamic_stopwords(tokens, filename=CUSTOM_STOPWORDS):
    """
    Removes custom stopwords from the input string using stopwords stored in a JSON file.

    :param tokens: A list of strings from which stopwords should be removed.
    :param filename: The JSON file containing custom stopwords (default is CUSTOM_STOPWORDS).
    :return: The cleaned string with stopwords removed.
    """
    # Check if the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file {filename} does not exist.")

    # Load stopwords from the JSON file
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    stopwords = data.get("stopwords", [])

    # Remove stopwords from the list of words
    cleaned_words = [word for word in tokens if word.lower() not in stopwords]

    return cleaned_words


def remove_numbers_by_length(tokens, min_digits=1, max_digits=3):
    """
    Removes numbers with a specified digit length from the input string.

    :param input_string: The string from which numbers should be removed.
    :param min_digits: The minimum number of digits a number should have to be removed.
    :param max_digits: The maximum number of digits a number should have to be removed.
    :return: The cleaned string with numbers in the specified range removed.
    """
    # Regular expression pattern to match numbers with the specified digit length
    pattern = rf'\b\d{{{min_digits},{max_digits}}}\b'

    # Use re.sub to replace matching numbers with an empty string
    cleaned_string = re.sub(pattern, '', tokens)

    # Remove any extra spaces left after removing numbers
    cleaned_string = ' '.join(cleaned_string.split())

    return cleaned_string
