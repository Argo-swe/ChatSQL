import pytest
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory import (
    SqlAlchemyDbManagerFactory,
)
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_authentication_repository_adapter import (
    SqlAlchemyAuthenticationRepositoryAdapter,
)
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_dictionary_repository_adapter import (
    SqlAlchemyDictionaryRepositoryAdapter,
)
from adapter.outcoming.db_manager.sql_alchemy import models
from adapter.outcoming.db_manager.sql_alchemy.base import engine


# Fixture to mock the SQLAlchemy engine and model creation
@pytest.fixture
def mock_sqlalchemy_engine(mocker):
    return mocker.patch.object(models.Base.metadata, "create_all")


"""CREATE AUTH REPOSITORY TEST BATTERY"""


"""Test for regular creation"""


def test_create_authentication_repository(mocker):
    # Given
    factory = SqlAlchemyDbManagerFactory()

    # Mock the SqlAlchemyAuthenticationRepositoryAdapter's constructor to track its instantiation
    mock_auth_repo_constructor = mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyAuthenticationRepositoryAdapter",
        side_effect=SqlAlchemyAuthenticationRepositoryAdapter,  # Ensure the real object is returned
    )

    # When calling create_authentication_repository
    auth_repo = factory.create_authentication_repository()

    # Then ensure the factory returns the correct repository instance
    mock_auth_repo_constructor.assert_called_once()
    assert isinstance(auth_repo, SqlAlchemyAuthenticationRepositoryAdapter)


"""CREATE DICTIONARY REPOSITORY TEST BATTERY"""


def test_create_dictionary_repository(mocker):
    # Given
    factory = SqlAlchemyDbManagerFactory()

    # Mock the SqlAlchemyDictionaryRepositoryAdapter's constructor to track its instantiation
    mock_dict_repo_constructor = mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyDictionaryRepositoryAdapter",
        side_effect=SqlAlchemyDictionaryRepositoryAdapter,  # Ensure the real object is returned
    )

    # When calling create_dictionary_repository
    dict_repo = factory.create_dictionary_repository()

    # Then ensure the factory returns the correct repository instance
    mock_dict_repo_constructor.assert_called_once()
    assert isinstance(dict_repo, SqlAlchemyDictionaryRepositoryAdapter)


"""Test creation with error"""


def test_create_dictionary_repository_with_error(mocker):
    # Given
    factory = SqlAlchemyDbManagerFactory()

    # Mock the constructor of SqlAlchemyDictionaryRepositoryAdapter to raise an exception
    mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyDictionaryRepositoryAdapter",
        side_effect=Exception("Failed to create repository"),
    )

    # When/Then
    with pytest.raises(Exception, match="Failed to create repository"):
        factory.create_dictionary_repository()


"""Test dictionary repository creation with multiple calls"""


def test_create_dictionary_repository_multiple_calls(mocker):
    # Given
    factory = SqlAlchemyDbManagerFactory()

    # Mock the constructor of SqlAlchemyDictionaryRepositoryAdapter to ensure it's called
    mock_dict_repo_constructor = mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyDictionaryRepositoryAdapter",
        side_effect=SqlAlchemyDictionaryRepositoryAdapter,
    )

    # When calling create_dictionary_repository multiple times
    dict_repo1 = factory.create_dictionary_repository()
    dict_repo2 = factory.create_dictionary_repository()

    # Then ensure that a new instance is created each time
    assert dict_repo1 is not dict_repo2
    assert mock_dict_repo_constructor.call_count == 2
