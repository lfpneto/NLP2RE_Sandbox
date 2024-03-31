# nlp_module

from src.Requirements.requirement import Requirement
from src.artifact.artifact import Artifact
from src.artifacts.artifacts import Artifacts
from gensim import models
import sys
from Document import Document

print(sys.version)
print(sys.executable)

# Define the namespace
NAMESPACE = {'ns': 'req_document.xsd'}

# Specify the path to your XML filec
path = r'C:\dev\NLP-Sandbox\PURE\requirements-xml\0000 - cctns.xml'

doc1 = Document(path, NAMESPACE)

# train the model
tfidf = models.TfidfModel(doc1.bow)


input_string = "system requirements".lower().split()
print(tfidf[doc1.dictionary.doc2bow(input_string)])
pass
