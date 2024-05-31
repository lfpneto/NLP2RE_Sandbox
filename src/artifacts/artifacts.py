import os
import pprint
from artifacts.artifact import artifact
from gensim import corpora
from gensim.corpora import Dictionary
from Utils import clean_data


class artifacts:
    def __init__(self, path2Artifacts, namespace):
        print('artifacts class object created...')
        self.path2Artifacts = path2Artifacts
        self.namespace = namespace
        self.artifactsCollection = []
        self.load_artifacts()
        self._dictionary = self.initialize_dictionary()
        self.initialize_artifact_BOW()

    def load_artifacts(self):
        for filename in os.listdir(self.path2Artifacts):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(self.path2Artifacts, filename)
                self.artifactsCollection.append(
                    artifact(xml_file_path, self.namespace))

    def __str__(self):
        return f"Artifacts({self.path2Artifacts})"

    @property
    def dictionary(self):
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        self._dictionary = value

    def initialize_dictionary(self):
        # initialize a Dictionary
        dct = Dictionary()

        # add more document (extend the vocabulary)
        for artifact in self.artifactsCollection:
            list_of_lists_tokens = clean_data.df_tokenize(
                artifact.df['text_clean'])
            dct.add_documents(list_of_lists_tokens)
        return dct

    def initialize_artifact_BOW(self):
        for artifact in self.artifactsCollection:
            artifact.bow = [self.dictionary.doc2bow(
                text) for text in artifact.cleanText]
