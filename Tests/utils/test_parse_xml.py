# test_math_operations.py

from src.utils import parse_xml
import pandas as pd

# Define a sample XML file for testing purposes
xml_file_path = r"C:\dev\NLP2RE_Sandbox\data\test_data\sample.xml"


def test_parse_xml_to_dataframe():

    # Parse the XML file
    df = parse_xml.parse_xml_to_dataframe(xml_file_path)

    # Define expected DataFrame
    expected_df = pd.DataFrame({
        'tag': ['root', 'item', 'name', 'price', 'item', 'name', 'price'],
        'text': ['', '', 'Item 1', '10.00', '', 'Item 2', '20.00'],
        'id': ['', '1', '', '', '2', '', ''],
        'path': ['/root', 'root/item', 'root/item/name', 'root/item/price', 'root/item', 'root/item/name', 'root/item/price']
    })
    # Assert that the DataFrame from the function matches the expected DataFrame
    pd.testing.assert_frame_equal(df, expected_df)


def test_shift_id_column():

    df = parse_xml.parse_xml_to_dataframe(xml_file_path)
    df = parse_xml.shift_id_column(df)

    # Define expected DataFrame
    expected_df = pd.DataFrame({
        'tag': ['root', 'item', 'name', 'price', 'item', 'name', 'price'],
        'text': ['', '', 'Item 1', '10.00', '', 'Item 2', '20.00'],
        'id': [None, '', '1', '', '', '2', ''],
        'path': ['/root', 'root/item', 'root/item/name', 'root/item/price', 'root/item', 'root/item/name', 'root/item/price']
    })
    # Assert that the DataFrame from the function matches the expected DataFrame
    pd.testing.assert_frame_equal(df, expected_df)


def test_replace_tag_with_previous():
    # TODO: ...
    pass


def test_delete_rows_with_missing_text():
    # TODO: ...
    pass


def test_merge_and_delete_items():
    # TODO: ...
    pass


def test_replace_multiple_spaces():
    # TODO: ...
    pass


def test_process_xml_with_namespace():
    # TODO: ...
    pass
