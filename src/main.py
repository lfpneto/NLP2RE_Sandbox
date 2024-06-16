import time
import gensim
from artifacts.artifacts import artifacts
from artifacts.artifact import artifact
from models.lsa_optimization import find_optimal_topics
from models.topic_tools import get_topic_with_highest_value
from models.topic_tools import get_reqs_by_topic
from models.evaluation import save_results_to_json

# SPECIFIC_PATH = r'C:\dev\NLP2RE_Sandbox\data\work_data\2006-eirene_sys_15.xml'
PATH = r'data\work_data'
NAMESPACE = {'ns': 'req_document.xsd'}
NUM_TOPICS_START = 75
NUM_TOPICS_LIMIT = 95
NUM_TOPICS_STEP = 2


def main():
    # Open folder with .xml req's
    docs = artifacts(path2Artifacts=PATH, namespace=NAMESPACE)

    # For each .xml, creates a new artifact
    for artifact in docs.artifactsCollection:
        print(
            f"Artifact Name: {artifact.name} \n\t has {artifact.df.size} documents")

    # Dictionary from all xml is stored in artifacts
    # FIXME: how can I test the dictionary, e.g contains relevant words in all documents ?
    # print(f"Dictionary created from {docs.dictionary.num_docs} documents")
    # print(docs.dictionary)

    # Find the optimal number of topics
    # FIXME: bow used for analysis is only from one artifact.
    optimal_model, optimal_num_topics, dbi_scores = find_optimal_topics(
        docs.dictionary, docs.artifactsCollection[0].bow, NUM_TOPICS_START, NUM_TOPICS_LIMIT, NUM_TOPICS_STEP)
    print(f"\n### The optimal number of topics is: \n\t {optimal_num_topics}")

    # Train the model on the corpus/BOW
    lda = gensim.models.ldamodel.LdaModel(
        [], num_topics=optimal_num_topics, id2word=docs.dictionary)
    for artifact in docs.artifactsCollection:
        lda.update(artifact.bow)
    # print("\n### Topic descriptors:")
    # for topic in lda.print_topics():
    #    print(f"\t{topic}")

    # Add topics to req
    for artifact in docs.artifactsCollection:
        # Filter the DataFrame to get rows where 'tag' is 'req'
        req_mask = artifact.df['tag'] == 'req'

        # Apply the function to the 'text_clean' attribute of these rows and store the result in a new attribute 'topics'
        artifact.df.loc[req_mask, 'topics'] = artifact.df.loc[req_mask, 'text_clean'].apply(
            lambda text: get_topic_with_highest_value(docs.dictionary, lda, text))

    # Evaluation
    save_results_to_json(docs, lda, docs.all_BOW)

    print(f"\n### END MAIN.")


if __name__ == "__main__":
    main()
