# Document Class

from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import models
from Utils import parse_xml
from Utils import nlp_transformations
from Utils import clean_data
from gensim import corpora


class Document:
    def __init__(self, xml_file_path, namespace):
        self.xml_file_path = xml_file_path
        self.namespace = namespace
        self.df = self.gen_df()
        self.corpus = self.gen_corpus()
        self.dictionary = self.gen_dictionary()
        self.bow = self.gen_bow()

    def __str__(self):
        return f"{self.__str__}({self.xml_file_path})"

    def gen_df(self):
        df = parse_xml.process_xml_with_namespace(
            self.xml_file_path, self.namespace)
        # TODO: Parametrization on the clean text function
        df['text_clean'] = df['text'].apply(
            lambda x: clean_data.preprocess_data_str(x))
        return df

    def gen_corpus(self):
        corpus = nlp_transformations.df_tokenized_2_corpus(
            self.df['text_clean'], 2)
        return corpus

    def gen_dictionary(self):
        dictionary = corpora.Dictionary(self.corpus)
        return dictionary

    def gen_bow(self):
        bow = [self.dictionary.doc2bow(text) for text in self.corpus]
        return bow
