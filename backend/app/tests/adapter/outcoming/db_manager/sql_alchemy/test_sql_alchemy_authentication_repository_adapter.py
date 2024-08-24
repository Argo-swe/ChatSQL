import pytest
from sqlalchemy.orm import Session
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_authentication_repository_adapter import (
    SqlAlchemyAuthenticationRepositoryAdapter,
)
from adapter.outcoming.db_manager.sql_alchemy.models import Admins


@pytest.fixture
def mock_session(mocker):
    return mocker.create_autospec(Session)


@pytest.fixture
def auth_repository(mock_session):
    return SqlAlchemyAuthenticationRepositoryAdapter(session=mock_session)


"""GET USER BY USERNAME TEST BATTERY"""


"""Test for retrieving an existing user by username"""


def test_get_user_by_username_existing_user(auth_repository, mock_session, mocker):
    # Given
    username = "existing_user"

    # Create a mock Admins instance that will be returned by the query
    mock_admin = mocker.create_autospec(Admins, instance=True)
    mock_admin.username = username
    mock_session.query(Admins).filter().first.return_value = mock_admin

    # When
    result = auth_repository.get_user_by_username(username)

    # Then
    # Ensure that the query was called with the correct filter
    mock_session.query.assert_any_call(Admins)  # Check that Admins was queried

    # Extract the actual call arguments to compare them more directly
    actual_filter_arg = mock_session.query(Admins).filter.call_args[0][0]

    # Assert that the filter argument matches the expected condition
    assert str(actual_filter_arg) == str(Admins.username == username)

    # Ensure that the method returns the correct admin instance
    assert result == mock_admin


"""Test for retrieving a non-existent user by username"""


def test_get_user_by_username_non_existent_user(auth_repository, mock_session, mocker):
    # Given
    username = "non_existent_user"

    # Simulate no user found by returning None
    mock_session.query(Admins).filter().first.return_value = None

    # When
    result = auth_repository.get_user_by_username(username)

    # Then
    # Ensure that the query was called with the correct filter
    mock_session.query.assert_any_call(Admins)

    # Extract the actual call arguments to compare them more directly
    actual_filter_arg = mock_session.query(Admins).filter.call_args[0][0]

    # Assert that the filter argument matches the expected condition
    assert str(actual_filter_arg) == str(Admins.username == username)

    # Ensure that the method returns None for a non-existent user
    assert result is None
