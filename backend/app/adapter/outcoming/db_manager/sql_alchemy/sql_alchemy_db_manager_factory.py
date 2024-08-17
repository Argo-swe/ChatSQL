from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_authentication_repository_adapter import (
    SqlAlchemyAuthenticationRepositoryAdapter,
)
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_dictionary_repository_adapter import (
    SqlAlchemyDictionaryRepositoryAdapter,
)
from core.port.outcoming.db_manager_abstract_factory import DbManagerAbstractFactory

from adapter.outcoming.db_manager.sql_alchemy import models
from adapter.outcoming.db_manager.sql_alchemy.base import engine


class SqlAlchemyDbManagerFactory(DbManagerAbstractFactory):

    def __init__(self) -> None:
        super().__init__()
        models.Base.metadata.create_all(bind=engine)

    def create_authentication_repository(
        self,
    ) -> SqlAlchemyAuthenticationRepositoryAdapter:
        return SqlAlchemyAuthenticationRepositoryAdapter()

    def create_dictionary_repository(self) -> SqlAlchemyDictionaryRepositoryAdapter:
        return SqlAlchemyDictionaryRepositoryAdapter()
