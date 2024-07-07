import json
import os
from collections import OrderedDict
from datetime import datetime
from models.topic_tools import get_reqs_by_topic
from models.internal_metrics import perplexity


def save_results_to_json(docs, lda_model, BOW, filename=None):
    """
    Save the evaluation results to a JSON file.

    Parameters:
    docs (artifacts): The artifacts object containing all artifact data.
    lda_model (gensim.models.LdaModel): The trained LDA model.
    BOW (list): The bag-of-words representation of the corpus.
    filename (str): The name of the JSON file to save the results. If None, a filename with the current date and time will be generated.
    """
    # Ensure the "metrics" directory exists
    os.makedirs("metrics", exist_ok=True)

    if filename is None:
        # Generate a filename with the current date and time if none is provided
        current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"evaluation_results_{current_time}.json"

    # Prepend the "metrics" directory to the filename
    filepath = os.path.join("metrics", filename)

    evaluation_results = {
        "model_metrics": [],
        "topic_summary": OrderedDict(),
        "artifacts": []
    }

    metrics_result = {
        "model_lifecycle_events": lda_model.lifecycle_events,
        "perplexity": perplexity(lda_model, BOW)
    }

    evaluation_results["model_metrics"].append(metrics_result)

    topic_summary = {}

    # Collecting data for each artifact
    for artifact in docs.artifactsCollection:
        artifact_result = {
            "artifact_name": artifact.name,
            "artifact_path": artifact.path,
            "total_reqs": len(artifact.df[artifact.df['tag'] == 'req']),
            "requirements": []
        }

        # Filter the DataFrame to get rows where 'tag' is 'req'
        req_mask = artifact.df['tag'] == 'req'
        artifact.df['present_in_filtered_reqs'] = False

        for index, row in artifact.df[req_mask].iterrows():
            topic_id = row['topics']
            text_clean = " ".join(row['text_clean']) if isinstance(
                row['text_clean'], list) else row['text_clean']

            if topic_id is not None:
                topic_words = lda_model.print_topic(int(topic_id))
                filtered_reqs = get_reqs_by_topic(artifact, topic_id)
                present_in_filtered_reqs = not filtered_reqs.empty

                req_result = {
                    "req_id": index,
                    "text": row['text'],
                    "text_clean": text_clean,
                    "topic_id": topic_id,
                    "topic_words": topic_words,
                    "present_in_filtered_reqs": present_in_filtered_reqs
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
                    index)
            else:
                req_result = {
                    "req_id": index,
                    "text": row['text'],
                    "text_clean": text_clean,
                    "topic_id": False,
                    "topic_words": False,
                    "present_in_filtered_reqs": False
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

    with open(filepath, 'w') as json_file:
        json.dump(evaluation_results, json_file, indent=4)
