from routes.auth.jwt_handler import JwtHandler
from core.port.outcoming.authentication_repository import AuthenticationRepository
from models.responses.auth_response_dto import AuthResponseDto
from core.port.incoming.authentication_use_case import AuthenticationUseCase
from models.responses.response_dto import ResponseStatusEnum


class AuthenticationService(AuthenticationUseCase):

    def __init__(self, authentication_repository: AuthenticationRepository) -> None:
        self._authentication_repository = authentication_repository

    def login(self, username: str, password: str) -> AuthResponseDto:
        user = self._authentication_repository.get_user_by_username(username)

        if user is None:
            return AuthResponseDto(data=None, status=ResponseStatusEnum.NOT_FOUND)

        if user.password != password:
            return AuthResponseDto(
                data=None,
                status=ResponseStatusEnum.BAD_CREDENTIAL,
                message="Wrong password",
            )
        token = JwtHandler.sign(user.id)
        return AuthResponseDto(data=token, status=ResponseStatusEnum.OK)
