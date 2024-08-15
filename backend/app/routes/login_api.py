from configuration import Configuration
from core.service.authentication_service import AuthenticationService
from models.login_dto import LoginDto
from models.responses.auth_response_dto import AuthResponseDto
from fastapi import APIRouter, Depends


def create_login_router(config: Configuration):
    tag = "login"
    router = APIRouter()

    def get_authentication_service() -> AuthenticationService:
        return config.get_authentication_service()

    @router.post("/", tags=[tag], response_model=AuthResponseDto, name="login")
    def login(
        data: LoginDto,
        authentication_service: AuthenticationService = Depends(
            get_authentication_service
        ),
    ):
        return authentication_service.login(data.username, data.password)

    return router


login_router = create_login_router
