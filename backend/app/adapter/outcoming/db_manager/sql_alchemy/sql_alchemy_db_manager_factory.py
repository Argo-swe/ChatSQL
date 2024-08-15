from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_authentication_repository_adapter import (
    SqlAlchemyAuthenticationRepositoryAdapter,
)
from adapter.outcoming.db_manager.sql_alchemy.sql_alchemy_dictionary_repository_adapter import (
    SqlAlchemyDictionaryRepositoryAdapter,
)
from core.port.outcoming.db_manager_abstract_factory import DbManagerAbstractFactory


class SqlAlchemyDbManagerFactory(DbManagerAbstractFactory):

    def create_authentication_repository(
        self,
    ) -> SqlAlchemyAuthenticationRepositoryAdapter:
        return SqlAlchemyAuthenticationRepositoryAdapter()

    def create_dictionary_repository(self) -> SqlAlchemyDictionaryRepositoryAdapter:
        return SqlAlchemyDictionaryRepositoryAdapter()
