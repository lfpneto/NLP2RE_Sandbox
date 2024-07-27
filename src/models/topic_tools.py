from Utils import clean_data


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
    if vector:
        topic_with_highest_value = max(vector, key=lambda x: x[1])
        return topic_with_highest_value[0]
    else:
        return None


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
    """
    # Preprocess the text
    words = clean_data.preprocess_data_str(text)

    # Convert text to BoW representation
    bow = dictionary.doc2bow(words)

    # Get topic distribution for the text
    topics = lda[bow]

    return topics


def display_topics(topics, lda, threshold=0.2, topn=10):
    """
    Display the most relevant topics for a given document.
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
    """
    for artifact in artifacts.artifactsCollection:
        print(f"Artifact name: {artifact.name}")

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
                # If there are matching topics, print the requirement's text
                print(f"\nRequirement ID: {index}")
                print(f"Original Text:\n{row['text']}")
