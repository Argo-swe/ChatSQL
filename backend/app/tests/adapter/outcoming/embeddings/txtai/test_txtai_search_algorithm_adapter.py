import pytest
from adapter.outcoming.embeddings.txtai.txtai_search_algorithm_adapter import TxtaiSearchAlgorithmAdapter
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
import time

@pytest.fixture
def mock_index_manager(mocker):
    return mocker.MagicMock(IndexManagerPort)


@pytest.fixture
def txtai_search_algorithm(mock_index_manager):
    return TxtaiSearchAlgorithmAdapter(index_manager=mock_index_manager)


"""Test for successful semantic search with logging enabled"""
def test_semantic_search_with_logging(mocker, txtai_search_algorithm):
    user_request = "Sample request"
    activate_log = True

    # Mock the search method in the index manager's embeddings
    mock_search = mocker.patch.object(
        txtai_search_algorithm._index_manager.get_embeddings(),
        "search",
        return_value=[{"table_name": "SampleTable", "text": "sample text", "column_description": "sample column description", "max_score": 0.9}],
    )

    # Mock the explain method in the embeddings
    mock_explain = mocker.patch.object(
        txtai_search_algorithm._index_manager.get_embeddings(),
        "explain",
        return_value=[{"tokens": [("term1", 0.8), ("term2", 0.7)]}]
    )

    # Spy on the _semantic_search_log method to verify it's called when logging is activated
    mock_log = mocker.spy(txtai_search_algorithm, "_semantic_search_log")

    # Call the semantic_search method with logging activated
    tuples, log_content = txtai_search_algorithm.semantic_search(user_request, activate_log)

    # Assert that the search method was called with the correct arguments
    mock_search.assert_called_once()
    mock_explain.assert_called()

    # Assert that the _semantic_search_log method was called
    mock_log.assert_called_once_with(user_request, mock_search.return_value)

    # Normalize the log content by stripping whitespace from each line
    normalized_log_content = [line.strip() for line in log_content]

    # Assert that the method returns the correct tuples and log content
    assert tuples == [{"table_name": "SampleTable", "text": "sample text", "column_description": "sample column description", "max_score": 0.9}]

    # Assert that the token importance is in the log content
    assert any("term1: 0.8" in line for line in normalized_log_content)
    assert any("term2: 0.7" in line for line in normalized_log_content)


"""Test for filtering relevant tuples without logging"""
def test_search_filtering_without_logging(mocker, txtai_search_algorithm):
    tuples = [
        {"table_name": "Table1", "max_score": 0.5},
        {"table_name": "Table2", "max_score": 0.6},
        {"table_name": "Table3", "max_score": 0.4},
    ]
    activate_log = False

    # Call the search_filtering method without logging
    relevant_tuples, log_content = txtai_search_algorithm.search_filtering(tuples, activate_log)

    # Assert that the method filtered the tuples correctly
    assert relevant_tuples == [
        {"table_name": "Table1", "max_score": 0.5},
        {"table_name": "Table2", "max_score": 0.6},
        {"table_name": "Table3", "max_score": 0.4},
    ]

    # Assert that no log content is generated
    assert log_content == []


"""Test for generating semantic search log with no tuples"""
def test_semantic_search_log_no_tuples(txtai_search_algorithm):
    user_request = "Test request"
    tuples = []

    result = txtai_search_algorithm._semantic_search_log(user_request, tuples)

    # Normalize the result by stripping whitespace from each log line
    normalized_result = [line.strip() for line in result]

    # Assert that the log contains the correct message when no tuples are found
    assert any("No relevant tables found." in line for line in normalized_result)


"""Test for generating semantic search log with tuples"""
def test_semantic_search_log_with_tuples(mocker, txtai_search_algorithm):
    user_request = "Test request"
    tuples = [
        {
            "table_name": "TestTable",
            "max_score": 0.9,
            "text": "Sample text",
            "column_description": "Sample column description",
        }
    ]

    # Mock the explain method return value
    mocker.patch.object(
        txtai_search_algorithm._index_manager.get_embeddings(),
        "explain",
        return_value=[{"tokens": [("term1", 0.8), ("term2", 0.7)]}]
    )

    result = txtai_search_algorithm._semantic_search_log(user_request, tuples)

    # Normalize the result by stripping whitespace from each log line
    normalized_result = [line.strip() for line in result]

    # Assert that the log content includes relevant information
    assert any("Table 1 | TestTable: 0.9" in line for line in normalized_result)
    assert any("term1: 0.8" in line for line in normalized_result)
    assert any("term2: 0.7" in line for line in normalized_result)


"""Test for filtering log with no relevant tuples"""
def test_search_filtering_log_no_relevant_tuples(txtai_search_algorithm):
    relevant_tuples = []
    tuples = []

    result = txtai_search_algorithm._search_filtering_log(relevant_tuples, tuples)

    # Normalize the result by stripping whitespace from each log line
    normalized_result = [line.strip() for line in result]

    # Assert that the log contains the correct message when no tables are found
    assert any("No tables found." in line for line in normalized_result)


"""Test for filtering log with relevant tuples"""
def test_search_filtering_log_with_relevant_tuples(txtai_search_algorithm):
    relevant_tuples = [
        {"table_name": "Table1", "max_score": 0.9},
        {"table_name": "Table2", "max_score": 0.6},
    ]
    tuples = relevant_tuples

    result = txtai_search_algorithm._search_filtering_log(relevant_tuples, tuples)

    # Normalize the result by stripping whitespace from each log line
    normalized_result = [line.strip() for line in result]

    # Assert that the log contains relevant information about the kept tables
    assert any("The table Table1 is kept because it has a high score." in line for line in normalized_result)
    assert any("The table Table2 is kept because it has a high score." in line for line in normalized_result) 
    

def test_search_filtering_log_with_discarded_tuples(txtai_search_algorithm):
    relevant_tuples = [
        {"table_name": "Table1", "max_score": 0.9},  # This tuple should be kept
        {"table_name": "Table2", "max_score": 0.4},  # This tuple should be discarded (score difference > 0.2)
    ]
    tuples = relevant_tuples

    result = txtai_search_algorithm._search_filtering_log(relevant_tuples, tuples)

    # Normalize the result by stripping whitespace from each log line
    normalized_result = [line.strip() for line in result]

    # Assert that the log contains relevant information about the kept and discarded tables
    assert any("The table Table1 is kept because it has a high score." in line for line in normalized_result)
    assert any("The remaining tables are discarded because the score is not high enough and the score difference with the previous highly relevant tables is greater than 0.2." in line for line in normalized_result)


"""Test for generating debug header"""
def test_get_debug_header(txtai_search_algorithm):
    result = txtai_search_algorithm._TxtaiSearchAlgorithmAdapter__get_debug_header(level="INFO", system="TestSystem")
    
    # Assert that the log contains the correct format with INFO level and TestSystem
    assert "[TestSystem] [INFO]" in result
