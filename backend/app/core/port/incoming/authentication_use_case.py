from abc import ABC, abstractmethod
from models.responses.auth_response_dto import AuthResponseDto


class AuthenticationUseCase(ABC):

    @abstractmethod
    def login(self, username: str, password: str) -> AuthResponseDto:
        pass
