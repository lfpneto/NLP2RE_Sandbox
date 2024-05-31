import time
import gensim
from artifacts.artifacts import artifacts
from artifacts.artifact import artifact

# SPECIFIC_PATH = r'C:\dev\NLP2RE_Sandbox\data\work_data\2006-eirene_sys_15.xml'
PATH = r'data\work_data'
NAMESPACE = {'ns': 'req_document.xsd'}


def main():
    # Open folder with .xml req's
    docs = artifacts(path2Artifacts=PATH, namespace=NAMESPACE)

    # For each .xml, creates a new artifact
    for artifact in docs.artifactsCollection:
        print(f"Artifact Name: {artifact.name}")
        print(f"{artifact.name} has {artifact.df.size} documents")

    # Dictionary from all xml is sored in artifacts
    # print(f"Dictionary created from {docs.dictionary.num_docs} documents")
    # print(docs.dictionary)
    # FIXME: how can I test that the dictionary contains all words in all documents ?

    # Train the model on the corpus/BOW
    lda = gensim.models.ldamodel.LdaModel(
        [], num_topics=10, id2word=docs.dictionary)
    for artifact in docs.artifactsCollection:
        lda.update(artifact.bow)

    # Print topics with words instead of IDs
    for topic in lda.print_topics():
        print(topic)

    while True:
        # Add a sleep statement to reduce CPU usage
        time.sleep(5)  # Sleep for 5 seconds


if __name__ == "__main__":
    main()
