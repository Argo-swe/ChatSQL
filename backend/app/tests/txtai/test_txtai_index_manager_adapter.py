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


# The base path for indexes is redirected to the temporary directory for testing
_indexes_out_file_base_path = temp_dir

# Now import the module after the mocks are applied
from adapter.outcoming.embeddings.txtai.txtai_index_manager_adapter import (
    TxtaiIndexManagerAdapter,
)
from core.port.outcoming.file_repository import FileRepository
from txtai.embeddings import Embeddings


# Mock the FileRepository to prevent actual file operations during tests
@pytest.fixture
def mock_file_repository(mocker):
    return mocker.MagicMock(spec=FileRepository)


# Create a fixture for the TxtaiIndexManagerAdapter with the mocked FileRepository
@pytest.fixture
def txtai_index_manager(mock_file_repository):
    return TxtaiIndexManagerAdapter(file_repository=mock_file_repository)


"""Test for get_embeddings"""


def test_get_embeddings(txtai_index_manager):
    # Ensure that the get_embeddings method returns an Embeddings instance
    embeddings = txtai_index_manager.get_embeddings()
    assert isinstance(
        embeddings, Embeddings
    ), "get_embeddings should return an instance of Embeddings"


"""CREATE OR LOAD TEST BATTERY"""

"""Test for loading an existing index"""


def test_create_or_load_index_load_existing(mocker, txtai_index_manager):
    dictionary_id = 1
    # Mock os.path.exists to simulate that the index already exists
    mocker.patch("os.path.exists", return_value=True)
    # Mock load_index to verify it is called
    mock_load_index = mocker.patch.object(txtai_index_manager, "load_index")

    # Call the method under test
    result = txtai_index_manager.create_or_load_index(dictionary_id)

    # Assert that the existing index is loaded, and the method returns False
    assert result is False, "should return False when an existing index gets loaded"
    mock_load_index.assert_called_once_with(dictionary_id)


"""Test for creating index when one does not exist"""


def test_create_or_load_index_create_new(mocker, txtai_index_manager):
    dictionary_id = 1
    # Mock os.path.exists to simulate that the index does not exist
    mocker.patch("os.path.exists", return_value=False)
    # Mock create_index to verify it is called
    mock_create_index = mocker.patch.object(txtai_index_manager, "create_index")

    # Call the method under test
    result = txtai_index_manager.create_or_load_index(dictionary_id)

    # Assert that a new index is created, and the method returns True
    assert result is True, "should return True when an index is created"
    mock_create_index.assert_called_once_with(dictionary_id)


"""Test for creating an index"""


def test_create_index(mocker, txtai_index_manager):
    dictionary_id = 1
    mock_documents = ["doc1", "doc2"]

    # Mock the extract_index_metadata method to return mock documents
    mocker.patch.object(
        txtai_index_manager._file_repository,
        "extract_index_metadata",
        return_value=mock_documents,
    )

    # Mock the embeddings.index method to avoid actual indexing
    mock_index = mocker.patch.object(txtai_index_manager._embeddings, "index")

    # Mock the save_index method to avoid actual saving
    mock_save_index = mocker.patch.object(txtai_index_manager, "save_index")

    # Call the method under test
    txtai_index_manager.create_index(dictionary_id)

    # Assert that the index method was called with the correct documents
    mock_index.assert_called_once_with([(0, "doc1", None), (1, "doc2", None)])

    # Assert that save_index was called since save_index=True by default
    mock_save_index.assert_called_once_with(dictionary_id)


"""Test for creating an index without saving it"""


def test_create_index_no_save(mocker, txtai_index_manager):
    dictionary_id = 1
    mock_documents = ["doc1", "doc2"]

    # Mock the extract_index_metadata method to return mock documents
    mocker.patch.object(
        txtai_index_manager._file_repository,
        "extract_index_metadata",
        return_value=mock_documents,
    )

    # Mock the embeddings.index method to avoid actual indexing
    mock_index = mocker.patch.object(txtai_index_manager._embeddings, "index")

    # Mock the save_index method to avoid actual saving
    mock_save_index = mocker.patch.object(txtai_index_manager, "save_index")

    # Call the method under test without saving the index
    txtai_index_manager.create_index(dictionary_id, save_index=False)

    # Assert that the index method was called with the correct documents
    mock_index.assert_called_once_with([(0, "doc1", None), (1, "doc2", None)])

    # Assert that save_index was NOT called since save_index=False
    mock_save_index.assert_not_called()


"""Test for saving an index"""


