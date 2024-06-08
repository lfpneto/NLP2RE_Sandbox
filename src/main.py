import time
import gensim
from artifacts.artifacts import artifacts
from artifacts.artifact import artifact
from models.lsa_optimization import find_optimal_topics

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

    # Find the optimal number of topics
    # Parameters
    start = 30
    limit = 90
    step = 5

    # FIXME: bow used for analysis is only from one artifact.
    optimal_model, optimal_num_topics, dbi_scores = find_optimal_topics(
        docs.dictionary, docs.artifactsCollection[0].bow, start, limit, step)

    print(f"The optimal number of topics is {optimal_num_topics}")

    # Train the model on the corpus/BOW
    lda = gensim.models.ldamodel.LdaModel(
        [], num_topics=optimal_num_topics, id2word=docs.dictionary)
    for artifact in docs.artifactsCollection:
        lda.update(artifact.bow)

    # Print topics with words instead of IDs
    for topic in lda.print_topics():
        print(topic)

    # Query, the model using new, unseen documents
    # Create a new corpus, made of previously unseen documents.
    other_texts = [
        ['computer', 'time', 'graph'],
        ['survey', 'response', 'eps'],
        ['human', 'system', 'computer']
    ]
    other_corpus = [docs.dictionary.doc2bow(text) for text in other_texts]
    unseen_doc = other_corpus[0]
    # get topic probability distribution for a document
    vector = lda[unseen_doc]
    # Get the tuple with the highest value based on the second element of each tuple
    topic_with_highest_value = max(vector, key=lambda x: x[1])
    print("Query, the model using new, unseen documents")
    print(topic_with_highest_value[0])
    lda.print_topic(topic_with_highest_value[0])

    while True:
        # Add a sleep statement to reduce CPU usage
        time.sleep(5)  # Sleep for 5 seconds


if __name__ == "__main__":
    main()
