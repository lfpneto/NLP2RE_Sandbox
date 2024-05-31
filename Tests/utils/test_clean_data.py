# test_clean_data.py

from Utils import clean_data
import string


def test_remove_punct():
    # Test input with punctuation
    text_with_punct = "Hello, World! How are you?"
    expected_result = "Hello World How are you"

    # Call the remove_punct function
    result = clean_data.remove_punct(text_with_punct)

    # Assert that the result matches the expected output
    assert result == expected_result

    # Test input with no punctuation
    text_without_punct = "This is a sentence without any punctuation"
    expected_result = text_without_punct

    # Call the remove_punct function
    result = clean_data.remove_punct(text_without_punct)

    # Assert that the result matches the expected output
    assert result == expected_result

    # Test input with only punctuation
    text_only_punct = "!@#$%^&*()_+"
    expected_result = ""

    # Call the remove_punct function
    result = clean_data.remove_punct(text_only_punct)

    # Assert that the result matches the expected output
    assert result == expected_result


def test_tokenize():
    # TODO:
    pass


def test_lemmatizing():
    """ Lemmatizing

    - See how the lemmatizing function reacts to erros, abbreviations and non indexed words
    DAL ( Development Assurance Levels or Design Assurance Levels ) 
    IDAL ( Item Development Assurance Levels used for the software )
    Automotive Safety Integrity Level (ASIL)
    ECSS-Q-ST-40 ( Safety )
    """
    input_1 = ["Devel", "Assurance", "DAL", "SIL", "ECSS-Q-ST-40"]
    expected_result_1 = ["Devel", "Assurance", "DAL", "SIL", "ECSS-Q-ST-40"]
    result_1 = clean_data.lemmatizing(input_1)
    assert result_1 == expected_result_1
    # TODO: Test actual lemmatization


def test_clean_text_original():
    # TODO:
    pass


def test_clean_text():
    text_with_punct = "Hello, World! How are you?"
    expected_result = "Hello World How are you"
    # TODO:
    pass


def test_join_list_to_string():
    # TODO:
    pass


def test_clean_and_lemm_text():
    # TODO:
    pass


def test_preprocess_data_str():
    input_1 = "Hello, World! How are you?"
    expected_result_1 = ['hello', 'world']
    result_1 = clean_data.preprocess_data_str(input_1)
    assert result_1 == expected_result_1
