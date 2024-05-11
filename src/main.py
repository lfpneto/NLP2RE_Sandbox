import time
import gensim
from artifacts.artifacts import artifacts
from artifacts.artifact import artifact

# SPECIFIC_PATH = r'C:\dev\NLP2RE_Sandbox\data\work_data\2006-eirene_sys_15.xml'
PATH = r'data\work_data'
NAMESPACE = {'ns': 'req_document.xsd'}


def main():
    docs = artifacts(path2Artifacts=PATH, namespace=NAMESPACE)

    # Example usage
    for artifact_item in docs.artifactsCollection:
        print(f"Artifact Name: {artifact_item.name}")

    # Models
    # Train the model on the corpus/BOW.
    bow = docs.artifactsCollection[0].bow

    lda = gensim.models.ldamodel.LdaModel(
        bow, num_topics=10, id2word=docs.dictionary)
    # Print topics with words instead of IDs
    for topic in lda.print_topics():
        print(topic)

    while True:
        # Add a sleep statement to reduce CPU usage
        time.sleep(5)  # Sleep for 5 seconds


if __name__ == "__main__":
    main()
