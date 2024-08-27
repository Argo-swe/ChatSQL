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

    # Mock the __get_tuples method to return a non-empty list of tuples and an empty log content
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_tuples",
        return_value=([{"max_score": 0.9}], []),
    )
    # Mock the __get_relevant_tuples method to return a non-empty list of relevant tuples and an empty log content
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_relevant_tuples",
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

    # Mock the __get_tuples method to return an empty list of tuples and an empty log content
    mocker.patch.object(
        prompt_manager, "_TxtaiPromptManagerAdapter__get_tuples", return_value=([], [])
    )
    # Mock the __get_relevant_tuples method to return an empty list of relevant tuples and an empty log content
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_relevant_tuples",
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

    # Mock the __get_tuples method to return a non-empty list of tuples and log content for phase 1
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_tuples",
        return_value=([{"max_score": 0.9}], ["log content phase 1"]),
    )
    # Mock the __get_relevant_tuples method to return a non-empty list of relevant tuples and log content for phase 2
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_relevant_tuples",
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
    # 2. Mocking __get_tuples to return an empty list, simulating no results found.
    # 3. Mocking __get_relevant_tuples to return an empty list as well, since no tuples are relevant.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager, "_TxtaiPromptManagerAdapter__get_tuples", return_value=([], [])
    )
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_relevant_tuples",
        return_value=([], []),
    )

    # Call the prompt_generator method with the empty user request.
    result, log_content = prompt_manager.prompt_generator(dictionary_id, user_request)

    # Assert that the result message indicates no relevant results were found.
    # This verifies that the method handles empty user inputs gracefully.
    assert result is None


"""Test for different languages"""


def test_prompt_generator_different_language(
    prompt_manager, mocker, mock_file_repository
):
    dictionary_id = 1
    user_request = "Sample request"
    lang = "spanish"  # Testing with a different language to ensure the language setting works correctly.

    # Mocking dependencies:
    # 1. Mocking load_index to avoid loading an actual index.
    # 2. Mocking __get_tuples to simulate finding a relevant tuple.
    # 3. Mocking __get_relevant_tuples to return a relevant tuple.
    # 4. Mocking extract_schema_metadata to return a controlled schema metadata string.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_tuples",
        return_value=([{"max_score": 0.9}], []),
    )
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_relevant_tuples",
        return_value=([{"max_score": 0.9}], []),
    )
    mock_file_repository.extract_schema_metadata.return_value = "Mocked schema metadata"

    # Call the prompt_generator method with the specific language parameter.
    result, log_content = prompt_manager.prompt_generator(
        dictionary_id, user_request, lang=lang
    )

    # Assert that the generated prompt string correctly includes the language setting.
    # This verifies that the prompt is generated in the specified language.
    assert (
        f"Answer in {lang}." in result
    )  # Ensure the language setting is reflected in the output


"""Test for different DBMS"""


def test_prompt_generator_different_dbms(prompt_manager, mocker, mock_file_repository):
    dictionary_id = 1
    user_request = "Sample request"
    dbms = "PostgreSQL"  # Testing with a different DBMS to ensure the DBMS setting works correctly.

    # Mocking dependencies:
    # 1. Mocking load_index to prevent actual loading of indexes.
    # 2. Mocking __get_tuples to simulate a search result.
    # 3. Mocking __get_relevant_tuples to return a relevant tuple.
    # 4. Mocking extract_schema_metadata to return controlled schema metadata.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_tuples",
        return_value=([{"max_score": 0.9}], []),
    )
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_relevant_tuples",
        return_value=([{"max_score": 0.9}], []),
    )
    mock_file_repository.extract_schema_metadata.return_value = "Mocked schema metadata"

    # Call the prompt_generator method with the specific DBMS parameter.
    result, log_content = prompt_manager.prompt_generator(
        dictionary_id, user_request, dbms=dbms
    )

    # Assert that the generated prompt string correctly includes the DBMS setting.
    # This verifies that the prompt is tailored for the specified DBMS.
    assert (
        f"Convert user request to a suitable SQL query for {dbms}." in result
    )  # Ensure the DBMS setting is reflected in the output


"""Test for file repository failure handling"""


