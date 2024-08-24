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
    # Create a mock session object
    return mocker.create_autospec(Session)


# Fixture to initialize the repository with the mocked session
@pytest.fixture
def dictionary_repository(mock_session):
    return SqlAlchemyDictionaryRepositoryAdapter(session=mock_session)


"""CREATE DICTIONARY TEST BATTERY"""

"""Test for successful dictionary creation"""


def test_create_dictionary_success(dictionary_repository, mock_session, mocker):
    # Given
    name = "New Dictionary"
    description = "A description for the new dictionary"

    # Create a mock dictionary instance that simulates the database model
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.name = name
    mock_dictionary.description = description

    # Mock the session's add, commit, and refresh methods
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # When
    result = dictionary_repository.create_dictionary(name, description)

    # Then
    # Check that the dictionary's properties were set correctly
    assert result.name == name
    assert result.description == description

    # Ensure that add, commit, and refresh were called correctly
    mock_session.add.assert_called_once_with(result)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(result)


"""Test for handling database commit failure during dictionary creation"""


def test_create_dictionary_commit_failure(dictionary_repository, mock_session, mocker):
    # Given
    name = "New Dictionary"
    description = "A description for the new dictionary"

    # Simulate a commit failure
    mock_session.commit.side_effect = Exception("Commit failed")

    # When/Then
    with pytest.raises(Exception, match="Commit failed"):
        dictionary_repository.create_dictionary(name, description)

    # Ensure that add was called but commit raised an exception
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

    # Ensure that refresh was never called due to the commit failure
    mock_session.refresh.assert_not_called()


"""Test for handling empty name or description"""


def test_create_dictionary_empty_name_or_description(
    dictionary_repository, mock_session
):
    # Given
    name = ""
    description = "A description without a name"

    # When/Then
    with pytest.raises(ValueError):
        dictionary_repository.create_dictionary(name, description)

    # Ensure that add, commit, and refresh were never called
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


"""UPDATE DICTIONARY TEST BATTERY"""


"""Test for updating a dictionary entry"""


def test_update_dictionary(dictionary_repository, mock_session, mocker):
    # Given
    dictionary_id = 1
    new_name = "Updated Name"
    new_description = "Updated Description"

    # Create a mock dictionary instance that will be returned by get_dictionary_by_id
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.id = dictionary_id
    mock_dictionary.name = "Old Name"
    mock_dictionary.description = "Old Description"

    # Mock the get_dictionary_by_id method to return the mock dictionary
    mocker.patch.object(
        dictionary_repository, "get_dictionary_by_id", return_value=mock_dictionary
    )

    # When
    result = dictionary_repository.update_dictionary(
        dictionary_id, new_name, new_description
    )

    # Then
    # Check that get_dictionary_by_id was called with the correct id
    dictionary_repository.get_dictionary_by_id.assert_called_once_with(dictionary_id)

    # Assert that the dictionary's name and description were updated
    assert mock_dictionary.name == new_name
    assert mock_dictionary.description == new_description

    # Ensure that commit and refresh were called
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_dictionary)

    # Check that the method returns the updated dictionary
    assert result == mock_dictionary


"""Test for handling database commit failure"""


def test_update_dictionary_commit_failure(dictionary_repository, mock_session, mocker):
    # Given
    dictionary_id = 1
    new_name = "Updated Name"
    new_description = "Updated Description"

    # Create a mock dictionary instance that will be returned by get_dictionary_by_id
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mock_dictionary.id = dictionary_id

    # Mock the get_dictionary_by_id method to return the mock dictionary
    mocker.patch.object(
        dictionary_repository, "get_dictionary_by_id", return_value=mock_dictionary
    )

    # Simulate a commit failure
    mock_session.commit.side_effect = Exception("Commit failed")

    # When/Then
    with pytest.raises(Exception, match="Commit failed"):
        dictionary_repository.update_dictionary(
            dictionary_id, new_name, new_description
        )

    # Ensure that commit was called but raised an exception
    mock_session.commit.assert_called_once()

    # Ensure that refresh was never called due to the commit failure
    mock_session.refresh.assert_not_called()


"""Test for updating a non-existent dictionary entry"""


def test_update_non_existent_dictionary(dictionary_repository, mock_session, mocker):
    # Given
    dictionary_id = 999  # Assume this ID does not exist
    new_name = "Updated Name"
    new_description = "Updated Description"

    # Mock get_dictionary_by_id to return None for a non-existent dictionary
    mocker.patch.object(
        dictionary_repository, "get_dictionary_by_id", return_value=None
    )

    # When/Then
    with pytest.raises(AttributeError):
        # Expecting an AttributeError since we're trying to update a None object
        dictionary_repository.update_dictionary(
            dictionary_id, new_name, new_description
        )

    # Ensure that commit was never called since the dictionary doesn't exist
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


"""DELETE DICTIONARY TEST BATTERY"""


"""Test for successful deletion of a dictionary"""


def test_delete_dictionary_success(dictionary_repository, mock_session, mocker):
    dictionary_id = 1

    # Create a mock dictionary instance to be returned by get_dictionary_by_id
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mocker.patch.object(
        dictionary_repository, "get_dictionary_by_id", return_value=mock_dictionary
    )

    # Call the delete method
    dictionary_repository.delete_dictionary(dictionary_id)

    # Ensure that get_dictionary_by_id was called with the correct ID
    dictionary_repository.get_dictionary_by_id.assert_called_once_with(dictionary_id)

    # Ensure that the delete and commit methods were called on the session
    mock_session.delete.assert_called_once_with(mock_dictionary)
    mock_session.commit.assert_called_once()


"""Test for trying to delete a non-existent dictionary"""


def test_delete_dictionary_non_existent(dictionary_repository, mock_session, mocker):
    dictionary_id = 1

    # Simulate get_dictionary_by_id returning None (dictionary does not exist)
    mocker.patch.object(
        dictionary_repository, "get_dictionary_by_id", return_value=None
    )

    # Call the delete method
    dictionary_repository.delete_dictionary(dictionary_id)

    # Ensure that get_dictionary_by_id was called with the correct ID
    dictionary_repository.get_dictionary_by_id.assert_called_once_with(dictionary_id)

    # Ensure that delete and commit were NOT called since the dictionary does not exist
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()


"""Test for handling database errors during deletion"""


def test_delete_dictionary_database_error(dictionary_repository, mock_session, mocker):
    dictionary_id = 1

    # Create a mock dictionary instance to be returned by get_dictionary_by_id
    mock_dictionary = mocker.create_autospec(Dictionaries, instance=True)
    mocker.patch.object(
        dictionary_repository, "get_dictionary_by_id", return_value=mock_dictionary
    )

    # Simulate an exception being raised when trying to delete the dictionary
    mock_session.delete.side_effect = Exception("Database error during deletion")

    # Call the delete method and catch the exception
    with pytest.raises(Exception, match="Database error during deletion"):
        dictionary_repository.delete_dictionary(dictionary_id)

    # Ensure that delete was called, but commit was not called due to the exception
    mock_session.delete.assert_called_once_with(mock_dictionary)
    mock_session.commit.assert_not_called()
