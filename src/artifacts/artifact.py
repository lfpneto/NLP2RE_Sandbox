import os
from Utils import parse_xml
from Utils import clean_data


class artifact:
    def __init__(self, path, namespace):
        print('artifact class object created...')
        self.path = path  # Assuming string type
        self.name = os.path.basename(path)  # Get the filename from the path
        self.namespace = namespace
        self.requirementCollection = []  # List to hold requirements
        self._df = None
        self.df = self.initialize_df()  # Set the df attribute using the setter method
        self._clean_text = self.initialize_clean_text()
        # FIXME: bow needs dictionary from composite
        self._bow = None

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        self._df = value

    def initialize_df(self):
        df = parse_xml.process_xml_with_namespace(
            self.path, self.namespace)
        df['text_clean'] = df['text'].apply(
            lambda x: clean_data.preprocess_data_str(x))
        return df

    @property
    def clean_text(self):
        return self._clean_text

    @clean_text.setter
    def clean_text(self, value):
        self._clean_text = value

    def initialize_clean_text(self):
        clean_text = clean_data.df_tokenize(self.df['text_clean'], 2)
        return clean_text

    @property
    def bow(self):
        return self._bow

    @bow.setter
    def bow(self, value):
        self._bow = value