def test_prompt_generator_file_repository_failure(
    prompt_manager, mocker, mock_file_repository
):
    dictionary_id = 1
    user_request = "Sample request"

    # Mocking dependencies:
    # 1. Mocking load_index to avoid any actual index loading.
    # 2. Mocking __get_tuples to return a simulated relevant tuple.
    # 3. Mocking __get_relevant_tuples to return a simulated relevant tuple.
    mocker.patch.object(prompt_manager._index_manager, "load_index", return_value=None)
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_tuples",
        return_value=([{"max_score": 0.9}], []),
    )
    mocker.patch.object(
        prompt_manager,
        "_TxtaiPromptManagerAdapter__get_relevant_tuples",
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
        result, log_content = prompt_manager.prompt_generator(
            dictionary_id, user_request
        )
        # If the method doesn't raise an exception, check the result.
        # Typically, you'd assert that an error message or specific handling occurs.
        assert (
            "Error" in result
        )  # This assertion checks if an error message is returned.
    except Exception as e:
        # If an exception is caught, ensure it's the expected one.
        assert str(e) == "Error extracting schema metadata"


"""GETTING TUPLES TEST BATTERY"""


"""Test for correct SQL query formation and search execution"""


def test_get_tuples_sql_query_and_search_execution(mocker, prompt_manager):
    user_request = "Sample request"
    activate_log = False

    # Mock the search method in the embeddings object
    mock_search = mocker.patch.object(
        prompt_manager._index_manager.get_embeddings(),
        "search",
        return_value=[{"table_name": "SampleTable"}],
    )

    # Call the __get_tuples method
    tuples, log_content = prompt_manager._TxtaiPromptManagerAdapter__get_tuples(
        user_request, activate_log
    )

    # Construct the expected SQL query
    query_limit = 20
    expected_sql_query = f"""
        SELECT table_name, text, table_pos, column_description, MAX(score) AS max_score, AVG(score) AS avg_score
        FROM txtai WHERE
        similar(':x', 'table_description') AND
        similar(':x', 'column_description') AND
        score >= 0.2
        GROUP BY table_name
        HAVING max_score >= 0.3 OR avg_score >= 0.28
        ORDER BY max_score DESC
        LIMIT {query_limit}
    """

    # Normalize the SQL queries by stripping leading/trailing spaces and removing excess indentation
    def normalize_sql_query(query):
        return " ".join(query.strip().split())

    expected_sql_query = normalize_sql_query(expected_sql_query)
    actual_sql_query = normalize_sql_query(
        mock_search.call_args[0][0]
    )  # The first argument in the call to search

    # Assert that the actual SQL query matches the expected SQL query after normalization
    assert actual_sql_query == expected_sql_query

    # Also ensure that other parameters passed to the search method are correct
    mock_search.assert_called_once_with(
        mock_search.call_args[0][0],
        limit=query_limit * 10,
        parameters={"x": user_request},
    )

    # Assert that the method returns the correct tuples and no log content
    assert tuples == [{"table_name": "SampleTable"}]
    assert log_content is None


"""Test for logging activation"""


def test_get_tuples_logging_activation(mocker, prompt_manager):
    user_request = "Sample request"
    activate_log = True

    # Mock the search method to return sample tuples
    mock_search = mocker.patch.object(
        prompt_manager._index_manager.get_embeddings(),
        "search",
        return_value=[{"table_name": "SampleTable"}],
    )

    # Mock the semantic_search_log method in the debug manager
    mock_log = mocker.patch.object(
        prompt_manager._debug_manager,
        "semantic_search_log",
        return_value=["Log content"],
    )

    # Call the __get_tuples method with logging activated
    tuples, log_content = prompt_manager._TxtaiPromptManagerAdapter__get_tuples(
        user_request, activate_log
    )

    # Assert that the log content is generated using the semantic_search_log method
    mock_log.assert_called_once_with(user_request, [{"table_name": "SampleTable"}])

    # Assert that the method returns the correct tuples and log content
    assert tuples == [{"table_name": "SampleTable"}]
    assert log_content == ["Log content"]


"""Test for handling empty search results"""


def test_get_tuples_empty_search_results(mocker, prompt_manager):
    user_request = "Sample request"
    activate_log = False

    # Mock the search method to return no tuples
    mock_search = mocker.patch.object(
        prompt_manager._index_manager.get_embeddings(), "search", return_value=[]
    )

    # Call the __get_tuples method
    tuples, log_content = prompt_manager._TxtaiPromptManagerAdapter__get_tuples(
        user_request, activate_log
    )

    # Assert that the method returns an empty list and no log content
    assert tuples == []
    assert log_content is None


"""GETTING RELEVANT TUPLES TEST BATTERY"""

"""Test for keeping tuples with high scores"""


def test_get_relevant_tuples_keep_high_scores(mocker, prompt_manager):
    # This test ensures that tuples with high scores are kept.
    tuples = [
        {
            "table_name": "Table1",
            "max_score": 0.5,
        },  # This tuple should be kept because its score >= 0.45
        {
            "table_name": "Table2",
            "max_score": 0.6,
        },  # This tuple should also be kept due to a high score
        {
            "table_name": "Table3",
            "max_score": 0.4,
        },  # This tuple should be kept due to scoring distance
    ]
    activate_log = False  # Logging is disabled for this test

    # Call the __get_relevant_tuples method
    relevant_tuples, log_content = (
        prompt_manager._TxtaiPromptManagerAdapter__get_relevant_tuples(
            tuples, activate_log
        )
    )

    # Assert that all tuples are kept
    assert relevant_tuples == [
        {"table_name": "Table1", "max_score": 0.5},
        {"table_name": "Table2", "max_score": 0.6},
        {
            "table_name": "Table3",
            "max_score": 0.4,
        },  # This should be kept due to scoring distance
    ]
    assert log_content == []  # No logging should occur since activate_log is False


"""Test for keeping and discarding based on scoring distance"""


def test_get_relevant_tuples_keep_based_on_scoring_distance(mocker, prompt_manager):
    # This test verifies that tuples are kept or discarded based on scoring distance.
    tuples = [
        {"table_name": "Table1", "max_score": 0.5},  # This tuple should be kept
        {
            "table_name": "Table2",
            "max_score": 0.4,
        },  # This tuple should be kept due to scoring distance
        {
            "table_name": "Table3",
            "max_score": 0.1,
        },  # This tuple should be discarded due to a large scoring distance
    ]
    activate_log = False  # Logging is disabled for this test

    # Call the __get_relevant_tuples method
    relevant_tuples, log_content = (
        prompt_manager._TxtaiPromptManagerAdapter__get_relevant_tuples(
            tuples, activate_log
        )
    )

    # Assert that only the first two tuples are kept
    assert relevant_tuples == [
        {"table_name": "Table1", "max_score": 0.5},
        {"table_name": "Table2", "max_score": 0.4},
    ]
    assert log_content == []  # No logging should occur since activate_log is False


"""Test for generating log content"""


def test_get_relevant_tuples_with_logging(mocker, prompt_manager):
    # This test checks if log content is generated when logging is activated.
    tuples = [
        {"table_name": "Table1", "max_score": 0.5},
        {"table_name": "Table2", "max_score": 0.6},
    ]
    activate_log = True  # Logging is enabled for this test

    # Mock the semantic_search_log_custom_algorithm method to return a predefined log
    mock_log = mocker.patch.object(
        prompt_manager._debug_manager,
        "semantic_search_log_custom_algorithm",
        return_value=["Log entry 1", "Log entry 2"],
    )

    # Call the __get_relevant_tuples method
    relevant_tuples, log_content = (
        prompt_manager._TxtaiPromptManagerAdapter__get_relevant_tuples(
            tuples, activate_log
        )
    )

    # Assert that all tuples are considered relevant
    assert relevant_tuples == tuples

    # Assert that the log content is generated correctly
    assert log_content == ["Log entry 1", "Log entry 2"]
    mock_log.assert_called_once_with(
        relevant_tuples, tuples
    )  # Ensure the logging method was called correctly


"""Test for an empty tuple list"""


def test_get_relevant_tuples_empty_list(prompt_manager):
    # This test ensures that an empty list of tuples returns no relevant tuples and no log content.
    tuples = []  # Empty list of tuples
    activate_log = False  # Logging is disabled for this test

    # Call the __get_relevant_tuples method
    relevant_tuples, log_content = (
        prompt_manager._TxtaiPromptManagerAdapter__get_relevant_tuples(
            tuples, activate_log
        )
    )

    # Assert that no relevant tuples are returned and no log content is generated
    assert relevant_tuples == []
    assert log_content == []


"""Test for a list with a single tuple"""


def test_get_relevant_tuples_single_tuple(prompt_manager):
    # This test checks that a single tuple is correctly returned as relevant.
    tuples = [{"table_name": "Table1", "max_score": 0.5}]  # Single tuple
    activate_log = False  # Logging is disabled for this test

    # Call the __get_relevant_tuples method
    relevant_tuples, log_content = (
        prompt_manager._TxtaiPromptManagerAdapter__get_relevant_tuples(
            tuples, activate_log
        )
    )

    # Assert that the single tuple is returned as relevant
    assert relevant_tuples == tuples
    assert log_content == []  # No logging should occur since activate_log is False
