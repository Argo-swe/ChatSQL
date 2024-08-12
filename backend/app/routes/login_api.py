from adapter.outcoming.sql_alchemy.sql_alchemy_authentication_repository_adapter import (
    SqlAlchemyAuthenticationRepositoryAdapter,
)
from core.service.authentication_service import AuthenticationService
from models.login_dto import LoginDto
from models.responses.auth_response_dto import AuthResponseDto
from fastapi import APIRouter

tag = "login"
router = APIRouter()

# TODO: ottimizzare gli import (Dep inj o singleton?)
authentication_repository = SqlAlchemyAuthenticationRepositoryAdapter()
authentication_service = AuthenticationService(authentication_repository)


@router.post("/", tags=[tag], response_model=AuthResponseDto, name="login")
def login(data: LoginDto):
    return authentication_service.login(data.username, data.password)
