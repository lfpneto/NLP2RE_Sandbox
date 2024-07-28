import json
import os


def load_parameters(file_path):
    """
    Load parameters from a JSON configuration file.

    Args:
        file_path (str): Path to the JSON file containing parameters.

    Returns:
        dict: A dictionary with the parameters loaded from the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON file.
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            # Log an error message and raise an exception
            logging.error(
                f"File not found: {file_path}. Ensure the file path is correct and the file exists.")
            raise FileNotFoundError(
                f"No such file or directory: '{file_path}'")

        # Open and load JSON file
        with open(file_path, 'r') as file:
            parameters = json.load(file)

        return parameters

    except FileNotFoundError as e:
        # Handle the FileNotFoundError
        logging.error(
            "FileNotFoundError: Could not find the configuration file.", exc_info=True)
        print(
            f"Error: The file '{file_path}' does not exist. Please check the file path.")
        raise  # Reraise the exception if you want it to propagate

    except json.JSONDecodeError as e:
        # Handle invalid JSON
        logging.error(
            "JSONDecodeError: The configuration file is not a valid JSON.", exc_info=True)
        print(
            f"Error: The file '{file_path}' is not a valid JSON. Please check the file's content.")
        raise

    except Exception as e:
        # Handle any other exceptions
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        print(f"An unexpected error occurred: {str(e)}")
        raise
