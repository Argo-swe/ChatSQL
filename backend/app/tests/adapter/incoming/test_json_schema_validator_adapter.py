from pathlib import Path
from adapter.incoming.schema_validator.json_schema_validator_adapter import (
    JsonSchemaValidatorAdapter,
)
import pytest
from tools.utils import Utils


@pytest.fixture
def json_schema_validator_adapter():
    return JsonSchemaValidatorAdapter()


def test_validate(json_schema_validator_adapter):
    example_schema = Utils.read_json_file_content(
        Path(__file__).parent / "../../assets/example_schema.json"
    )
    result = json_schema_validator_adapter.validate(example_schema)
    assert result is True


def test_validate_wrong(json_schema_validator_adapter):
    wrong_schema = Utils.read_json_file_content(
        Path(__file__).parent / "../../assets/example_schema_wrong.json"
    )
    result = json_schema_validator_adapter.validate(wrong_schema)
    assert result is False


def test_validate_empty(json_schema_validator_adapter):
    empty_schema = None
    result = json_schema_validator_adapter.validate(empty_schema)
    assert result is False
