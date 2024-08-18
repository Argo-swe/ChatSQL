from abc import ABC, abstractmethod

from core.port.outcoming.authentication_repository import AuthenticationRepository
from core.port.outcoming.dictionary_repository import DictionaryRepository


class DbManagerAbstractFactory(ABC):

    @abstractmethod
    def create_authentication_repository(self) -> AuthenticationRepository:
        pass

    @abstractmethod
    def create_dictionary_repository(self) -> DictionaryRepository:
        pass
