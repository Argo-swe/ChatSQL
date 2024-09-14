import pytest
from adapter.outcoming.embeddings.txtai.txtai_index_manager_adapter import (
    TxtaiIndexManagerAdapter,
)
from adapter.outcoming.embeddings.txtai.txtai_prompt_manager_adapter import (
    TxtaiPromptManagerAdapter,
)
from core.port.outcoming.file_repository import FileRepository


# Fixture for mocking FileRepository
@pytest.fixture
def mock_file_repository(mocker):
    # Creates a mock object for the FileRepository to simulate its behavior
    return mocker.MagicMock(spec=FileRepository)


# Fixture for mocking TxtaiIndexManagerAdapter
@pytest.fixture
def mock_index_manager(mocker):
    # Creates a mock object for the TxtaiIndexManagerAdapter to simulate its behavior
    return mocker.MagicMock(spec=TxtaiIndexManagerAdapter)


# Fixture for creating an instance of TxtaiPromptManagerAdapter with mocked dependencies
@pytest.fixture
def prompt_manager(mock_index_manager, mock_file_repository):
    # Instantiates the TxtaiPromptManagerAdapter with mocked dependencies
    return TxtaiPromptManagerAdapter(
        index_manager=mock_index_manager, file_repository=mock_file_repository
    )


"""PROMPT GENERATION TEST BATTERY"""

"""Test for successful prompt generation"""


def test_prompt_generator_successful(prompt_manager, mocker, mock_file_repository):
    dictionary_id = 1
    user_request = "Sample request"

    # Mock the load_index method of the index manager to do nothing
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)

    # Mock the search_algorithm method to return a non-empty list of tuples and an empty log content
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "semantic_search",
        return_value=([{"max_score": 0}], []),
    )

    # Mock the search_filtering method to return a non-empty list of relevant tuples and an empty log content
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "search_filtering",
        return_value=([{"max_score": 0.9}], []),
    )

    # Mock the extract_schema_metadata method of the file repository to return a specific string
    mock_file_repository.extract_schema_metadata.return_value = "Mocked schema metadata"

    # Call the prompt_generator method with the mocked dependencies
    result, log_content = prompt_manager.prompt_generator(dictionary_id, user_request)

    # Assertions
    assert (
        "Mocked schema metadata" in result
    )  # Verify that the result contains the mocked schema metadata
    assert (
        "Sample request" in result
    )  # Verify that the result includes the user request
    assert (
        log_content is None
    )  # Verify that no log content is returned (since logging is not activated by default)


"""Test for no relevant results"""


def test_prompt_generator_no_relevant_results(prompt_manager, mocker):
    dictionary_id = 1
    user_request = "Sample request"

    # Mock the load_index method of the index manager to do nothing
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)

    # Mock the search_algorithm method to return an empty list of tuples and an empty log content
    mocker.patch.object(
        prompt_manager._search_algorithm, "semantic_search", return_value=([], [])
    )
    # Mock the search_filtering method to return an empty list of relevant tuples and an empty log content
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "search_filtering",
        return_value=([], []),
    )

    # Call the prompt_generator method with the mocked dependencies
    result, log_content = prompt_manager.prompt_generator(dictionary_id, user_request)

    # Assertions
    assert result is None  # Verify that the no results message is returned
    assert (
        log_content is None
    )  # Verify that no log content is returned (since logging is not activated by default)


"""Test with logging activated"""


def test_prompt_generator_with_logging(prompt_manager, mocker, mock_file_repository):
    dictionary_id = 1
    user_request = "Sample request"

    # Mock the load_index method of the index manager to do nothing
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)

    # Mock the search_algorithm method to return a non-empty list of tuples and log content for phase 1
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "semantic_search",
        return_value=([{"max_score": 0.9}], ["log content phase 1"]),
    )
    # Mock the search_filtering method to return a non-empty list of relevant tuples and log content for phase 2
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "search_filtering",
        return_value=([{"max_score": 0.9}], ["log content phase 2"]),
    )

    # Mock the extract_schema_metadata method of the file repository to return a specific string
    mock_file_repository.extract_schema_metadata.return_value = "Mocked schema metadata"

    # Call the prompt_generator method with logging activated
    result, log_content = prompt_manager.prompt_generator(
        dictionary_id, user_request, activate_log=True
    )

    # Assertions
    assert (
        "Mocked schema metadata" in result
    )  # Verify that the result contains the mocked schema metadata
    assert (
        "Sample request" in result
    )  # Verify that the result includes the user request
    assert (
        "log content phase 1" in log_content
    )  # Verify that the log content from phase 1 is included
    assert (
        "log content phase 2" in log_content
    )  # Verify that the log content from phase 2 is included


"""Test for empty user request"""


