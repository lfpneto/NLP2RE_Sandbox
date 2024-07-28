from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim import corpora, models
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns

# Example to calculate perplexity


def perplexity(model, BOW):
    """
    Calculate perplexity for the given LDA model and BOW corpus.

    :param model: LDA model.
    :param BOW: Bag of Words corpus.
    :return: Perplexity value.
    """
    perplexity = model.log_perplexity(BOW)
    print(f'Perplexity: {perplexity}')
    return perplexity


def cosine_similarity_matrix(lda):
    """
    Calculate cosine similarity matrix for topics.

    :param lda: LDA model.
    :return: Cosine similarity matrix and topic matrix.
    """
    # Get the topics
    topics = lda.get_topics()  # shape: (num_topics, num_words)

    # Compute cosine similarity between all pairs of topics
    similarity_matrix = cosine_similarity(topics)

    return similarity_matrix, topics


def cluster_topics(similarity_matrix, num_clusters=20):
    """
    Cluster topics based on the similarity matrix.

    :param similarity_matrix: Cosine similarity matrix.
    :param num_clusters: Number of clusters to form.
    :return: Cluster assignments for each topic.
    """
    # TODO: Better understanding on how value can be retrieved from this metric
    # Initialize the clustering model with the updated metric parameter
    clustering_model = AgglomerativeClustering(
        n_clusters=num_clusters,
        metric='precomputed',  # Use 'precomputed' for the cosine similarity matrix
        linkage='average'
    )

    # Fit the model and predict cluster assignments
    cluster_assignments = clustering_model.fit_predict(1 - similarity_matrix)

    return cluster_assignments


def extract_high_similarity_pairs(similarity_matrix, lda_model, threshold=0.7, num_words=20):
    """
    Extract pairs of topics with similarity higher than a given threshold and their top words.

    :param similarity_matrix: A square numpy array representing topic similarity.
    :param lda_model: Trained LDA model.
    :param threshold: Similarity threshold for filtering topic pairs.
    :param num_words: Number of top words to display for each topic.
    :return: List of tuples containing topic indices, similarity score, and top words.
    """
    num_topics = similarity_matrix.shape[0]
    high_similarity_pairs = []

    for i in range(num_topics):
        for j in range(i + 1, num_topics):  # Only check upper triangle (excluding diagonal)
            if similarity_matrix[i, j] > threshold:
                # Retrieve top words for each topic
                top_words_i = [word for word,
                               _ in lda_model.show_topic(i, num_words)]
                top_words_j = [word for word,
                               _ in lda_model.show_topic(j, num_words)]

                # Append the pair with similarity and top words
                high_similarity_pairs.append(
                    (i, j, similarity_matrix[i, j], top_words_i, top_words_j))

    return high_similarity_pairs


def print_high_similarity_pairs(high_similarity_pairs):
    """
    Print pairs of topics with high similarity and their top words.

    :param high_similarity_pairs: List of tuples with topic indices, similarity scores, and top words.
    """
    print(f"Pairs of Topics with Similarity Higher than Threshold:")
    for i, (topic_i, topic_j, similarity, words_i, words_j) in enumerate(high_similarity_pairs):
        print(f"Pair {i+1}:")
        print(
            f"  Topic {topic_i} and Topic {topic_j}: Similarity = {similarity:.2f}")
        print(f"  Topic {topic_i}: {', '.join(words_i)}")
        print(f"  Topic {topic_j}: {', '.join(words_j)}\n")


def plot_similarity_matrix(similarity_matrix, cluster_assignments, topic_labels=None):
    """
    Plot cosine similarity matrix and cluster assignments, excluding zero clusters.

    :param similarity_matrix: Cosine similarity matrix.
    :param cluster_assignments: Cluster assignments for topics.
    :param topic_labels: Optional list of labels for each topic.
    """
    # Plot cosine similarity matrix with custom color scale
    plt.figure(figsize=(10, 8))
    heatmap = sns.heatmap(
        similarity_matrix,
        cmap='coolwarm',
        annot=False,
        cbar=True,
        vmin=0.4,
        vmax=1.0
    )

    # Customizing the color bar
    cbar = heatmap.collections[0].colorbar
    cbar.set_ticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])  # Set specific ticks
    cbar.set_ticklabels(['0.4', '0.5', '0.6', '0.7', '0.8',
                        '0.9', '1.0'])  # Label ticks

    plt.title('Cosine Similarity Matrix of Topics')
    plt.xlabel('Topic Index')
    plt.ylabel('Topic Index')
    plt.show()

    # Filter out topics with zero clusters
    non_zero_indices = np.where(cluster_assignments != 0)[0]
    filtered_cluster_assignments = cluster_assignments[non_zero_indices]
    filtered_topic_labels = None
    if topic_labels is not None:
        filtered_topic_labels = [topic_labels[i] for i in non_zero_indices]

    # Plot cluster assignments excluding zero clusters
    plt.figure(figsize=(10, 8))
    scatter_plot = sns.scatterplot(
        x=non_zero_indices,
        y=filtered_cluster_assignments,
        hue=filtered_cluster_assignments,
        palette='Set2',
        legend=None
    )
    plt.title('Cluster Assignments of Topics (Excluding Zero Clusters)')
    plt.xlabel('Topic Index')
    plt.ylabel('Cluster')

    # Annotate each point with the corresponding label
    if filtered_topic_labels is not None:
        for i, label in enumerate(filtered_topic_labels):
            scatter_plot.text(
                non_zero_indices[i],
                filtered_cluster_assignments[i],
                str(label),
                fontsize=9,
                ha='right',
                va='bottom'
            )

    plt.show()
