from abc import ABC, abstractmethod
from models.responses.auth_response_dto import AuthResponseDto


class AuthenticationUseCase(ABC):

    @abstractmethod
    def login(self, username: str, password: str) -> AuthResponseDto:
        """Authenticate the user with the given username and password.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user attempting to log in.

        Returns:
            AuthResponseDto: The authentication response containing user details and tokens.
        """
        pass
