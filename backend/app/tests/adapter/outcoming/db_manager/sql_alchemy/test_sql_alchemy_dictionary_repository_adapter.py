import pytest
from sqlalchemy.orm import Session
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_dictionary_repository_adapter import (
    SqlAlchemyDictionaryRepositoryAdapter,
)
from models.dictionary_dto import DictionaryDto
from adapter.outcoming.db_manager.sql_alchemy.models import Dictionaries


# Fixture to mock the SQLAlchemy session
@pytest.fixture
def mock_session(mocker):
    # Create a mock session object to simulate database interactions
    return mocker.create_autospec(Session)


# Fixture to initialize the repository with the mocked session
@pytest.fixture
def dictionary_repository(mock_session):
    # Initialize the SqlAlchemyDictionaryRepositoryAdapter with the mocked session
    return SqlAlchemyDictionaryRepositoryAdapter(session=mock_session)


"""CREATE DICTIONARY TEST BATTERY"""

"""Test for successful dictionary creation"""


def test_create_dictionary_success(dictionary_repository, mock_session, mocker):
    name = "New Dictionary"
    description = "A description for the new dictionary"

    # Simulate a new dictionary instance and set its properties
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.name = name
    mock_dictionary.description = description

    # Mock the session's add, commit, and refresh methods to simulate a successful transaction
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Call the create_dictionary method
    result = dictionary_repository.create_dictionary(name, description)

    # Verify that the dictionary's properties were set correctly
    assert result.name == name
    assert result.description == description

    # Ensure that add, commit, and refresh were called as expected
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


"""Test for handling database commit failure during dictionary creation"""


def test_create_dictionary_commit_failure(dictionary_repository, mock_session, mocker):
    name = "New Dictionary"
    description = "A description for the new dictionary"

    # Simulate a commit failure by raising an exception
    mock_session.commit.side_effect = Exception("Commit failed")

    # Attempt to create a dictionary and expect an exception
    with pytest.raises(Exception, match="Commit failed"):
        dictionary_repository.create_dictionary(name, description)

    # Ensure that add was called but commit raised an exception
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

    # Verify that refresh was not called due to the commit failure
    mock_session.refresh.assert_not_called()


"""UPDATE DICTIONARY TEST BATTERY"""

"""Test for updating a dictionary entry"""


def test_update_dictionary(dictionary_repository, mock_session, mocker):
    dictionary_id = 1
    new_name = "Updated Name"
    new_description = "Updated Description"

    # Simulate an existing dictionary instance and set its initial properties
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.id = dictionary_id
    mock_dictionary.name = "Old Name"
    mock_dictionary.description = "Old Description"

    # Mock the query to return the mock dictionary
    mock_session.query(Dictionaries).filter().first.return_value = mock_dictionary

    # Call the update_dictionary method
    result = dictionary_repository.update_dictionary(
        dictionary_id, new_name, new_description
    )

    # Check that the dictionary's name and description were updated
    assert mock_dictionary.name == new_name
    assert mock_dictionary.description == new_description

    # Ensure that commit and refresh were called as expected
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_dictionary)

    # Verify that the method returns the updated dictionary
    assert isinstance(result, DictionaryDto)


"""Test for handling database commit failure"""


def test_update_dictionary_commit_failure(dictionary_repository, mock_session, mocker):
    dictionary_id = 1
    new_name = "Updated Name"
    new_description = "Updated Description"

    # Simulate an existing dictionary instance to be returned
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.id = dictionary_id
    mock_session.query(Dictionaries).filter().first.return_value = mock_dictionary

    # Simulate a commit failure by raising an exception
    mock_session.commit.side_effect = Exception("Commit failed")

    # Attempt to update the dictionary and expect an exception
    with pytest.raises(Exception, match="Commit failed"):
        dictionary_repository.update_dictionary(
            dictionary_id, new_name, new_description
        )

    # Ensure that commit was called but raised an exception
    mock_session.commit.assert_called_once()

    # Verify that refresh was not called due to the commit failure
    mock_session.refresh.assert_not_called()


"""Test for updating a non-existent dictionary entry"""


def test_update_non_existent_dictionary(dictionary_repository, mock_session, mocker):
    dictionary_id = 999  # Assume this ID does not exist
    new_name = "Updated Name"
    new_description = "Updated Description"

    # Mock the query to return None for a non-existent dictionary
    mock_session.query(Dictionaries).filter().first.return_value = None

    # Attempt to update a non-existent dictionary and expect a return value of None
    result = dictionary_repository.update_dictionary(
        dictionary_id, new_name, new_description
    )

    # Ensure that the result is None
    assert result is None

    # Verify that commit was not called since the dictionary doesn't exist
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


"""DELETE DICTIONARY TEST BATTERY"""

"""Test for successful deletion of a dictionary"""


def test_delete_dictionary_success(dictionary_repository, mock_session, mocker):
    dictionary_id = 1

    # Simulate an existing dictionary instance to be returned
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)

    # Mock the query to return the mock dictionary
    mock_session.query(Dictionaries).filter().first.return_value = mock_dictionary

    # Call the delete_dictionary method
    dictionary_repository.delete_dictionary(dictionary_id)

    # Verify that the query was called with the Dictionaries model
    mock_session.query.assert_called_with(Dictionaries)

    # Ensure that the delete and commit methods were called on the session
    mock_session.delete.assert_called_once_with(mock_dictionary)
    mock_session.commit.assert_called_once()


