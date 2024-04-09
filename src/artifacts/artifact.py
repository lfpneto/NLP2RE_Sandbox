import os
from Utils import parse_xml


class artifact:
    def __init__(self, path, namespace):
        print('artifact class object created...')
        self.path = path  # Assuming string type
        self.name = os.path.basename(path)  # Get the filename from the path
        self.namespace = namespace
        self.df = parse_xml.process_xml_with_namespace(
            path, self.namespace)

        self.requirementCollection = []  # List to hold requirements
