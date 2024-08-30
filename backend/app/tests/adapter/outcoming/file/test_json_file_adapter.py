from adapter.outcoming.file.json_file_adapter import JsonFileAdapter
import pytest
from unittest.mock import MagicMock, patch

from tools.utils import Utils


@pytest.fixture
def mock_filesystem():
    with patch("builtins.open", new_callable=MagicMock) as mock_open, patch(
        "os.path.exists", return_value=True
    ) as mock_exists, patch("os.remove") as mock_remove:
        yield mock_open, mock_exists, mock_remove


@pytest.fixture
def adapter():
    return JsonFileAdapter(file_path="/mock/path")


def test_save(mock_filesystem, adapter):
    mock_open, _, _ = mock_filesystem

    file_content = '{"database_name": "test_db"}'
    adapter.save(1, file_content)

    expected_path = "/mock/path/dic_schema_1.json"

    mock_open.assert_called_with(expected_path, "wb")
    mock_open.return_value.__enter__().write.assert_called_with(file_content)


def test_load(mock_filesystem, adapter):
    _, _, _ = mock_filesystem
    result = adapter.load(1)

    expected_path = "/mock/path/dic_schema_1.json"
    assert result == expected_path


def test_delete(mock_filesystem, adapter):
    _, mock_exists, mock_remove = mock_filesystem
    adapter.delete(1)

    expected_path = "/mock/path/dic_schema_1.json"
    mock_exists.assert_called_with(expected_path)
    mock_remove.assert_called_with(expected_path)


def test_get_preview_no_schema(adapter):
    with patch.object(Utils, "read_json_file_content", return_value=None):
        preview = adapter.get_preview(1)

    assert preview is None


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

    with patch.object(Utils, "read_json_file_content", return_value=schema):
        preview = adapter.get_preview(1)

    assert preview.database_name == "test_db"
    assert preview.database_description == "A test database"
    assert len(preview.tables) == 1
    assert preview.tables[0].name == "table1"
    assert preview.tables[0].description == "Test table"


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

    with patch.object(Utils, "read_json_file_content", return_value=schema):
        metadata = adapter.extract_index_metadata(1)

    assert len(metadata) == 1
    assert metadata[0] == {
        "table_name": "table1",
        "text": "Test table",
        "table_pos": 0,
        "column_description": "A column",
    }


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

    with patch.object(Utils, "read_json_file_content", return_value=schema):
        metadata = adapter.extract_schema_metadata(1, tuples)

    assert "Table schema: table1" in metadata
    assert "PRIMARY KEY: (column1)" in metadata
    assert "Table description: Test table" in metadata


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

    metadata = adapter.extract_schema_metadata(1, tuples)

    assert "FOREIGN KEYS:" in metadata
    assert "FOREIGN KEY table1 (column1) references table2 (column2)" in metadata
