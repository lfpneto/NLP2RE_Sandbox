from collections import OrderedDict
import numpy as np
from collections import defaultdict
from datetime import datetime
import os
import json
from utils import clean_data


def get_topic_with_highest_value(dictionary, model, text):
    """
    Get the topic with the highest value for a given text.

    Parameters:
    dictionary (gensim.corpora.Dictionary): The gensim dictionary.
    model (gensim.models.LdaModel): The trained LDA model.
    text (list of str): The tokenized text.

    Returns:
    int: The topic ID with the highest value.
    """
    bow = dictionary.doc2bow(text)
    vector = model[bow]

    if isinstance(vector, list):
        # Ensure vector is a list of tuples
        if vector and all(isinstance(item, tuple) and len(item) == 2 for item in vector):
            topic_with_highest_value = max(vector, key=lambda x: x[1])
            return topic_with_highest_value[0]
        else:
            raise ValueError(
                "Unexpected format for 'vector'. It should be a list of tuples.")
    elif isinstance(vector, tuple) and len(vector) == 2:
        # Handle case where vector is a single tuple (this should be less common)
        return vector[0]
    else:
        raise ValueError(
            "Unexpected format for 'vector'. It should be a list of tuples or a single tuple.")


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


def get_topics_for_unseen_text(lda, dictionary, text):
    """
    Get the topic distribution for unseen text using the trained LDA model.

    Parameters:
    - lda (gensim.models.LdaModel): The trained LDA model.
    - dictionary (gensim.corpora.Dictionary): The gensim dictionary.
    - text (str): The input text to be analyzed.

    Returns:
    - topics (list of tuples): A list of topics with their IDs and probabilities.
    - cleaned_words (list of str): The preprocessed words from the input text.
    """
    # Preprocess the text
    words = clean_data.data_preparation(text)

    # Convert text to BoW representation
    bow = dictionary.doc2bow(words)

    # Get topic distribution for the text
    topics = lda[bow]

    return topics, words


def display_topics(topics, lda, threshold=0.2, topn=10):
    """
    Display the most relevant topics for a given document.

    Parameters:
    - topics (list of tuples): List of topic IDs and their probabilities.
    - lda (gensim.models.LdaModel): The trained LDA model.
    - threshold (float): Probability threshold to display a topic.
    - topn (int): Number of top words to display for each topic.
    """
    print("\nTopic distribution for the input text:")
    for topic_num, prob in topics:
        if prob >= threshold:
            topic_terms = lda.show_topic(topic_num, topn)
            topic_terms_str = ', '.join([term for term, _ in topic_terms])
            print(f"Topic {topic_num}: {prob*100:.2f}% probability")
            print(f"  Terms: {topic_terms_str}\n")


def find_matching_requirements(artifacts, topics):
    """
    Iterates through each artifact to find and print requirements that match the topics
    identified from the unseen text.

    Parameters:
    - artifacts: The artifacts object containing the collection of artifacts.
    - topics: A list of tuples where each tuple contains a topic ID and its probability.

    Returns:
    - matching_requirements (dict): Dictionary mapping artifact names to their matching requirements.
    """
    matching_requirements = defaultdict(list)

    for artifact in artifacts.artifactsCollection:
        # Filter the DataFrame to get rows where 'tag' is 'req'
        req_mask = artifact.df['tag'] == 'req'

        # Iterate over requirements
        for index, row in artifact.df[req_mask].iterrows():
            # This contains a list of topics with probabilities
            topic_ids = row['topics']

            # Convert topic_ids to float for comparison
            topic_ids = [float(tid) for tid in topic_ids] if isinstance(
                topic_ids, list) else [float(topic_ids)]

            # Check if any topic ID matches the topics from unseen text
            matching_topic_ids = [
                float(topic_num) for topic_num, prob in topics if float(topic_num) in topic_ids
            ]

            if matching_topic_ids:
                # If there are matching topics, add the requirement's text to the dictionary
                matching_requirements[artifact.name].append({
                    "requirement_id": row['id'],
                    "original_text": row['text']
                })

    return matching_requirements


class NumpyEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder for handling numpy data types and numpy arrays.
    """

    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


def export_results_to_json(text, topics, lda, artifacts, threshold=0.2, topn=10, foldername="evaluation_results"):
    """
    Export results to a JSON file.

    Parameters:
    - text (str): The input text.
    - topics (list): List of tuples with topics and their probabilities.
    - lda (gensim.models.LdaModel): The trained LDA model.
    - artifacts: The artifacts object.
    - threshold (float): Minimum probability threshold for displaying topics.
    - topn (int): Number of top words to show for each topic.
    - foldername (str): Directory to save the JSON file.
    """
    # Ensure the folder exists
    os.makedirs(foldername, exist_ok=True)

    # Generate a filename with the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"topic_results_{current_time}.json"
    filepath = os.path.join(foldername, filename)

    # Prepare results
    topic_details = []
    for topic_num, prob in topics:
        if prob >= threshold:
            topic_terms = lda.show_topic(topic_num, topn)
            topic_terms_str = ', '.join([term for term, _ in topic_terms])
            topic_details.append({
                "topic_num": topic_num,
                "probability": prob,
                "top_words": topic_terms_str
            })

    matching_requirements = {}
    for artifact in artifacts.artifactsCollection:
        artifact_name = artifact.name
        artifact_requirements = []

        # Filter the DataFrame to get rows where 'tag' is 'req'
        req_mask = artifact.df['tag'] == 'req'

        for index, row in artifact.df[req_mask].iterrows():
            topic_ids = row['topics']
            topic_ids = [float(tid) for tid in topic_ids] if isinstance(
                topic_ids, list) else [float(topic_ids)]
            matching_topic_ids = [
                float(topic_num) for topic_num, prob in topics if float(topic_num) in topic_ids]

            if matching_topic_ids:
                artifact_requirements.append({
                    "req_id": row['id'],
                    "text": row['text'],
                    "matching_topic_ids": matching_topic_ids
                })

        if artifact_requirements:
            matching_requirements[artifact_name] = artifact_requirements

    output = {
        "text": text,
        "topics": topic_details,
        "matching_requirements": matching_requirements
    }

    # Save to JSON file
    with open(filepath, 'w') as json_file:
        json.dump(output, json_file, cls=NumpyEncoder, indent=4)

    print(f"Results exported to {filepath}")
