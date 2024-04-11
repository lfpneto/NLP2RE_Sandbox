import os
import pprint
from artifacts.artifact import artifact
from gensim import corpora
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
        # FIXME: dictionary only created from first artifact
        df = self.artifactsCollection[0].df
        clean_text = clean_data.df_tokenize(df['text_clean'], 2)
        dictionary = corpora.Dictionary(clean_text)
        # pprint.pprint(self._dictionary.token2id)
        return dictionary

    def initialize_artifact_BOW(self):
        for artifact in self.artifactsCollection:
            artifact.bow = [self.dictionary.doc2bow(
                text) for text in artifact.cleanText]
