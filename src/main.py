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

    # Dictionary from all xml is stored in artifacts
    # print(f"Dictionary created from {docs.dictionary.num_docs} documents")
    # print(docs.dictionary)
    # FIXME: how can I test that the dictionary contains all words in all documents ?

    # Find the optimal number of topics
    # Parameters
    start = 75
    limit = 95
    step = 2

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

    # ADD TOPICS TO REQ

    def get_topic(text):
        bow = docs.dictionary.doc2bow(text)
        vector = lda[bow]
        if vector:
            topic_with_highest_value = max(vector, key=lambda x: x[1])
            return topic_with_highest_value[0]
        else:
            return None

    for artifact in docs.artifactsCollection:
        # Filter the DataFrame to get rows where 'tag' is 'req'
        req_mask = artifact.df['tag'] == 'req'
        artifact.df.loc[req_mask, 'topics'] = artifact.df.loc[req_mask,
                                                              'text_clean'].apply(get_topic)

    # INPUT CHANGE REQUEST
    print("### ### ### ### ### ### ### ### ###")
    print("Querying the model using new, unseen documents")

    # Access req in artifact
    test_document = docs.artifactsCollection[0].df['text_clean'].iloc[19]
    other_corpus = docs.dictionary.doc2bow(test_document)
    print(f"REQ: {test_document}")

    # Get topic probability distribution for a document
    vector = lda[other_corpus]
    if vector:
        # Get the tuple with the highest value based on the second element of each tuple
        topic_with_highest_value = max(vector, key=lambda x: x[1])
        print(
            f"Topic identified in REQ: {topic_with_highest_value[0]} ; {lda.print_topic(topic_with_highest_value[0])}")

    # GET ALL REQs WITH TOPIC

    def get_reqs_by_topic(artifact, topic_id):
        """
        Retrieve all 'req' rows from the artifact's DataFrame that have the specified topic ID.

        Parameters:
        artifact (artifact): The artifact object containing the DataFrame.
        topic_id (int): The topic ID to filter by.

        Returns:
        pd.DataFrame: A DataFrame containing all 'req' rows with the specified topic ID.
        """
        # Filter the DataFrame to get rows where 'tag' is 'req' and 'topics' matches the topic_id
        reqs_with_topic = artifact.df[(artifact.df['tag'] == 'req') & (
            artifact.df['topics'] == topic_id)]
        return reqs_with_topic

    for artifact in docs.artifactsCollection:
        filtered_reqs = get_reqs_by_topic(
            artifact, topic_with_highest_value[0])
        print(f"Filtered_reqs: {filtered_reqs}")

    while True:
        # Add a sleep statement to reduce CPU usage
        time.sleep(5)  # Sleep for 5 seconds


if __name__ == "__main__":
    main()
