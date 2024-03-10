def df_tokenized_2_corpus(df_column, min_word_freq=1):
    """
    Process a DataFrame attribute containing a list of tokenized data.

    Parameters:
    - df_column (pandas.Series): DataFrame column containing a list of tokenized data.
    - min_word_freq (int): minimum word frequency

    Returns:
    - processed_corpus (list of lists): Processed corpus after filtering based on word frequencies.
    """
    # Count word frequencies
    from collections import defaultdict
    frequency = defaultdict(int)

    # Count word frequencies
    for text_list in df_column:
        for token in text_list:
            frequency[token] += 1

    # Only keep words that appear more than once
    processed_corpus = [[token for token in text_list if frequency[token]
                         > min_word_freq] for text_list in df_column]

    return processed_corpus
