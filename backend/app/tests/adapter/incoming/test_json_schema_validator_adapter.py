from unittest.mock import patch
from adapter.incoming.schema_validator.json_schema_validator_adapter import (
    JsonSchemaValidatorAdapter,
)
import pytest


@pytest.fixture
def mock_schema_file():
    return {
        "type": "object",
        "properties": {"name": {"type": "string"}, "description": {"type": "string"}},
        "required": ["name", "description"],
    }


@pytest.fixture
def valid_json():
    return '{"name": "Test", "description": "A valid description"}'


@pytest.fixture
def invalid_json():
    return '{"name": "Test"}'


def test_validate_success(mock_schema_file, valid_json):
    adapter = JsonSchemaValidatorAdapter()

    with patch(
        "tools.utils.Utils.read_json_file_content", return_value=mock_schema_file
    ):
        is_valid = adapter.validate(valid_json)
        assert is_valid is True


def test_validate_failure(mock_schema_file, invalid_json):
    adapter = JsonSchemaValidatorAdapter()

    with patch(
        "tools.utils.Utils.read_json_file_content", return_value=mock_schema_file
    ):
        is_valid = adapter.validate(invalid_json)
        assert is_valid is False


def test_validate_file_not_found():
    adapter = JsonSchemaValidatorAdapter()

    with pytest.raises(FileNotFoundError) as exc_info:
        with patch(
            "tools.utils.Utils.read_json_file_content", side_effect=FileNotFoundError
        ):
            is_valid = adapter.validate("{}")
            assert is_valid is False
