import xml.etree.ElementTree as ET
import pandas as pd
import re


def parse_xml_to_dataframe(xml_file_path, namespace=None):
    """
    Parse an XML file into a pandas DataFrame.

    Parameters:
    - xml_file_path (str): The path to the XML file to be parsed.
    - namespace (dict, optional): A dictionary containing namespace information. Default is None.

    Returns:
    - df (DataFrame): A pandas DataFrame containing the parsed XML data.

    This function parses the specified XML file into a pandas DataFrame. It traverses the XML tree recursively,
    extracting tag names, text content, IDs, and paths for each element in the XML file. The namespace parameter
    can be used to handle XML files with namespace prefixes. If provided, it should be a dictionary containing a
    'ns' key representing the namespace prefix. The function returns a pandas DataFrame where each row corresponds
    to a tag in the XML file, with columns representing tag name, text content, ID (if present), and path within
    the XML tree. Missing values in the DataFrame are filled with empty strings.
    """

    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # List to store dictionaries representing each tag
    xml_data = []

    # Function to recursively traverse the XML tree and extract data
    def extract_data(element, path=''):
        tag_without_namespace = element.tag.replace(
            namespace.get('ns', '') + '}', '') if namespace else element.tag
        data = {
            'tag': tag_without_namespace.replace("{", ""),
            'text': element.text.strip() if element.text else '',
            'id': element.get('id', None),
            'path': path + '/' + tag_without_namespace.replace('{', ''),
        }

        xml_data.append(data)

        for child in element:
            child_path = path + '/' + tag_without_namespace.replace(
                '{', '') if path else tag_without_namespace.replace('{', '')
            extract_data(child, child_path)

    # Start the recursive traversal from the root element
    extract_data(root)

    # Create a Pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(xml_data)

    return df.fillna('')


def shift_id_column(df):
    # NOTE: should only be applicable when namespace is the one for requiementes
    # FIXME: first value after shift is "None" instead of ""
    # FIXME: percaution with last value in column
    # Shift the values in the 'id' column down by one row
    df['id'] = df['id'].shift(periods=1)

    return df


def replace_tag_with_previous(df):
    # Iterate through the DataFrame
    for i in range(1, len(df)):
        # Check if the value in the "tag" column is "text_body"
        if df.loc[i, 'tag'] == 'text_body':
            # Replace it with the value from the previous row
            df.loc[i, 'tag'] = df.loc[i - 1, 'tag']

    return df


def delete_rows_with_missing_text(df):
    # Filter rows where the value in the "text" column is not missing or empty
    df = df[df['text'].notna() & (df['text'] != '')]

    return df


def merge_and_delete_items(df):
    i = 1
    while i < len(df):
        if df.iloc[i, df.columns.get_loc('tag')] == 'item':
            # Append the "text" value to the previous row's "text" with a new line
            df.iloc[i - 1, df.columns.get_loc('text')] += ' \n- ' + \
                df.iloc[i, df.columns.get_loc('text')]
            # Drop the current row
            df = df.drop(df.index[i]).reset_index(drop=True)
            # Reduce i by 1 to recheck the merged row in the next iteration
            i -= 1
        i += 1

    return df


def replace_multiple_spaces(df):
    # Apply regex to replace multiple spaces with a single space for each entry in the "text" column
    df['text'] = df['text'].apply(lambda x: re.sub(
        r'\s+', ' ', x) if isinstance(x, str) else x)

    return df


def process_xml_with_namespace(xml_file_path, namespace):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Check if the XML file has the specified namespace
    if root.tag.startswith('{%s}' % namespace['ns']):
        df = parse_xml_to_dataframe(xml_file_path, namespace)
        df = shift_id_column(df)
        df = replace_tag_with_previous(df)
        df = delete_rows_with_missing_text(df)
        df = merge_and_delete_items(df)
        df = replace_multiple_spaces(df)
        df = remove_rows_with_tag(df, 'modifier')
        return df
    else:
        # If not, print a message
        print("The XML file does not have the specified namespace.")


def remove_rows_with_tag(df, tag_value):
    """
    Removes rows from a DataFrame where the attribute 'tag' has the exact content specified.

    Parameters:
        df (DataFrame): The DataFrame from which rows will be removed.
        tag_value (str): The value of the 'tag' attribute to remove.

    Returns:
        DataFrame: A new DataFrame with rows removed where the 'tag' attribute matches the specified value.
    """
    # Filter out rows where the 'tag' attribute is not equal to the specified value
    filtered_df = df[df['tag'] != tag_value]
    return filtered_df
