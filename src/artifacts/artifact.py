import os
from Utils import parse_xml
from Utils import clean_data
from artifacts.requirement import requirement


class artifact:
    def __init__(self, path, namespace):
        print('artifact class object created...')
        self.path = path  # Assuming string type
        self.name = os.path.basename(path)  # Get the filename from the path
        self.namespace = namespace
        self.requirementCollection = []  # List to hold requirements
        self._df = None
        self._cleanText = None
        self._bow = None
        self.initialize_df()  # Set the df attribute using the setter method
        self.initialize_textClean()
        self.create_requirements_from_df()

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        self._df = value

    def initialize_df(self):
        self._df = parse_xml.process_xml_with_namespace(
            self.path, self.namespace)
        self._df['text_clean'] = self._df['text'].apply(
            lambda x: clean_data.preprocess_data_str(x))

    @property
    def cleanText(self):
        return self._cleanText

    @cleanText.setter
    def cleanText(self, value):
        self._cleanText = value

    def initialize_textClean(self):
        self._cleanText = clean_data.df_tokenize(self._df['text_clean'], 2)

    @property
    def bow(self):
        return self._bow

    @bow.setter
    def bow(self, value):
        self._bow = value

    def create_requirements_from_df(self):
        for index, row in self._df.iterrows():
            if row['tag'] == 'req':
                req = requirement(row['id'], row['text'], row['text_clean'])
                self.requirementCollection.append(req)

    def initialize_bow(self, dictionary):
        self.bow = [dictionary.doc2bow(text)
                    for text in self._df['text_clean']]
        return self.bow
