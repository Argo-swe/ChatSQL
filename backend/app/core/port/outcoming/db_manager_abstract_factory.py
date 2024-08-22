from abc import ABC, abstractmethod

from core.port.outcoming.authentication_repository import AuthenticationRepository
from core.port.outcoming.dictionary_repository import DictionaryRepository


class DbManagerAbstractFactory(ABC):

    @abstractmethod
    def create_authentication_repository(self) -> AuthenticationRepository:
        """Create and return an instance of the AuthenticationRepository.

        Returns:
            AuthenticationRepository: An instance of a repository handling authentication data.
        """
        pass

    @abstractmethod
    def create_dictionary_repository(self) -> DictionaryRepository:
        """Create and return an instance of the DictionaryRepository.

        Returns:
            DictionaryRepository: An instance of a repository handling dictionary data.
        """
        pass
