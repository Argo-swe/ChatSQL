import json
from adapter.incoming.schema_validator.schema_validator_factory import (
    SchemaValidatorFactory,
)
from adapter.outcoming.db_manager.db_manager_factory import DbManagerFactory
from adapter.outcoming.file.file_factory import FileFactory
from adapter.outcoming.embeddings.embeddings_manager_factory import (
    EmbeddingsManagerFactory,
)
from core.service.authentication_service import AuthenticationService
from core.service.dictionary_service import DictionaryService
from core.service.prompt_manager_service import PromptManagerService


class Configuration:
    _instance = None

    # signleton implementation
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):

            try:
                with open("/opt/chatsql/config.json", "r") as file:
                    config = json.load(file)
            except FileNotFoundError:
                print("File not found")
            except json.JSONDecodeError:
                print("Error while decoding JSON file")

            self._config = config
            self._db_manager_factory = DbManagerFactory.create(self._config)
            self._embeddings_factory = EmbeddingsManagerFactory.create(self._config)
            self._file_repository = FileFactory.create(self._config)
            self._schema_validator = SchemaValidatorFactory.create(self._config)

            self._dictionary_repository = (
                self._db_manager_factory.create_dictionary_repository()
            )
            self._authentication_repository = (
                self._db_manager_factory.create_authentication_repository()
            )

            self._prompt_manager = self._embeddings_factory.create_prompt_manager(
                self._file_repository
            )

            self._dictionary_service = DictionaryService(
                self._dictionary_repository,
                self._prompt_manager.get_index_manager(),
                self._file_repository,
                self._schema_validator,
            )
            self._authentication_service = AuthenticationService(
                self._authentication_repository
            )
            self._prompt_manager_service = PromptManagerService(
                self._dictionary_service, self._prompt_manager
            )

            self._initialized = True

    def get_prompt_manager_service(self) -> PromptManagerService:
        return self._prompt_manager_service

    def get_dictionary_service(self) -> DictionaryService:
        return self._dictionary_service

    def get_authentication_service(self) -> AuthenticationService:
        return self._authentication_service
