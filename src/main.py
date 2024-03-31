from artifacts.artifacts import artifacts
from artifacts.artifact import artifact
from requirements.requirement import requirement


NAMESPACE = {'ns': 'req_document.xsd'}
# PATH = r'C:\dev\NLP-Sandbox\PURE\requirements-xml\0000 - cctns.xml'
PATH = r'C:\dev\NLP-Sandbox\PURE\requirements-xml'


def main():
    artifacts_instance = artifacts(path2Artifacts=PATH, namespace=NAMESPACE)
    artifact1 = artifact("Artifact1")
    artifact2 = artifact("Artifact2")
    requirement1 = requirement(1, "Requirement1")
    requirement2 = requirement(2, "Requirement2")

    # Establishing relationships
    artifact1.requirementCollection.append(requirement1)
    artifact2.requirementCollection.append(requirement2)
    artifacts_instance.artifactsCollection.append(artifact1)
    artifacts_instance.artifactsCollection.append(artifact2)

    # Example usage
    print("Artifacts:")
    for artifact_item in artifacts_instance.artifactsCollection:
        print(f"Artifact Name: {artifact_item.name}")
        print("Requirements:")
        for requirement_item in artifact_item.requirementCollection:
            print(
                f"  - ID: {requirement_item.Id}, Text: {requirement_item.reqText}")


if __name__ == "__main__":
    main()
