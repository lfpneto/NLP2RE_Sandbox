# Document Class

from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import models
from Utils import parse_xml
from Utils import nlp_transformations


class Document:
    def __init__(self, xml_file_path, namespace):
        self.xml_file_path = xml_file_path
        self.namespace = namespace
        self.df = None
        self.tfidf_matrix = None

        # import Utils.ParseXML as ParseXML
        self.df = parse_xml.process_xml_with_namespace(
            xml_file_path, namespace)

    def __str__(self):
        return f"{self.__str__}({self.xml_file_path})"

    def gen_tfidf_matrix(self):
        # Initialize TfidfVectorizer
        self.tfidf_vectorizer = TfidfVectorizer()
        # Fit and transform the text in df to compute TF-IDF scores
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['text'])

    def print_tfidf_matrix(self):
        # get idf values and feature names
        print('\nidf values:')
        for ele1, ele2 in zip(self.tfidf_vectorizer.get_feature_names_out(), self.tfidf_vectorizer.idf_):
            print(ele1, ':', ele2)

    def gen_corpus(self):
        # FIXME: ['text_clean'] not yet created
        corpus = nlp_transformations.df_tokenized_2_corpus(
            self.df['text_clean'], 2)
