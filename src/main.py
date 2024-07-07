import time
import gensim
import json
from artifacts.artifacts import artifacts
from artifacts.artifact import artifact
from models.lsa_optimization import find_optimal_topics
from models.topic_tools import get_topic_with_highest_value
from models.topic_tools import get_reqs_by_topic
from models.evaluation import save_results_to_json


def load_parameters(file_path):
    with open(file_path, 'r') as file:
        parameters = json.load(file)
    return parameters


params = load_parameters('config.json')

# Access the parameters
PATH = params['path']
NAMESPACE = params['namespace']
NUM_TOPICS_START = params['num_topics_start']
NUM_TOPICS_LIMIT = params['num_topics_limit']
NUM_TOPICS_STEP = params['num_topics_step']
FILENAME = params['filename']

# Access the nested parameters
LSA_PARAM_1 = params['lsa']['param_1']
LSA_PARAM_2 = params['lsa']['param_2']
LSA_PARAM_3 = params['lsa']['param_3']


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
    optimal_num_topics = 85
    # FIXME: bow used for analysis is only from one artifact.
    # optimal_model, optimal_num_topics, dbi_scores = find_optimal_topics(
    #    docs.dictionary, docs.artifactsCollection[0].bow, NUM_TOPICS_START, NUM_TOPICS_LIMIT, NUM_TOPICS_STEP)
    # print(f"\n### The optimal number of topics is: \n\t {optimal_num_topics}")

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
