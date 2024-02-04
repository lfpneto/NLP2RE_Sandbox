import pandas as pd
import sys
from xmlschema import XMLSchema
from pprint import pprint

print(sys.version)
print(sys.executable)

# Specify the path to your XML file
xml_file_path = r'C:\dev\NLP-Sandbox\PURE\requirements-xml\0000 - cctns.xml'
schema_file_path = r'C:\dev\NLP-Sandbox\PURE\req_document.xsd'

# Define the namespace
namespace = {'ns': 'req_document.xsd'}

# Load an XSD schema file
schema = XMLSchema(schema_file_path)

# Validate against the schema
schema.validate(xml_file_path)

# Decode a file
xml_data = schema.to_dict(xml_file_path)

def flatten_dict(nested_dict, parent_key='', sep='_'):
    flat_dict = {}
    for key, value in nested_dict.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flat_dict.update(flatten_dict(value, new_key, sep=sep))
        else:
            flat_dict[new_key] = value\
    return flat_dict

xml_data_flat = flatten_dict(xml_data)

print(xml_data_flat)

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(xml_data_flat, orient='index')
# Display the DataFrame
print(df)


