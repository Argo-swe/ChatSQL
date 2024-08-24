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
