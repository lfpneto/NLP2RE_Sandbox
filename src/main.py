import gensim
from artifacts.artifacts import artifacts
from models.topic_tools import get_topic_with_highest_value
from models.topic_tools import get_topics_for_unseen_text
from models.topic_tools import display_topics
from models.topic_tools import find_matching_requirements
from models.internal_metrics import cosine_similarity_matrix
from models.internal_metrics import extract_high_similarity_pairs
from models.internal_metrics import print_high_similarity_pairs
from models.evaluation import save_results_to_json
from utils.utils import load_parameters
import logging

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Logs to the console
)

params = load_parameters('config.json')

# Access the parameters
PATH = params['path']
NAMESPACE = params['namespace']
NUM_TOPICS_START = params['num_topics_start']
NUM_TOPICS_LIMIT = params['num_topics_limit']
NUM_TOPICS_STEP = params['num_topics_step']
FILENAME = params['filename']
TOPIC_SIMILARITY_THRESHOLD = params['topic_similarity_threshold']
# Access the nested parameters
NUM_TOPICS = params['lsa']['num_topics']
# LSA_PARAM_2 = params['lsa']['min_doc_freq']
# LSA_PARAM_3 = params['lsa']['normalization']


def main():
    # Open folder with .xml req's
    docs = artifacts(path2Artifacts=PATH, namespace=NAMESPACE)

    # For each .xml, creates a new artifact
    for artifact in docs.artifactsCollection:
        print(
            f"Artifact Name: {artifact.name} \n  has {artifact.df.size} documents")

    # Dictionary from all xml is stored in artifacts
    # FIXME: how can I test the dictionary, e.g contains relevant words in all documents ?
    print(f"Dictionary created from {docs.dictionary.num_docs} documents")
    # Return a list of the n most common words and their counts from the most common to the least.
    print("Number of unique tokens:", len(docs.dictionary))
    print(docs.dictionary.most_common(40))

    # Find the optimal number of topics
    # FIXME: bow used for analysis is only from one artifact.
    # optimal_model, optimal_num_topics, dbi_scores = find_optimal_topics(
    #    docs.dictionary, docs.artifactsCollection[0].bow, NUM_TOPICS_START, NUM_TOPICS_LIMIT, NUM_TOPICS_STEP)
    # print(f"\n### The optimal number of topics is: \n\t {optimal_num_topics}")

    # Train the model on the corpus/BOW
    lda = gensim.models.ldamodel.LdaModel(
        [], num_topics=NUM_TOPICS, id2word=docs.dictionary)
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

    # METRICS
    similarity_matrix, topics = cosine_similarity_matrix(lda)
    high_similarity_pairs = extract_high_similarity_pairs(
        similarity_matrix, lda, threshold=TOPIC_SIMILARITY_THRESHOLD)
    print_high_similarity_pairs(high_similarity_pairs)

    # Optional: Visualize the clustering results
    # plot_similarity_matrix(similarity_matrix, cluster_assignments)

    # EVALUATION
    save_results_to_json(docs, lda, docs.all_BOW)

    # Query with new, unseen document
    while True:
        print("\nEnter your text to get the associated topics (type 'exit' to quit):")
        user_input = input()
        if user_input.lower() == 'exit':
            break

        # Get topics for unseen text
        topics = get_topics_for_unseen_text(lda, docs.dictionary, user_input)
        # Ensure topics is a list of tuples
        if not isinstance(topics, list):
            print("Unexpected format for topics:", topics)
            continue

        # Display the topics
        display_topics(topics, lda)
        find_matching_requirements(docs, topics)


if __name__ == "__main__":
    main()