def test_prompt_generator_empty_user_request(prompt_manager, mocker):
    dictionary_id = 1
    user_request = (
        ""  # Empty request to simulate the scenario where the user provides no input.
    )

    # Mocking dependencies:
    # 1. Mocking load_index to ensure it does not perform any actual loading.
    # 2. Mocking semantic_search to return an empty list, simulating no results found.
    # 3. Mocking search_filtering to return an empty list as well, since no tuples are relevant.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager._search_algorithm, "semantic_search", return_value=([], [])
    )
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "search_filtering",
        return_value=([], []),
    )

    # Call the prompt_generator method with the empty user request.
    result = prompt_manager.prompt_generator(dictionary_id, user_request)

    # Assert that the result message indicates no relevant results were found.
    # This verifies that the method handles empty user inputs gracefully.
    assert result[0] is None


"""Test for different languages"""


def test_prompt_generator_different_language(
    prompt_manager, mocker, mock_file_repository
):
    dictionary_id = 1
    user_request = "Sample request"
    lang = "spanish"  # Testing with a different language to ensure the language setting works correctly.

    # Mocking dependencies:
    # 1. Mocking load_index to avoid loading an actual index.
    # 2. Mocking semantic_search to simulate finding a relevant tuple.
    # 3. Mocking search_filtering to return a relevant tuple.
    # 4. Mocking extract_schema_metadata to return a controlled schema metadata string.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "semantic_search",
        return_value=([{"max_score": 0.9}], []),
    )
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "search_filtering",
        return_value=([{"max_score": 0.9}], []),
    )
    mock_file_repository.extract_schema_metadata.return_value = "Mocked schema metadata"

    # Call the prompt_generator method with the specific language parameter.
    result = prompt_manager.prompt_generator(dictionary_id, user_request, lang=lang)

    # Assert that the generated prompt string correctly includes the language setting.
    # This verifies that the prompt is generated in the specified language.
    assert (
        f"Answer in {lang}." in result[0]
    )  # Ensure the language setting is reflected in the output


"""Test for different DBMS"""


def test_prompt_generator_different_dbms(prompt_manager, mocker, mock_file_repository):
    dictionary_id = 1
    user_request = "Sample request"
    dbms = "PostgreSQL"  # Testing with a different DBMS to ensure the DBMS setting works correctly.

    # Mocking dependencies:
    # 1. Mocking load_index to prevent actual loading of indexes.
    # 2. Mocking semantic_search to simulate a search result.
    # 3. Mocking search_filtering to return a relevant tuple.
    # 4. Mocking extract_schema_metadata to return controlled schema metadata.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "semantic_search",
        return_value=([{"max_score": 0.9}], []),
    )
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "search_filtering",
        return_value=([{"max_score": 0.9}], []),
    )
    mock_file_repository.extract_schema_metadata.return_value = "Mocked schema metadata"

    # Call the prompt_generator method with the specific DBMS parameter.
    result = prompt_manager.prompt_generator(dictionary_id, user_request, dbms=dbms)

    # Assert that the generated prompt string correctly includes the DBMS setting.
    # This verifies that the prompt is tailored for the specified DBMS.
    assert (
        f"Convert user request to a suitable SQL query for {dbms}." in result[0]
    )  # Ensure the DBMS setting is reflected in the output


"""Test for file repository failure handling"""


def test_prompt_generator_file_repository_failure(
    prompt_manager, mocker, mock_file_repository
):
    dictionary_id = 1
    user_request = "Sample request"

    # Mocking dependencies:
    # 1. Mocking load_index to avoid any actual index loading.
    # 2. Mocking semantic_search to return a simulated relevant tuple.
    # 3. Mocking search_filtering to return a simulated relevant tuple.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "semantic_search",
        return_value=([{"max_score": 0.9}], []),
    )
    mocker.patch.object(
        prompt_manager._search_algorithm,
        "search_filtering",
        return_value=([{"max_score": 0.9}], []),
    )

    # Simulating an exception being raised by the extract_schema_metadata method
    # to test how the prompt_generator handles such a failure scenario.
    mock_file_repository.extract_schema_metadata.side_effect = Exception(
        "Error extracting schema metadata"
    )

    # Try-except block to catch the exception raised by the method
    # and verify that it is correctly handled.
    try:
        result = prompt_manager.prompt_generator(dictionary_id, user_request)
        # If the method doesn't raise an exception, check the result.
        # Typically, you'd assert that an error message or specific handling occurs.
        assert (
            "Error" in result
        )  # This assertion checks if an error message is returned.
    except Exception as e:
        # If an exception is caught, ensure it's the expected one.
        assert str(e) == "Error extracting schema metadata"


"""Test for get_index_manager method"""


def test_get_index_manager(prompt_manager, mock_index_manager):
    # Call the get_index_manager method
    result = prompt_manager.get_index_manager()

    # Assert that the result is the same as the mocked index_manager
    assert result == mock_index_manager
