from engine.tools.utils import Utils
from models.responses.response_dto import ResponseStatusEnum
from models.responses.string_data_response_dto import StringDataResponseDto

from fastapi import APIRouter, Depends
from engine.index_manager import IndexManager

from sqlalchemy.orm import Session
from database import crud, models
from database.base import SessionLocal, engine

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tag = "prompt"
router = APIRouter()

manager = IndexManager()

@router.get("/", tags=[tag], response_model=StringDataResponseDto)
def generatePrompt(dictionaryId: int, query: str, dbms: str, lang: str, db: Session = Depends(getDb)) -> StringDataResponseDto:

    foundDic = crud.getDictionaryById(db, dictionaryId)

    if foundDic == None:
        return StringDataResponseDto(
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND
            )

    if query is None or query == "":
        return StringDataResponseDto(
                message=f"Query cannot be empty",
                status=ResponseStatusEnum.BAD_REQUEST
            )

    manager.loadIndex(foundDic.id)
    prompt = manager.promptGenerator(foundDic.id, query, lang, dbms, activate_log=True)

    print(prompt)

    return StringDataResponseDto(
        data=prompt,
        status=ResponseStatusEnum.OK
    )

# TODO: valutare quando gestire il caricamento indice (problema concorrenza)
# @router.put("/select-index", tags=[tag], response_model=ResponseDto)
# def generatePrompt(dictionaryId: int, db: Session = Depends(getDb)) -> Res:

#     foundDic = crud.getDictionaryById(db, dictionaryId)

#     if foundDic == None:
#         return ResponseDto(
#                 message=f"Dictionary with id {id} not found",
#                 status=ResponseStatusEnum.NOT_FOUND
#             )

#     manager.createOrLoadIndex(f"index_{foundDic.id}")

#     return ResponseDto(
#         data=prompt,
#         status=ResponseStatusEnum.OK
#     )

@router.get("/debug", tags=[tag], response_model=StringDataResponseDto)
def generatePromptDebug() -> StringDataResponseDto:

    try:
        with open('/opt/chatsql/logs/chatsql_log.txt', 'r') as file:
            return StringDataResponseDto(
                data=file.read(),
                status=ResponseStatusEnum.OK
    )
    except FileNotFoundError:
        return StringDataResponseDto(
            message="Log file not found",
            status=ResponseStatusEnum.NOT_FOUND
        )
