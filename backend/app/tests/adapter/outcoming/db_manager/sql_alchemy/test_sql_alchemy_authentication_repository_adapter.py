import pytest
from sqlalchemy.orm import Session
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_authentication_repository_adapter import (
    SqlAlchemyAuthenticationRepositoryAdapter,
)
from adapter.outcoming.db_manager.sql_alchemy.models import Admins


# Fixture to mock the SQLAlchemy session
@pytest.fixture
def mock_session(mocker):
    # Create a mock object for the SQLAlchemy session to simulate database operations
    return mocker.create_autospec(Session)


# Fixture to initialize the authentication repository with the mocked session
@pytest.fixture
def auth_repository(mock_session):
    # Instantiate the SqlAlchemyAuthenticationRepositoryAdapter with the mocked session
    return SqlAlchemyAuthenticationRepositoryAdapter(session=mock_session)


"""GET USER BY USERNAME TEST BATTERY"""

"""Test for retrieving an existing user by username"""


def test_get_user_by_username_existing_user(auth_repository, mock_session, mocker):
    username = "existing_user"

    # Create a mock Admins instance that simulates the database model
    mock_admin = mocker.create_autospec(Admins, instance=True)
    mock_admin.username = username

    # Mock the query, filter, and first methods to return the mock_admin when queried
    mock_session.query(Admins).filter().first.return_value = mock_admin

    # Call the get_user_by_username method
    result = auth_repository.get_user_by_username(username)

    # Ensure that the query was performed on the Admins model
    mock_session.query.assert_any_call(Admins)

    # Extract the actual filter argument used in the query
    actual_filter_arg = mock_session.query(Admins).filter.call_args[0][0]

    # Assert that the filter argument matches the expected condition (Admins.username == username)
    assert str(actual_filter_arg) == str(Admins.username == username)

    # Ensure that the method returns the correct admin instance
    assert result == mock_admin


"""Test for retrieving a non-existent user by username"""


def test_get_user_by_username_non_existent_user(auth_repository, mock_session, mocker):
    username = "non_existent_user"

    # Mock the query, filter, and first methods to simulate no user found by returning None
    mock_session.query(Admins).filter().first.return_value = None

    # Call the get_user_by_username method
    result = auth_repository.get_user_by_username(username)

    # Ensure that the query was performed on the Admins model
    mock_session.query.assert_any_call(Admins)

    # Extract the actual filter argument used in the query
    actual_filter_arg = mock_session.query(Admins).filter.call_args[0][0]

    # Assert that the filter argument matches the expected condition (Admins.username == username)
    assert str(actual_filter_arg) == str(Admins.username == username)

    # Ensure that the method returns None for a non-existent user
    assert result is None
