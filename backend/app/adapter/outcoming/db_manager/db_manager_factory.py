from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_db_manager_factory import (
    SqlAlchemyDbManagerFactory,
)
from core.port.outcoming.db_manager_abstract_factory import DbManagerAbstractFactory


class DbManagerFactory:
    @staticmethod
    def create(config: dict) -> DbManagerAbstractFactory:
        """Creates an instance of a database manager factory based on the configuration.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            DbManagerAbstractFactory: An instance of a class implementing the DbManagerAbstractFactory interface.

        Raises:
            ValueError: If the database manager type specified in the configuration is unknown or unsupported.
        """
        manager_type = config.get("db_manager")

        if manager_type == "sqlalchemy":
            return SqlAlchemyDbManagerFactory()
        else:
            raise ValueError(f"Unknown DB manager type: {manager_type}")
