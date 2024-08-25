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
    # Mock the create_all method to prevent actual database interactions during tests
    return mocker.patch.object(models.Base.metadata, "create_all")


"""CREATE AUTH REPOSITORY TEST BATTERY"""

"""Test for regular creation of the authentication repository"""


def test_create_authentication_repository(mocker):
    config = SqlAlchemyDbManagerFactory()

    # Mock the SqlAlchemyAuthenticationRepositoryAdapter's constructor to track its instantiation
    mock_auth_repo_constructor = mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyAuthenticationRepositoryAdapter",
        side_effect=SqlAlchemyAuthenticationRepositoryAdapter,  # Ensure the real object is returned
    )

    # Call the create_authentication_repository method
    auth_repo = config.create_authentication_repository()

    # Verify that the factory method returns the correct repository instance
    mock_auth_repo_constructor.assert_called_once()
    assert isinstance(auth_repo, SqlAlchemyAuthenticationRepositoryAdapter)


"""Test for creation with error during authentication repository creation"""


def test_create_authentication_repository_with_error(mocker):
    config = SqlAlchemyDbManagerFactory()

    # Mock the constructor of SqlAlchemyAuthenticationRepositoryAdapter to raise an exception
    mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyAuthenticationRepositoryAdapter",
        side_effect=Exception("Failed to create authentication repository"),
    )

    # Attempt to create the authentication repository and expect an exception
    with pytest.raises(Exception, match="Failed to create authentication repository"):
        config.create_authentication_repository()


"""Test for verifying the correct repository type is returned"""


def test_create_authentication_repository_returns_correct_type():
    config = SqlAlchemyDbManagerFactory()

    # Create the authentication repository
    auth_repo = config.create_authentication_repository()

    # Ensure it returns an instance of SqlAlchemyAuthenticationRepositoryAdapter
    assert isinstance(auth_repo, SqlAlchemyAuthenticationRepositoryAdapter)


"""CREATE DICTIONARY REPOSITORY TEST BATTERY"""

"""Test for regular creation of the dictionary repository"""


def test_create_dictionary_repository(mocker):
    config = SqlAlchemyDbManagerFactory()

    # Mock the SqlAlchemyDictionaryRepositoryAdapter's constructor to track its instantiation
    mock_dict_repo_constructor = mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyDictionaryRepositoryAdapter",
        side_effect=SqlAlchemyDictionaryRepositoryAdapter,  # Ensure the real object is returned
    )

    # Call the create_dictionary_repository method
    dict_repo = config.create_dictionary_repository()

    # Verify that the factory method returns the correct repository instance
    mock_dict_repo_constructor.assert_called_once()
    assert isinstance(dict_repo, SqlAlchemyDictionaryRepositoryAdapter)


"""Test for creation with error during dictionary repository creation"""


def test_create_dictionary_repository_with_error(mocker):
    config = SqlAlchemyDbManagerFactory()

    # Mock the constructor of SqlAlchemyDictionaryRepositoryAdapter to raise an exception
    mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyDictionaryRepositoryAdapter",
        side_effect=Exception("Failed to create repository"),
    )

    # Attempt to create the dictionary repository and expect an exception
    with pytest.raises(Exception, match="Failed to create repository"):
        config.create_dictionary_repository()


"""Test for multiple calls to create_dictionary_repository"""


def test_create_dictionary_repository_multiple_calls(mocker):
    config = SqlAlchemyDbManagerFactory()

    # Mock the constructor of SqlAlchemyDictionaryRepositoryAdapter to ensure it's called
    mock_dict_repo_constructor = mocker.patch(
        "adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory.SqlAlchemyDictionaryRepositoryAdapter",
        side_effect=SqlAlchemyDictionaryRepositoryAdapter,
    )

    # Call create_dictionary_repository multiple times
    dict_repo1 = config.create_dictionary_repository()
    dict_repo2 = config.create_dictionary_repository()

    # Verify that a new instance is created each time
    assert dict_repo1 is not dict_repo2
    assert mock_dict_repo_constructor.call_count == 2


"""Test for verifying the correct repository type is returned"""


def test_create_dictionary_repository_returns_correct_type():
    config = SqlAlchemyDbManagerFactory()

    # Create the dictionary repository
    dict_repo = config.create_dictionary_repository()

    # Ensure it returns an instance of SqlAlchemyDictionaryRepositoryAdapter
    assert isinstance(dict_repo, SqlAlchemyDictionaryRepositoryAdapter)


"""INITIALIZATION LOGIC TEST"""

"""Test for ensuring the factory initialization calls create_all"""


def test_factory_initialization_calls_create_all(mocker):
    # Mock the create_all method to ensure it's called
    mock_create_all = mocker.patch.object(models.Base.metadata, "create_all")

    # Instantiate the factory, which triggers the __init__ method
    SqlAlchemyDbManagerFactory()

    # Verify that create_all is called with the engine
    mock_create_all.assert_called_once_with(bind=engine)
