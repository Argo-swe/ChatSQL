import pytest
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory import (
    SqlAlchemyDbManagerFactory,
)
from core.port.outcoming.db_manager_abstract_factory import DbManagerAbstractFactory
from adapter.outcoming.db_manager.db_manager_factory import DbManagerFactory


"""CREATION TEST BATTERY"""


"""Test for creating a SqlAlchemyDbManagerFactory instance"""


def test_create_sqlalchemy_db_manager_factory(mocker):
    config = {
        "db_manager": "sqlalchemy"
    }  # Configuration specifying the use of SQLAlchemy as the DB manager

    # Mock the SqlAlchemyDbManagerFactory to track its instantiation
    # This mock ensures that when SqlAlchemyDbManagerFactory is called within the DbManagerFactory, we can verify it was called correctly.
    mock_sqlalchemy_factory = mocker.patch(
        "adapter.outcoming.db_manager.db_manager_factory.SqlAlchemyDbManagerFactory",
        return_value=mocker.MagicMock(spec=SqlAlchemyDbManagerFactory),
    )

    # Call the create method of DbManagerFactory with the configuration
    result = DbManagerFactory.create(config)

    # Ensure the factory method was called exactly once
    mock_sqlalchemy_factory.assert_called_once()

    # Ensure the result is an instance of SqlAlchemyDbManagerFactory
    # This verifies that the correct factory is instantiated based on the config
    assert isinstance(result, SqlAlchemyDbManagerFactory)


"""Test for unknown DB manager type, ensuring it raises a ValueError"""


def test_create_unknown_db_manager_type():
    config = {"db_manager": "unknown"}  # Configuration with an unknown DB manager type

    # Attempt to create a DB manager with an unknown type and expect a ValueError
    with pytest.raises(ValueError) as exc_info:
        DbManagerFactory.create(config)

    # Ensure the error message is correct and indicates the unknown type
    assert str(exc_info.value) == "Unknown DB manager type: unknown"


"""Test for missing db_manager key, ensuring it raises a ValueError"""


def test_create_missing_db_manager_key():
    config = {}  # Configuration without the "db_manager" key

    # Attempt to create a DB manager with a missing key and expect a ValueError
    with pytest.raises(ValueError) as exc_info:
        DbManagerFactory.create(config)

    # Ensure the error message is correct, indicating that the db_manager key was None
    assert str(exc_info.value) == "Unknown DB manager type: None"