"""Test for trying to delete a non-existent dictionary"""


def test_delete_dictionary_non_existent(dictionary_repository, mock_session, mocker):
    dictionary_id = 1

    # Mock the query to return None for a non-existent dictionary
    mock_session.query(Dictionaries).filter().first.return_value = None

    # Call the delete_dictionary method
    dictionary_repository.delete_dictionary(dictionary_id)

    # Verify that the query was called to fetch the dictionary
    mock_session.query.assert_called_with(Dictionaries)

    # Ensure that delete and commit were NOT called since the dictionary does not exist
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()


"""Test for handling database errors during deletion"""


def test_delete_dictionary_database_error(dictionary_repository, mock_session, mocker):
    dictionary_id = 1

    # Mock the query to return the mock dictionary
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)

    # Mock the session query to return the mock dictionary
    mock_session.query(Dictionaries).filter().first.return_value = mock_dictionary

    # Simulate an exception being raised when trying to delete the dictionary
    mock_session.delete.side_effect = Exception("Database error during deletion")

    # Attempt to delete the dictionary and expect an exception
    with pytest.raises(Exception, match="Database error during deletion"):
        dictionary_repository.delete_dictionary(dictionary_id)

    # Ensure that the query was called to fetch the dictionary
    mock_session.query.assert_called_with(Dictionaries)

    # Ensure that delete was called, but commit was not called due to the exception
    mock_session.delete.assert_called_once_with(mock_dictionary)
    mock_session.commit.assert_not_called()


"""Test to ensure commit is always called after deletion"""


def test_delete_dictionary_ensure_commit_called(
    dictionary_repository, mock_session, mocker
):
    dictionary_id = 1

    # Simulate an existing dictionary instance to be returned
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_session.query(Dictionaries).filter().first.return_value = mock_dictionary

    # Call the delete_dictionary method
    dictionary_repository.delete_dictionary(dictionary_id)

    # Verify that commit is called after deletion
    mock_session.commit.assert_called_once()


"""GETTERS TEST BATTERY"""

"""Test for get_all_dictionaries"""


def test_get_all_dictionaries(dictionary_repository, mock_session, mocker):
    # Create mock dictionaries with the necessary attributes
    mock_dictionaries = []
    for i in range(3):
        mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
        mock_dictionary.id = i + 1
        mock_dictionary.name = f"Dictionary {i + 1}"
        mock_dictionary.description = f"Description for Dictionary {i + 1}"
        mock_dictionaries.append(mock_dictionary)

    # Mock the session query to return the list of mock dictionaries
    mock_session.query(Dictionaries).all.return_value = mock_dictionaries

    # Call the get_all_dictionaries method
    result = dictionary_repository.get_all_dictionaries()

    # Verify that the query was performed on the Dictionaries model
    mock_session.query.assert_any_call(Dictionaries)
    # Ensure that the all() method was called to fetch all results
    mock_session.query(Dictionaries).all.assert_called_once()
    # Ensure the result is a list of DictionaryDto instances
    assert isinstance(result, list)
    for dictionary in result:
        assert isinstance(dictionary, DictionaryDto)


"""Test for get_dictionary_by_id"""


def test_get_dictionary_by_id(dictionary_repository, mock_session, mocker):
    dictionary_id = 1
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.id = dictionary_id
    mock_dictionary.name = "Sample Dictionary"
    mock_dictionary.description = "A description"

    # Mock the query to return the mock dictionary
    mock_session.query(Dictionaries).filter().first.return_value = mock_dictionary

    # Call the get_dictionary_by_id method
    result = dictionary_repository.get_dictionary_by_id(dictionary_id)

    # Verify that the query was called with Dictionaries
    mock_session.query.assert_any_call(Dictionaries)

    # Check if filter was called with a condition involving the correct ID
    called_args, _ = mock_session.query(Dictionaries).filter.call_args
    assert called_args[0].left.name == "id"
    assert called_args[0].right.value == dictionary_id

    # Ensure that first() was called after the filter
    mock_session.query(Dictionaries).filter().first.assert_called_once()

    # Ensure the result is the expected DictionaryDto
    assert isinstance(result, DictionaryDto)


"""Test for get_dictionary_by_name"""


def test_get_dictionary_by_name(dictionary_repository, mock_session, mocker):
    dictionary_name = "SampleDictionary"
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.id = 1
    mock_dictionary.name = dictionary_name
    mock_dictionary.description = "A description"

    # Mock the query to return the mock dictionary
    mock_session.query(Dictionaries).filter().first.return_value = mock_dictionary

    # Call the get_dictionary_by_name method
    result = dictionary_repository.get_dictionary_by_name(dictionary_name)

    # Verify that the query was called with Dictionaries
    mock_session.query.assert_any_call(Dictionaries)

    # Check if filter was called with a condition involving the correct name
    called_args, _ = mock_session.query(Dictionaries).filter.call_args
    assert called_args[0].left.name == "name"
    assert called_args[0].right.value == dictionary_name

    # Ensure that first() was called after the filter
    mock_session.query(Dictionaries).filter().first.assert_called_once()

    # Ensure the result is the expected DictionaryDto
    assert isinstance(result, DictionaryDto)
