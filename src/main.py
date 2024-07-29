import gensim
from artifacts.artifacts import artifacts
from models.topic_tools import get_topic_with_highest_value
from models.topic_tools import get_topics_for_unseen_text
from models.topic_tools import display_topics
from models.topic_tools import find_matching_requirements
from models.topic_tools import export_results_to_json
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
NUM_TOPICS = params['lda']['num_topics']
LDA_PASSES = params['lda']['passes']
LDA_EVAL = params['lda']['eval_every']
LDA_ITERATIONS = params['lda']['iterations']
LDA_MINIMUM_PROB = params['lda']['minimum_probability']


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

    # LDA PARAMETERS
    # num_topics(int, optional)             – The number of requested latent topics to be extracted from the training corpus.
    # passes(int, optional)                 – Number of passes through the corpus during training. More passes can lead to better convergence but will take longer to train.
    # update_every(int, optional)           – Number of documents to be iterated through for each update. Set to 0 for batch learning, > 1 for online iterative learning.
    # eval_every(int, optional)             – Log perplexity is estimated every that many updates. Setting this to one slows down training by ~2x.
    # iterations(int, optional)             – Maximum number of iterations through the corpus when inferring the topic distribution of a corpus.
    # minimum_probability(float, optional)  – Topics with a probability lower than this threshold will be filtered out.
    # per_word_topics(bool)                 – If True, the model also computes a list of topics, sorted in descending order of most likely topics for each word, along with their phi values multiplied by the feature length(i.e. word count).
    # callbacks(list of Callback)           – Metric callbacks to log and visualize evaluation metrics of the model during training.
    # eta                                   - Determines the density of words in topics. A lower eta indicates fewer words per topic, while a higher eta suggests more words. Use 'auto' for automatic adjustment. Alternatively, set a small value like 0.01 if topics should be distinct and sparse.

    lda = gensim.models.ldamodel.LdaModel(
        [], num_topics=NUM_TOPICS,
        id2word=docs.dictionary,
        per_word_topics=False,  # FIXME: set to true and adapt code
        update_every=0,
        alpha='auto',
        eta='auto',
        random_state=42,
        passes=LDA_PASSES,
        eval_every=LDA_EVAL,
        iterations=LDA_ITERATIONS,
        minimum_probability=LDA_MINIMUM_PROB)
    for artifact in docs.artifactsCollection:
        lda.update(artifact.bow)

    # print("Topic descriptors:")
    # for topic in lda.print_topics(): print(f"\t{topic}")

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

    text_list = [
        # 4.1.3
        "Mobile equipment must limit external interference impacts. (I)",
        "All EIRENE mobiles must operate in the EIRENE frequency band. (MI)",
        "All EIRENE mobiles must operate in public GSM 900 frequency bands. (M)",
        "All EIRENE mobiles shall/should operate in the extended GSM-R frequency band. (I)",
        "a) Cab Radio must operate in the extended GSM-R frequency band. (M)",
        "b) General Purpose Radio, Operational Radio, and Shunting Radio should operate in the extended GSM-R frequency band. (O)",
        "All EIRENE mobiles should operate in other public GSM frequency bands. (O)",
        "Equipment operating in 4.1.3i, 4.1.3ii, and 4.1.3iii bands must function at speeds of 0–500 km/h. (MI)",
        "EIRENE mobiles must store data for network and subscriber identification. (M)"]

    is_interactive = False
    if is_interactive:
        while True:
            print("\nEnter your text to get the associated topics (type 'exit' to quit):")
            user_input = input()
            if user_input.lower() == 'exit':
                break

            # Get topics for unseen text
            topics, words = get_topics_for_unseen_text(
                lda, docs.dictionary, user_input)
            # Ensure topics is a list of tuples
            if not isinstance(topics, list):
                print("Unexpected format for topics:", topics)
                continue

            # Display the topics
            display_topics(topics, lda)
            find_matching_requirements(docs, topics)

    else:
        # If not interactive, iterate over a list of predefined strings
        for text in text_list:
            print(f"\nProcessing text: {text}")

            # Get topics for unseen text
            topics, words = get_topics_for_unseen_text(
                lda, docs.dictionary, text)
            # Ensure topics is a list of tuples
            if not isinstance(topics, list):
                print("Unexpected format for topics:", topics)
                continue

            # Display the topics
            find_matching_requirements(docs, topics)
            export_results_to_json(
                text, topics, lda, docs, threshold=0.2, topn=10)


if __name__ == "__main__":
    main()
