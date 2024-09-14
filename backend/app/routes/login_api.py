from configuration import Configuration
from core.service.authentication_service import AuthenticationService
from models.login_dto import LoginDto
from models.responses.auth_response_dto import AuthResponseDto
from fastapi import APIRouter, Depends


def create_login_router(config: Configuration):
    tag = "login"
    router = APIRouter()

    def get_authentication_service() -> AuthenticationService:
        """Retrieve the authentication service instance from the configuration."""
        return config.get_authentication_service()

    @router.post(
        "/",
        tags=[tag],
        response_model=AuthResponseDto,
        name="login",
        summary="User login",
    )
    def login(
        data: LoginDto,
        authentication_service: AuthenticationService = Depends(
            get_authentication_service
        ),
    ) -> AuthResponseDto:
        """Authenticate a user with the provided credentials.

        - **username**: The username of the user.
        - **password**: The password of the user.

        Returns an authentication token if the login is successful.
        """
        return authentication_service.login(data.username, data.password)

    return router


login_router = create_login_router
