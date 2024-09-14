from routes.auth.jwt_handler import JwtHandler
from core.port.outcoming.authentication_repository import AuthenticationRepository
from models.responses.auth_response_dto import AuthResponseDto
from core.port.incoming.authentication_use_case import AuthenticationUseCase
from models.responses.response_dto import ResponseStatusEnum
from tools.exceptions import LoginError


class AuthenticationService(AuthenticationUseCase):
    def __init__(self, authentication_repository: AuthenticationRepository) -> None:
        """Initialize the AuthenticationService with an AuthenticationRepository.

        Args:
            authentication_repository (AuthenticationRepository): The repository used to fetch user data.
        """
        self._authentication_repository = authentication_repository

    def login(self, username: str, password: str) -> AuthResponseDto:
        """Authenticate a user with the provided username and password.

        Args:
            username (str): The username of the user trying to log in.
            password (str): The password provided by the user.

        Returns:
            AuthResponseDto: The response object containing the authentication result.
                - If the user is not found, the status will be `ResponseStatusEnum.NOT_FOUND`.
                - If the password is incorrect, the status will be `ResponseStatusEnum.BAD_CREDENTIAL` with an appropriate message.
                - If the credentials are valid, the status will be `ResponseStatusEnum.OK` and the response will include a JWT token.
        """
        user = self._authentication_repository.get_admin_by_username(username)

        if user is None:
            return AuthResponseDto(data=None, status=ResponseStatusEnum.NOT_FOUND)

        if user.password != password:
            return AuthResponseDto(
                data=None,
                status=ResponseStatusEnum.BAD_CREDENTIAL,
                message=LoginError.wrong_password(),
            )
        token = None
        if user.id:
            token = JwtHandler.sign(user.id)
        return AuthResponseDto(data=token, status=ResponseStatusEnum.OK)
