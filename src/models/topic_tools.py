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
