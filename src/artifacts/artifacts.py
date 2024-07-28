import os
import pprint

from artifacts.artifact import artifact
from gensim import corpora
from gensim.corpora import Dictionary
from gensim.parsing import preprocessing
from utils import clean_data
from utils import stpwrds
from collections import defaultdict


class artifacts:
    def __init__(self, path2Artifacts, namespace):
        self.path2Artifacts = path2Artifacts
        self.namespace = namespace
        self.artifactsCollection = []
        self.load_artifacts()
        self._dictionary = self.initialize_dictionary()
        self.initialize_all_BOW()
        self.all_BOW = self.get_all_BOW()
        print(f'instance created: {self}')

    def __str__(self):
        return f"Artifacts({self.path2Artifacts})"

    @property
    def dictionary(self):
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        self._dictionary = value

    def load_artifacts(self):
        for filename in os.listdir(self.path2Artifacts):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(self.path2Artifacts, filename)
                self.artifactsCollection.append(
                    artifact(xml_file_path, self.namespace))

    def initialize_dictionary(self):
        # initialize a Dictionary
        dct = Dictionary()
        # TODO: Fix costum implementation of stopword removal
        remove_stopwords = False
        filter_extremes = False

        # add more document (extend the vocabulary)
        for artifact in self.artifactsCollection:
            list_of_lists_tokens = clean_data.df_tokenize(
                artifact.df['text_clean'])
            dct.add_documents(list_of_lists_tokens)

        if remove_stopwords:
            stopwords_instance = stpwrd()
            list_of_lists_tokens = [[preprocessing.remove_stopwords(
                token) for token in tokens] for tokens in list_of_lists_tokens]
            # Remove custom words from dictionary
            # Get the ids of the custom words to be removed
            ids_to_remove = [dct.token2id[word]
                             for word in stopwords_instance.stopwords if word in dct.token2id]
            # Filter the dictionary
            dct.filter_tokens(bad_ids=ids_to_remove)
            del stopwords_instance

        if filter_extremes:
            dct.filter_extremes(no_below=0, no_above=0.075, keep_n=1000000)

        dct.compactify()
        return dct

    def initialize_all_BOW(self):
        if self._dictionary is None:
            self.initialize_dictionary()
        for artifact in self.artifactsCollection:
            artifact.initialize_bow(self._dictionary)

    def get_all_BOW(self):
        # Create a list of all clean texts from artifacts
        all_BOW = []
        for artifact in self.artifactsCollection:
            for text in artifact.cleanText:
                # Tokenize the text if it's a string
                if isinstance(text, str):
                    tokens = text.split()
                else:
                    tokens = text

                # Create the BoW representation
                bow = self.dictionary.doc2bow(tokens)
                all_BOW.append(bow)

        return all_BOW
