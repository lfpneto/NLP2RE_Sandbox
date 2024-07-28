import json
import os
import numpy as np  # Import numpy for type conversion
from collections import OrderedDict
from datetime import datetime
from utils.utils import load_parameters
from models.internal_metrics import cosine_similarity_matrix
from models.internal_metrics import extract_high_similarity_pairs


def save_results_to_json(docs, lda_model, BOW, params="config.json", filename=None, foldername="evaluation_log"):
    """
    Save the evaluation results to a JSON file.

    Parameters:
    docs (artifacts): The artifacts object containing all artifact data.
    lda_model (gensim.models.LdaModel): The trained LDA model.
    BOW (list): The bag-of-words representation of the corpus.
    params (str): The name of the JSON file with configuration parameters.
    filename (str): The name of the JSON file to save the results. If None, a filename with the current date and time will be generated.
    foldername (str): The directory where the evaluation results will be saved.
    """

    # Ensure the "evaluation_log" directory exists
    os.makedirs(foldername, exist_ok=True)

    if filename is None:
        # Generate a filename with the current date and time if none is provided
        current_time = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
        filename = f"evaluation_results_{current_time}.json"

    # Full path for the JSON file
    filepath = os.path.join(foldername, filename)

    # Read configuration from config.json
    try:
        with open(params, 'r') as config_file:
            config_data = json.load(config_file)
            params = load_parameters('config.json')
            TOPIC_SIMILARITY_THRESHOLD = params['topic_similarity_threshold']
    except FileNotFoundError:
        print(f"Error: Configuration file '{params}' not found.")
        config_data = {}  # Default to empty if config is not found
    except json.JSONDecodeError:
        print(
            f"Error: Configuration file '{params}' contains invalid JSON.")
        config_data = {}  # Default to empty if config has invalid JSON

    # Calculate cosine similarity matrix and extract high similarity pairs
    similarity_matrix, topics = cosine_similarity_matrix(lda_model)
    high_similarity_pairs = extract_high_similarity_pairs(
        similarity_matrix, lda_model,
        threshold=TOPIC_SIMILARITY_THRESHOLD, num_words=10)

    # Prepare high similarity pairs data for JSON serialization
    high_similarity_pairs_data = [
        {
            "topic_1": int(pair[0]),  # Convert to Python int
            "topic_2": int(pair[1]),  # Convert to Python int
            "similarity_score": float(pair[2]),  # Convert to Python float
            "top_words_topic_1": pair[3],
            "top_words_topic_2": pair[4]
        }
        for pair in high_similarity_pairs
    ]

    # Initialize the evaluation results dictionary
    evaluation_results = {
        "parameters": config_data,  # Include the config data at the top level
        "model_metrics": [],
        "topic_summary": OrderedDict(),
        "artifacts": [],
    }

    # Collect model lifecycle metrics
    metrics_result = {
        "model_lifecycle_events": lda_model.lifecycle_events,
        "high_similarity_pairs": high_similarity_pairs_data
    }
    evaluation_results["model_metrics"].append(metrics_result)

    # Dictionary to store topic summary
    topic_summary = {}

    # Collecting data for each artifact
    for artifact in docs.artifactsCollection:
        artifact_result = {
            "artifact_name": artifact.name,
            "artifact_path": artifact.path,
            # Ensure int type
            "total_reqs": int(len(artifact.df[artifact.df['tag'] == 'req'])),
            "requirements": []
        }

        # Filter the DataFrame to get rows where 'tag' is 'req'
        req_mask = artifact.df['tag'] == 'req'

        for index, row in artifact.df[req_mask].iterrows():
            topic_id = row['topics']
            text_clean = " ".join(row['text_clean']) if isinstance(
                row['text_clean'], list) else row['text_clean']

            if topic_id is not None:
                topic_words = lda_model.print_topic(int(topic_id))

                req_result = {
                    "df_index": int(index),  # Ensure int type
                    "req_id": row['id'],
                    "text": row['text'],
                    "text_clean": text_clean,
                    "topic_id": topic_id,
                    "topic_words": topic_words,
                }
                artifact_result["requirements"].append(req_result)

                if topic_id not in topic_summary:
                    topic_summary[topic_id] = {
                        "topic_words": topic_words,
                        "total_reqs_by_artifact": {}
                    }
                if artifact.name not in topic_summary[topic_id]["total_reqs_by_artifact"]:
                    topic_summary[topic_id]["total_reqs_by_artifact"][artifact.name] = {
                        "count": 0,
                        "req_ids": []
                    }

                topic_summary[topic_id]["total_reqs_by_artifact"][artifact.name]["count"] += 1
                topic_summary[topic_id]["total_reqs_by_artifact"][artifact.name]["req_ids"].append(
                    row['id'])
            else:
                req_result = {
                    "df_index": int(index),  # Ensure int type
                    "req_id": row['id'],
                    "text": row['text'],
                    "text_clean": text_clean,
                    "topic_id": False,
                    "topic_words": False,
                }
                artifact_result["requirements"].append(req_result)

        # Sort requirements by req_id
        artifact_result["requirements"] = sorted(
            artifact_result["requirements"], key=lambda x: x["req_id"])
        evaluation_results["artifacts"].append(artifact_result)

    # Order the topic_summary by topic_id
    evaluation_results["topic_summary"] = OrderedDict(
        sorted(topic_summary.items(), key=lambda item: item[0])
    )

    # Save the evaluation results to a JSON file
    with open(filepath, 'w') as json_file:
        json.dump(evaluation_results, json_file, indent=4)

    print(f"Results saved to {filepath}")
