import pytest
from adapter.outcoming.file.json_file_adapter import JsonFileAdapter
from core.port.outcoming.file_repository import FileRepository
from adapter.outcoming.file.file_factory import FileFactory


"""FILE FACTORY TEST BATTERY"""

"""Test for JSON file adapter creation"""


def test_create_json_file_adapter():
    # Configuration for creating a JSON file adapter
    config = {"file_type": "json"}

    # Create the file adapter using the factory
    file_adapter = FileFactory.create(config)

    # Check that the created object is an instance of JsonFileAdapter
    assert isinstance(file_adapter, JsonFileAdapter)
    assert isinstance(file_adapter, FileRepository)


"""Test for unknown file type"""


def test_create_unknown_file_type():
    # Configuration with an unknown file type
    config = {"file_type": "xml"}

    # Attempt to create the file adapter and expect a ValueError
    with pytest.raises(ValueError, match="Unknown file type: xml"):
        FileFactory.create(config)
