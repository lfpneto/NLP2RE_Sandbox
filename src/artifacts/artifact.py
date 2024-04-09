import os
from Utils import parse_xml
from Utils import clean_data


class artifact:
    def __init__(self, path, namespace):
        print('artifact class object created...')
        self.path = path  # Assuming string type
        self.name = os.path.basename(path)  # Get the filename from the path
        self.namespace = namespace
        self.setDf()
        self.requirementCollection = []  # List to hold requirements

    def setDf(self):
        self.df = parse_xml.process_xml_with_namespace(
            self.path, self.namespace)
        self.df['text_clean'] = self.df['text'].apply(
            lambda x: clean_data.preprocess_data_str(x))
