import pytest

# Now import the module after applying the mock and redirecting the base path
from adapter.outcoming.embeddings.txtai.txtai_index_manager_adapter import (
    TxtaiIndexManagerAdapter,
)
from adapter.outcoming.embeddings.txtai.txtai_prompt_manager_adapter import (
    TxtaiPromptManagerAdapter,
)
from adapter.outcoming.embeddings.txtai.txtai_embeddings_manager_factory import (
    TxtaiEmbeddingsManagerFactory,
)
from core.port.outcoming.file_repository import FileRepository


@pytest.fixture
def mock_file_repository(mocker):
    # Create a mock for the FileRepository interface to avoid actual file operations during testing
    return mocker.MagicMock(spec=FileRepository)


@pytest.fixture
def valid_config():
    # Provide a valid configuration dictionary required to create the TxtaiIndexManagerAdapter
    return {
        "txtai": {
            "embeddings_table_path": "some_table_path",
            "embeddings_columns_path": "some_columns_path",
        }
    }


@pytest.fixture
def invalid_config_missing_keys():
    # Provide an invalid configuration dictionary missing essential keys to test error handling
    return {
        "txtai": {
            # "embeddings_table_path" is missing, only "embeddings_columns_path" is present
            "embeddings_columns_path": "some_columns_path"
        }
    }


@pytest.fixture
def invalid_config_no_txtai_key():
    # Provide an invalid configuration dictionary missing the main "txtai" key to test error handling
    return {
        "some_other_key": {
            "embeddings_table_path": "some_table_path",
            "embeddings_columns_path": "some_columns_path",
        }
    }


"""TESTING CREATE_INDEX_MANAGER"""

"""Test for create_index_manager with valid configuration"""


def test_create_index_manager_success(valid_config, mock_file_repository):
    # Initialize the factory with a valid configuration
    factory = TxtaiEmbeddingsManagerFactory(valid_config)

    # Call the create_index_manager method to create an index manager
    index_manager = factory.create_index_manager(mock_file_repository)

    # Assert that the returned object is an instance of TxtaiIndexManagerAdapter
    assert isinstance(
        index_manager, TxtaiIndexManagerAdapter
    ), "Expected a TxtaiIndexManagerAdapter instance."


"""TESTING CREATE_PROMPT_MANAGER_WITH_DEPENDENCIES"""

"""Test for create_prompt_manager_with_dependencies with valid configuration"""


def test_create_prompt_manager_with_dependencies(valid_config, mock_file_repository):
    # Initialize the factory with a valid configuration
    factory = TxtaiEmbeddingsManagerFactory(valid_config)

    # Create an index manager to be used as a dependency
    index_manager = factory.create_index_manager(mock_file_repository)

    # Call the create_prompt_manager_with_dependencies method to create a prompt manager
    prompt_manager = factory.create_prompt_manager_with_dependencies(
        index_manager, mock_file_repository
    )

    # Assert that the returned object is an instance of TxtaiPromptManagerAdapter
    assert isinstance(
        prompt_manager, TxtaiPromptManagerAdapter
    ), "Expected a TxtaiPromptManagerAdapter instance."


"""TESTING CREATE_PROMPT_MANAGER"""

"""Test for create_prompt_manager with valid configuration"""


def test_create_prompt_manager(valid_config, mock_file_repository):
    # Initialize the factory with a valid configuration
    factory = TxtaiEmbeddingsManagerFactory(valid_config)

    # Call the create_prompt_manager method to create a prompt manager,
    # which also internally creates the index manager
    prompt_manager = factory.create_prompt_manager(mock_file_repository)

    # Assert that the returned object is an instance of TxtaiPromptManagerAdapter
    assert isinstance(
        prompt_manager, TxtaiPromptManagerAdapter
    ), "Expected a TxtaiPromptManagerAdapter instance."
