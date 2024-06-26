from enum import Enum
from engine.backend.database_connector import DatabaseConnector
from engine.backend.jwt_handler import JwtHandler
from models.responses.response_dto import ResponseStatusEnum
from models.login_dto import LoginDto
from models.responses.auth_response_dto import AuthResponseDto
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from database import crud, models
from database.base import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tag = "login"
router = APIRouter()
connector = DatabaseConnector()
class CheckUserResult(Enum):
    OK = "OK"
    WRONG_USERNAME = "WRONG USERNAME"
    WRONG_PASSWORD = "WRONG PASSWORD"

def _checkUser(data: LoginDto, db: Session = Depends(getDb)) -> CheckUserResult:
    query = crud.getUserByUsername(db, data.username)
    if(query == None):
        return CheckUserResult.WRONG_USERNAME
    if(query.password != data.password):
        return CheckUserResult.WRONG_PASSWORD
    return CheckUserResult.OK

@router.post("/", tags=[tag], response_model=AuthResponseDto)
def login(data: LoginDto, db: Session = Depends(getDb)):
    check = _checkUser(data, db)
    if(check == CheckUserResult.WRONG_USERNAME):
        return AuthResponseDto(
            data = None,
            status = ResponseStatusEnum.NOT_FOUND
        )
    if(check == CheckUserResult.WRONG_PASSWORD):
        return AuthResponseDto(
            data = None,
            status = ResponseStatusEnum.ERROR,
            message = "Wrong password"
        )
    if(check == CheckUserResult.OK):
        token = JwtHandler.sign()
        return AuthResponseDto(
            data = token,
            status = ResponseStatusEnum.OK
        )
    return AuthResponseDto(
        data = None,
        status = ResponseStatusEnum.ERROR
    )
