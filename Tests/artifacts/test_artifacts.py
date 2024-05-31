import os
from unittest.mock import patch, MagicMock
import pytest
from artifacts import artifacts
from gensim.corpora import Dictionary


@pytest.fixture
def mock_artifact():
    mock = MagicMock()
    mock['text_clean'] = "some cleaned text"
    return mock


@pytest.fixture
def mock_clean_data():
    with patch('Utils.clean_data') as mock_clean_data:
        mock_clean_data.df_tokenize.return_value = [["token1", "token2"]]
        yield mock_clean_data


@pytest.fixture
def mock_os_listdir():
    with patch('os.listdir') as mock_listdir:
        mock_listdir.return_value = ["artifact1.xml", "artifact2.xml"]
        yield mock_listdir


@pytest.fixture
def mock_artifact_class():
    with patch('artifacts.artifact') as mock_artifact_class:
        mock_artifact_class.return_value = MagicMock()
        yield mock_artifact_class


def test_initialize_dictionary(mock_os_listdir, mock_artifact_class, mock_clean_data):
    path2Artifacts = '.\data\test_data'
    namespace = {'ns': 'req_document.xsd'}
    art = artifacts(path2Artifacts, namespace)

    # Verify if the dictionary is initialized correctly
    dct = art.initialize_dictionary()
    assert isinstance(dct, Dictionary)
    assert len(dct) > 0  # Ensure dictionary has been populated with tokens
