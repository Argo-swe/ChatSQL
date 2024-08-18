import pytest
import os
import shutil
import tempfile

# To avoid getting a Permission denied when accessing /opt/chatsql,
# we need to mock the makedirs method before importing the modules.
# Apply the mock before importing the module
os.makedirs = lambda *args, **kwargs: None  # Mock os.makedirs to do nothing


@pytest.fixture(scope="module")
def temp_dir():
    # Create a temporary directory for the test
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up the directory after the test
    shutil.rmtree(temp_dir)


_indexes_out_file_base_path = temp_dir  # Redirect the base path to a safe location

# Now import the module after the mocks are applied
from adapter.outcoming.embeddings.txtai.txtai_index_manager_adapter import (
    TxtaiIndexManagerAdapter,
)
from core.port.outcoming.file_repository import FileRepository
from txtai.embeddings import Embeddings


@pytest.fixture
def mock_file_repository(mocker):
    return mocker.MagicMock(spec=FileRepository)


@pytest.fixture
def txtai_index_manager(mock_file_repository):
    return TxtaiIndexManagerAdapter(file_repository=mock_file_repository)


""""Test for get_embeddings"""


def test_get_embeddings(txtai_index_manager):
    embeddings = txtai_index_manager.get_embeddings()
    assert isinstance(
        embeddings, Embeddings
    ), "get_embeddings should return an instance of Embeddings"


""""CREATE OR LOAD TEST BATTERY"""

"""Test for loading an existing index"""


def test_create_or_load_index_load_existing(mocker, txtai_index_manager):
    dictionary_id = 1
    mocker.patch("os.path.exists", return_value=True)
    mock_load_index = mocker.patch.object(txtai_index_manager, "load_index")

    result = txtai_index_manager.create_or_load_index(dictionary_id)

    assert result is False, "should return False when an existing index gets loaded"
    mock_load_index.assert_called_once_with(dictionary_id)


"""Test for creating index"""


def test_create_or_load_index_create_new(mocker, txtai_index_manager):
    dictionary_id = 1
    mocker.patch("os.path.exists", return_value=False)
    mock_create_index = mocker.patch.object(txtai_index_manager, "create_index")

    result = txtai_index_manager.create_or_load_index(dictionary_id)

    assert result is True, "should return True when an index is created"
    mock_create_index.assert_called_once_with(dictionary_id)
