import json


def load_parameters(file_path):
    with open(file_path, 'r') as file:
        parameters = json.load(file)
    return parameters
