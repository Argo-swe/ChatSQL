import pytest
from adapter.outcoming.embeddings.txtai.txtai_debug_manager_adapter import (
    TxtaiDebugManagerAdapter,
)
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort


@pytest.fixture
def mock_index_manager(mocker):
    return mocker.MagicMock(IndexManagerPort)


@pytest.fixture
def txtai_debug_manager(mock_index_manager):
    return TxtaiDebugManagerAdapter(index_manager=mock_index_manager)


"""SEMANTIC SEARCH LOG TEST BATTERY"""

"""Test for empty tuple"""


def test_semantic_search_log_empty_tuples(txtai_debug_manager):
    user_request = "Test request"
    tuples = []

    result = txtai_debug_manager.semantic_search_log(user_request, tuples)

    # Check the presence of expected log content
    assert (
        "[ChatSQL] [DEBUG] - Details of the prompt generation process.\n" in result[0]
    )
    assert f"Request: {user_request}\n\n" in result[1]
    assert "[ChatSQL] [DEBUG] - Phase 1 - first extraction\n" in result[2]
    assert "List of relevant tables:\n" in result[3]
    assert "No relevant tables found.\n" in result[4]

    # Ensure the last entry is a newline or blank line
    assert result[-1] == "\n"


"""Test for a single tuple"""


def test_semantic_search_log_single_tuple(txtai_debug_manager, mock_index_manager):
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
    mock_index_manager.get_embeddings().explain.return_value = [
        {"tokens": [("term1", 0.8), ("term2", 0.7)]}
    ]

    result = txtai_debug_manager.semantic_search_log(user_request, tuples)

    # Print the result for debugging purposes
    for line in result:
        print(f"DEBUG: {line.strip()}")

    # Adjust assertions to match the actual format
    assert result[5].strip() == "Table 1 | TestTable: 0.9"
    assert result[6].strip() == "Description of the table: Sample text"
    assert result[7].strip() == "Ranking of the most relevant terms in the description:"
    assert result[8].strip() == "term1: 0.8"
    assert result[9].strip() == "term2: 0.7"
    assert (
        result[10].strip()
        == "Description of the most relevant column: Sample column description"
    )
    assert (
        result[11].strip() == "Ranking of the most relevant terms in the description:"
    )
    assert result[12].strip() == "term1: 0.8"
    assert result[13].strip() == "term2: 0.7"

    # Verify the correct call to the mock
    mock_index_manager.get_embeddings().explain.assert_any_call(
        user_request, ["Sample text"], limit=1
    )
    mock_index_manager.get_embeddings().explain.assert_any_call(
        user_request, ["Sample column description"], limit=1
    )


"""Test for multiple tuples"""


def test_semantic_search_log_multiple_tuples(txtai_debug_manager, mock_index_manager):
    user_request = "Test request"
    tuples = [
        {
            "table_name": "TestTable1",
            "max_score": 0.9,
            "text": "Sample text 1",
            "column_description": "Sample column description 1",
        },
        {
            "table_name": "TestTable2",
            "max_score": 0.8,
            "text": "Sample text 2",
            "column_description": "Sample column description 2",
        },
    ]

    # Mock the explain method return value for each tuple's text and column_description
    mock_index_manager.get_embeddings().explain.side_effect = [
        [{"tokens": [("term1", 0.8), ("term2", 0.7)]}],  # for "Sample text 1"
        [
            {"tokens": [("term3", 0.6), ("term4", 0.5)]}
        ],  # for "Sample column description 1"
        [{"tokens": [("term5", 0.4), ("term6", 0.3)]}],  # for "Sample text 2"
        [
            {"tokens": [("term7", 0.2), ("term8", 0.1)]}
        ],  # for "Sample column description 2"
    ]

    result = txtai_debug_manager.semantic_search_log(user_request, tuples)

    # Print the result for debugging purposes
    for line in result:
        print(f"DEBUG: {line.strip()}")

    # Assertions for the first tuple
    assert result[5].strip() == "Table 1 | TestTable1: 0.9"
    assert result[6].strip() == "Description of the table: Sample text 1"
    assert result[7].strip() == "Ranking of the most relevant terms in the description:"
    assert result[8].strip() == "term1: 0.8"
    assert result[9].strip() == "term2: 0.7"
    assert (
        result[10].strip()
        == "Description of the most relevant column: Sample column description 1"
    )
    assert (
        result[11].strip() == "Ranking of the most relevant terms in the description:"
    )
    assert result[12].strip() == "term3: 0.6"
    assert result[13].strip() == "term4: 0.5"

    # Assertions for the second tuple
    assert result[15].strip() == "Table 2 | TestTable2: 0.8"
    assert result[16].strip() == "Description of the table: Sample text 2"
    assert (
        result[17].strip() == "Ranking of the most relevant terms in the description:"
    )
    assert result[18].strip() == "term5: 0.4"
    assert result[19].strip() == "term6: 0.3"
    assert (
        result[20].strip()
        == "Description of the most relevant column: Sample column description 2"
    )
    assert (
        result[21].strip() == "Ranking of the most relevant terms in the description:"
    )
    assert result[22].strip() == "term7: 0.2"
    assert result[23].strip() == "term8: 0.1"

    # Verify the correct call to the mock
    mock_index_manager.get_embeddings().explain.assert_any_call(
        user_request, ["Sample text 1"], limit=1
    )
    mock_index_manager.get_embeddings().explain.assert_any_call(
        user_request, ["Sample column description 1"], limit=1
    )
    mock_index_manager.get_embeddings().explain.assert_any_call(
        user_request, ["Sample text 2"], limit=1
    )
    mock_index_manager.get_embeddings().explain.assert_any_call(
        user_request, ["Sample column description 2"], limit=1
    )


