from adapter.outcoming.file.json_file_adapter import JsonFileAdapter
import pytest
from unittest.mock import MagicMock, patch

from tools.utils import Utils


# Fixture to mock the filesystem operations like open, os.path.exists, os.remove, and os.makedirs
@pytest.fixture
def mock_filesystem():
    # Mocks the 'open' function, 'os.path.exists', 'os.remove', and 'os.makedirs' functions
    with patch("builtins.open", new_callable=MagicMock) as mock_open, patch(
        "os.path.exists", return_value=True
    ) as mock_exists, patch("os.remove") as mock_remove, patch(
        "os.makedirs"
    ) as mock_makedirs:
        yield mock_open, mock_exists, mock_remove, mock_makedirs


# Fixture to create an instance of JsonFileAdapter with the mocked filesystem
@pytest.fixture
def adapter(mock_filesystem):
    # Initializes the JsonFileAdapter with a mock file path
    return JsonFileAdapter(file_path="/mock/path")


"""SAVE TEST BATTERY"""

"""Test for saving a file using the JsonFileAdapter"""


def test_save(mock_filesystem, adapter):
    # Extract the mock objects from the fixture
    mock_open, _, _, _ = mock_filesystem

    file_content = '{"database_name": "test_db"}'

    # Call the save method to simulate saving the file
    adapter.save(1, file_content)

    expected_path = "/mock/path/dic_schema_1.json"

    # Verify that the correct file was opened in write-binary mode
    mock_open.assert_called_with(expected_path, "wb")

    # Verify that the content was written to the file
    mock_open.return_value.__enter__().write.assert_called_with(file_content)


"""LOAD TEST BATTERY"""

"""Test for loading a file path using the JsonFileAdapter"""


def test_load(mock_filesystem, adapter):
    # Extract the mock objects from the fixture
    _, _, _, _ = mock_filesystem

    # Call the load method to get the file path
    result = adapter.load(1)

    expected_path = "/mock/path/dic_schema_1.json"

    # Verify that the returned file path is correct
    assert result == expected_path


"""DELETE TEST BATTERY"""

"""Test for deleting a file using the JsonFileAdapter"""


def test_delete(mock_filesystem, adapter):
    # Extract the mock objects from the fixture
    _, mock_exists, mock_remove, _ = mock_filesystem

    # Call the delete method to simulate file deletion
    adapter.delete(1)

    expected_path = "/mock/path/dic_schema_1.json"

    # Verify that the existence of the file was checked
    mock_exists.assert_called_with(expected_path)

    # Verify that the file was removed
    mock_remove.assert_called_with(expected_path)


"""GET PREVIEW TEST BATTERY"""

"""Test for getting a preview when no schema exists"""


def test_get_preview_no_schema(adapter):
    # Mock the Utils.read_json_file_content method to return None (no schema)
    with patch.object(Utils, "read_json_file_content", return_value=None):
        # Call get_preview and expect it to return None
        preview = adapter.get_preview(1)

    # Verify that the preview is None when no schema is found
    assert preview is None


"""Test for getting a preview with an existing schema"""


def test_get_preview_with_schema(adapter):
    schema = {
        "database_name": "test_db",
        "database_description": "A test database",
        "tables": [
            {
                "name": "table1",
                "description": "Test table",
                "columns": [{"name": "column1", "description": "A column"}],
            }
        ],
    }

    # Mock the Utils.read_json_file_content method to return the schema
    with patch.object(Utils, "read_json_file_content", return_value=schema):
        # Call get_preview to get the dictionary preview
        preview = adapter.get_preview(1)

    # Verify that the preview contains the correct database and table information
    assert preview.database_name == "test_db"
    assert preview.database_description == "A test database"
    assert len(preview.tables) == 1
    assert preview.tables[0].name == "table1"
    assert preview.tables[0].description == "Test table"


"""EXTRACT INDEX METADATA TEST BATTERY"""

"""Test for extracting index metadata from the schema"""


def test_extract_index_metadata(adapter):
    schema = {
        "tables": [
            {
                "name": "table1",
                "description": "Test table",
                "columns": [{"name": "column1", "description": "A column"}],
            }
        ]
    }

    # Mock the Utils.read_json_file_content method to return the schema
    with patch.object(Utils, "read_json_file_content", return_value=schema):
        # Call extract_index_metadata to get the index metadata
        metadata = adapter.extract_index_metadata(1)

    # Verify that the metadata is correctly extracted
    assert len(metadata) == 1
    assert metadata[0] == {
        "table_name": "table1",
        "text": "Test table",
        "table_pos": 0,
        "column_description": "A column",
    }


"""EXTRACT SCHEMA METADATA TEST BATTERY"""

"""Test for extracting schema metadata with a simple schema"""


def test_extract_schema_metadata(adapter):
    schema = {
        "tables": [
            {
                "name": "table1",
                "description": "Test table",
                "columns": [
                    {"name": "column1", "type": "VARCHAR", "description": "A column"}
                ],
                "primary_key": ["column1"],
            }
        ]
    }

    tuples = [{"table_pos": 0, "table_name": "table1"}]

    # Mock the Utils.read_json_file_content method to return the schema
    with patch.object(Utils, "read_json_file_content", return_value=schema):
        # Call extract_schema_metadata to get the schema metadata
        metadata = adapter.extract_schema_metadata(1, tuples)

    # Verify that the schema metadata is correctly extracted
    assert "Table schema: table1" in metadata
    assert "PRIMARY KEY: (column1)" in metadata
    assert "Table description: Test table" in metadata


"""Test for extracting schema metadata with foreign keys"""


@patch.object(
    Utils,
    "read_json_file_content",
    return_value={
        "tables": [
            {
                "name": "table1",
                "description": "Test table",
                "columns": [
                    {"name": "column1", "type": "VARCHAR", "description": "A column"}
                ],
                "primary_key": ["column1"],
                "foreign_keys": [
                    {
                        "foreign_key_column_names": ["column1"],
                        "reference_table_name": "table2",
                        "reference_column_names": ["column2"],
                    }
                ],
            }
        ]
    },
)
def test_extract_schema_metadata_with_foreign_keys(
    mock_read_json_file_content, adapter
):
    tuples = [{"table_pos": 0, "table_name": "table1"}]

    # Call extract_schema_metadata to get the schema metadata with foreign keys
    metadata = adapter.extract_schema_metadata(1, tuples)

    # Verify that the foreign keys are included in the schema metadata
    assert "FOREIGN KEYS:" in metadata
    assert "FOREIGN KEY table1 (column1) references table2 (column2)" in metadata