def test_save_index(mocker, txtai_index_manager):
    dictionary_id = 1

    # Mock the embeddings.save method to avoid actual saving
    mock_save = mocker.patch.object(txtai_index_manager._embeddings, "save")

    # Call the method under test
    txtai_index_manager.save_index(dictionary_id)

    # Assert that save was called with the correct file path
    mock_save.assert_called_once_with(
        txtai_index_manager._TxtaiIndexManagerAdapter__index_file_path(dictionary_id)
    )


"""Test for loading an index"""


def test_load_index(mocker, txtai_index_manager):
    dictionary_id = 1

    # Mock the embeddings.load method to avoid actual loading
    mock_load = mocker.patch.object(txtai_index_manager._embeddings, "load")

    # Call the method under test
    txtai_index_manager.load_index(dictionary_id)

    # Assert that load was called with the correct file path
    mock_load.assert_called_once_with(
        txtai_index_manager._TxtaiIndexManagerAdapter__index_file_path(dictionary_id)
    )


"""Test for deleting an index"""


def test_delete_index(mocker, txtai_index_manager):
    dictionary_id = 1

    # Mock the os.path.exists method to simulate that the directory exists
    mocker.patch("os.path.exists", return_value=True)

    # Mock the shutil.rmtree method to avoid actual deletion
    mock_rmtree = mocker.patch("shutil.rmtree")

    # Call the method under test
    txtai_index_manager.delete_index(dictionary_id)

    # Assert that rmtree was called with the correct directory path
    mock_rmtree.assert_called_once_with(
        txtai_index_manager._TxtaiIndexManagerAdapter__index_file_path(dictionary_id)
    )


"""TESTS FOR UNINTENDED BEHAVIOR"""

"""Test for creating an index with an empty document list"""


def test_create_index_empty_documents(mocker, txtai_index_manager):
    dictionary_id = 1
    mock_documents = []  # Empty document list

    # Mock the extract_index_metadata method to return an empty list
    mocker.patch.object(
        txtai_index_manager._file_repository,
        "extract_index_metadata",
        return_value=mock_documents,
    )

    # Mock the embeddings.index method to avoid actual indexing
    mock_index = mocker.patch.object(txtai_index_manager._embeddings, "index")

    # Mock the save_index method to avoid actual saving
    mock_save_index = mocker.patch.object(txtai_index_manager, "save_index")

    # Call the method under test
    txtai_index_manager.create_index(dictionary_id)

    # Assert that the index method was called with an empty list
    mock_index.assert_called_once_with([])

    # Assert that save_index was called even with an empty document list
    mock_save_index.assert_called_once_with(dictionary_id)


"""Test for delete_index when directory does not exist"""


def test_delete_index_non_existent(mocker, txtai_index_manager):
    dictionary_id = 1

    # Mock the os.path.exists method to simulate that the directory does not exist
    mocker.patch("os.path.exists", return_value=False)

    # Mock the shutil.rmtree method to avoid actual deletion
    mock_rmtree = mocker.patch("shutil.rmtree")

    # Call the method under test
    txtai_index_manager.delete_index(dictionary_id)

    # Assert that rmtree was NOT called since the directory does not exist
    mock_rmtree.assert_not_called()


"""Test for create_index failure during indexing"""


def test_create_index_failure_during_indexing(mocker, txtai_index_manager):
    dictionary_id = 1
    mock_documents = ["doc1", "doc2"]

    # Mock the extract_index_metadata method to return mock documents
    mocker.patch.object(
        txtai_index_manager._file_repository,
        "extract_index_metadata",
        return_value=mock_documents,
    )

    # Mock the embeddings.index method to raise an error
    mock_index = mocker.patch.object(
        txtai_index_manager._embeddings,
        "index",
        side_effect=RuntimeError("Indexing failed"),
    )

    # Mock the save_index method to avoid actual saving
    mock_save_index = mocker.patch.object(txtai_index_manager, "save_index")

    # Call the method under test and expect it to raise an error
    with pytest.raises(RuntimeError, match="Indexing failed"):
        txtai_index_manager.create_index(dictionary_id)

    # Assert that the index method was called and failed
    mock_index.assert_called_once_with([(0, "doc1", None), (1, "doc2", None)])

    # Assert that save_index was NOT called since indexing failed
    mock_save_index.assert_not_called()


"""Test for save_index failure"""


def test_save_index_failure(mocker, txtai_index_manager):
    dictionary_id = 1

    # Mock the embeddings.save method to raise an error
    mock_save = mocker.patch.object(
        txtai_index_manager._embeddings, "save", side_effect=RuntimeError("Save failed")
    )

    # Call the method under test and expect it to raise an error
    with pytest.raises(RuntimeError, match="Save failed"):
        txtai_index_manager.save_index(dictionary_id)

    # Assert that save was called and failed
    mock_save.assert_called_once_with(
        txtai_index_manager._TxtaiIndexManagerAdapter__index_file_path(dictionary_id)
    )