"""SEMANTIC SEARCH LOG CUSTOM ALGORITHM BATTERY"""

"""Test for empty tuples"""


def test_semantic_search_log_custom_algorithm_no_tuples(txtai_debug_manager):
    relevant_tuples = []
    tuples = []

    result = txtai_debug_manager.semantic_search_log_custom_algorithm(
        relevant_tuples, tuples
    )

    # Assert that the length of the result log is exactly 3 lines:
    # 1. The header indicating the start of phase 2
    # 2. The list of pertinent tables header
    # 3. The "No tables found." message
    assert len(result) == 3

    # Assert that the specific message "No tables found." appears in the third line of the log
    assert "No tables found." in result[2]


"""Test where all tables are kept"""


def test_semantic_search_log_custom_algorithm_all_kept(txtai_debug_manager):
    # Define a list of relevant_tuples where all tables have a max_score >= 0.45
    relevant_tuples = [
        {"table_name": "Table1", "max_score": 0.5},
        {"table_name": "Table2", "max_score": 0.6},
        {"table_name": "Table3", "max_score": 0.55},
    ]
    # In this test, the tuples list is identical to relevant_tuples
    tuples = relevant_tuples

    # Call the method being tested with the relevant tuples
    result = txtai_debug_manager.semantic_search_log_custom_algorithm(
        relevant_tuples, tuples
    )

    # Assert that each table is kept because their max_score is above the 0.45 threshold
    assert (
        "The table Table1 is kept because it has a sufficiently high score."
        in result[2]
    )
    assert (
        "The table Table2 is kept because it has a sufficiently high score."
        in result[3]
    )
    assert (
        "The table Table3 is kept because it has a sufficiently high score."
        in result[4]
    )

    # Verify that the log contains only the expected entries (no discard message)
    assert len(result) == 5  # 3 log entries for the tables + 2 header lines


"""Test where some tables are discarded"""


def test_semantic_search_log_custom_algorithm_some_discarded(txtai_debug_manager):
    # Define a list of relevant_tuples where the first table is kept, but the following tables should be discarded due to low max_score
    relevant_tuples = [
        {"table_name": "Table1", "max_score": 0.9},  # This table should be kept
        {"table_name": "Table2", "max_score": 0.4},  # This table should be discarded
        {"table_name": "Table3", "max_score": 0.35},  # This table should be discarded
    ]
    # In this test, the tuples list is identical to relevant_tuples
    tuples = relevant_tuples

    # Call the method being tested with the relevant tuples
    result = txtai_debug_manager.semantic_search_log_custom_algorithm(
        relevant_tuples, tuples
    )

    # Assert that the first table is kept because it has a sufficiently high score (>= 0.45)
    assert (
        "The table Table1 is kept because it has a sufficiently high score."
        in result[2]
    )

    # Assert that the remaining tables are discarded due to their low scores
    assert (
        "The remaining tables are discarded because the score is not high enough and the score difference with the previous tables is greater than 0.25."
        in result[3]
    )

    # Verify that the log contains only the expected entries (kept table + discard message)
    assert len(result) == 4  # 2 header lines + 1 kept message + 1 discard message


"""Test where the first table score is under 0.45"""


def test_semantic_search_log_custom_algorithm_first_underscore_table(
    txtai_debug_manager,
):
    # Define a list of relevant_tuples where the first table has a max_score below 0.45, but it is kept because the scoring distance (starting from 0) is within 0.25
    relevant_tuples = [
        {
            "table_name": "Table1",
            "max_score": 0.4,
        },  # Table1 should be kept due to scoring_distance <= 0.25
        {
            "table_name": "Table2",
            "max_score": 0.35,
        },  # Table2 should also be kept for the same reason
    ]
    # In this test, the tuples list is identical to relevant_tuples
    tuples = relevant_tuples

    # Call the method being tested with the relevant tuples
    result = txtai_debug_manager.semantic_search_log_custom_algorithm(
        relevant_tuples, tuples
    )

    # Assert that the first table is kept because the score difference is less than 0.25
    assert (
        "The table Table1 is kept because the score difference with the previous table is less than 0.25."
        in result[2]
    )

    # Assert that the second table is also kept due to a similar score difference
    assert (
        "The table Table2 is kept because the score difference with the previous table is less than 0.25."
        in result[3]
    )

    # Verify that the log contains only the expected entries (no discard message)
    assert len(result) == 4  # 2 header lines + 2 kept messages
