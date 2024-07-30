from auth.jwt_handler import JwtHandler
from models.responses.response_dto import ResponseStatusEnum
from models.login_dto import LoginDto
from models.responses.auth_response_dto import AuthResponseDto
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from database import crud
from database.base import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tag = "login"
router = APIRouter()


@router.post("/", tags=[tag], response_model=AuthResponseDto, name="login")
def login(data: LoginDto, db: Session = Depends(get_db)):
    query = crud.get_user_by_username(db, data.username)
    if query is None:
        return AuthResponseDto(data=None, status=ResponseStatusEnum.NOT_FOUND)
    if query.password != data.password:
        return AuthResponseDto(
            data=None,
            status=ResponseStatusEnum.BAD_CREDENTIAL,
            message="Wrong password",
        )
    token = JwtHandler.sign(query.id)
    return AuthResponseDto(data=token, status=ResponseStatusEnum.OK)
