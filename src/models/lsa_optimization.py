import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.matutils import cossim
from sklearn.metrics import pairwise_distances
import numpy as np

# Function to compute the Cosine Davies-Bouldin Index (cDBI)
def compute_cDBI(model, corpus, num_topics, dictionary):
    # Get the topic vectors in a dense format
    topic_vectors = []
    for i in range(num_topics):
        topic_vector = np.zeros(len(dictionary))
        for term_id, weight in model.get_topic_terms(i, topn=len(dictionary)):
            topic_vector[term_id] = weight
        topic_vectors.append(topic_vector)
    
    # Convert topic vectors to a numpy array
    topic_matrix = np.array(topic_vectors)
    
    # Compute the pairwise cosine distances between topic vectors
    dist_matrix = pairwise_distances(topic_matrix, metric='cosine')
    
    # Compute intra-cluster distances
    s_i = np.zeros(num_topics)
    for i in range(num_topics):
        topic_i = topic_matrix[i]
        sims = [1 - dist_matrix[i, j] for j in range(num_topics) if i != j]  # Cosine similarity is 1 - cosine distance
        s_i[i] = np.mean(sims)
    
    # Compute inter-cluster distances
    r_ij = np.zeros((num_topics, num_topics))
    for i in range(num_topics):
        for j in range(num_topics):
            if i != j:
                r_ij[i, j] = (s_i[i] + s_i[j]) / dist_matrix[i, j]
    
    # Compute the Davies-Bouldin index
    dbi = np.mean(np.max(r_ij, axis=1))
    return dbi

# Function to find the optimal number of topics
def find_optimal_topics(dictionary, corpus, start, limit, step):
    dbi_scores = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=10)
        model_list.append(model)
        dbi = compute_cDBI(model, corpus, num_topics, dictionary)
        dbi_scores.append(dbi)
        print(f"Num Topics: {num_topics}, DBI: {dbi}")
    
    # Find the model with the lowest DBI score
    optimal_index = np.argmin(dbi_scores)
    optimal_model = model_list[optimal_index]
    optimal_num_topics = start + optimal_index * step
    
    return optimal_model, optimal_num_topics, dbi_scores