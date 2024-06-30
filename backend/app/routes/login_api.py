from enum import Enum
from auth.jwt_handler import JwtHandler
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

@router.post("/", tags=[tag], response_model=AuthResponseDto)
def login(data: LoginDto, db: Session = Depends(getDb)):
    query = crud.getUserByUsername(db, data.username)
    if(query == None):
        return AuthResponseDto(
            data = None,
            status = ResponseStatusEnum.NOT_FOUND
        )
    if(query.password != data.password):
        return AuthResponseDto(
            data = None,
            status = ResponseStatusEnum.BAD_CREDENTIAL,
            message = "Wrong password"
        )
    token = JwtHandler.sign(query.id)
    return AuthResponseDto(
        data = token,
        status = ResponseStatusEnum.OK
    )
