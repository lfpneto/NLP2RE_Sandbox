import time
from artifacts.artifacts import artifacts
from artifacts.artifact import artifact
from requirements.requirement import requirement


# PATH = r'C:\dev\NLP-Sandbox\PURE\requirements-xml\0000 - cctns.xml'
PATH = r'data\work_data'
NAMESPACE = {'ns': 'req_document.xsd'}


def main():
    artifacts_instance = artifacts(path2Artifacts=PATH, namespace=NAMESPACE)

    # Example usage
    print("Artifacts:")
    for artifact_item in artifacts_instance.artifactsCollection:
        print(f"Artifact Name: {artifact_item.name}")
        print("Requirements:")
        for requirement_item in artifact_item.requirementCollection:
            print(
                f"  - ID: {requirement_item.Id}, Text: {requirement_item.reqText}")

    while True:
        # Add a sleep statement to reduce CPU usage
        time.sleep(5)  # Sleep for 5 seconds


if __name__ == "__main__":
    main()
