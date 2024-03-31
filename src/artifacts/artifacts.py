import os
from .artifact import artifact


class artifacts:
    def __init__(self, path2Artifacts, namespace):
        self.path2Artifacts = path2Artifacts
        self.namespace = namespace
        self.model = None  # Assuming model is an object of some class
        self.artifactsCollection = []  # List to hold artifacts
        self.load_artifacts()

    def load_artifacts(self):
        for filename in os.listdir(self.path2Artifacts):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(self.path2Artifacts, filename)
                self.artifactsCollection.append(artifact(xml_file_path))

    def __str__(self):
        return f"Artifacts({self.path2Artifacts})"

    def setModel(self, model):
        self.model = model
