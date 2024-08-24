import pytest
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory import (
    SqlAlchemyDbManagerFactory,
)
from core.port.outcoming.db_manager_abstract_factory import DbManagerAbstractFactory
from adapter.outcoming.db_manager.db_manager_factory import DbManagerFactory


"""CREATION TEST BATTERY"""


"""Test for creating a SqlAlchemyDbManagerFactory instance"""


def test_create_sqlalchemy_db_manager_factory(mocker):
    # Given
    config = {"db_manager": "sqlalchemy"}

    # Mock the SqlAlchemyDbManagerFactory to track its instantiation
    mock_sqlalchemy_factory = mocker.patch(
        "adapter.outcoming.db_manager.db_manager_factory.SqlAlchemyDbManagerFactory",
        return_value=mocker.MagicMock(spec=SqlAlchemyDbManagerFactory),
    )

    # When
    result = DbManagerFactory.create(config)

    # Then
    # Ensure the factory method was called
    mock_sqlalchemy_factory.assert_called_once()

    # Ensure the result is an instance of SqlAlchemyDbManagerFactory
    assert isinstance(result, SqlAlchemyDbManagerFactory)


"""Test for unknown DB manager type, ensuring it raises a ValueError"""


def test_create_unknown_db_manager_type():
    # Given
    config = {"db_manager": "unknown"}

    # When/Then
    with pytest.raises(ValueError) as exc_info:
        DbManagerFactory.create(config)

    # Ensure the error message is correct
    assert str(exc_info.value) == "Unknown DB manager type: unknown"


"""Test for missing db_manager key, ensuring it raises a ValueError"""


def test_create_missing_db_manager_key():
    # Given
    config = {}  # No "db_manager" key provided

    # When/Then
    with pytest.raises(ValueError) as exc_info:
        DbManagerFactory.create(config)

    # Ensure the error message is correct for the default case
    assert str(exc_info.value) == "Unknown DB manager type: None"
