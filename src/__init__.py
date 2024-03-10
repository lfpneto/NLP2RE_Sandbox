# nlp_module

import sys
from Document import Document

print(sys.version)
print(sys.executable)

# Define the namespace
NAMESPACE = {'ns': 'req_document.xsd'}

# Specify the path to your XML filec
path = r'C:\dev\NLP-Sandbox\PURE\requirements-xml\0000 - cctns.xml'

doc1 = Document(path, NAMESPACE)
doc1.gen_tfidf_matrix()
doc1.print_tfidf_matrix()
