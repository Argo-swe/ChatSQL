from typing import Annotated
from models.responses.response_dto import ResponseStatusEnum
from models.responses.string_data_response_dto import StringDataResponseDto

from fastapi import APIRouter, Depends, Query
from engine.index_manager import IndexManager

from sqlalchemy.orm import Session
from database import crud
from database.base import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tag = "prompt"
router = APIRouter()

manager = IndexManager()


@router.get(
    "/", tags=[tag], response_model=StringDataResponseDto, name="generatePrompt"
)
def generate_prompt(
    dictionary_id: Annotated[int, Query(alias="dictionaryId")],
    query: str,
    dbms: str,
    lang: str,
    db: Session = Depends(get_db),
) -> StringDataResponseDto:

    found_dic = crud.get_dictionary_by_id(db, dictionary_id)

    if found_dic is None:
        return StringDataResponseDto(
            message=f"Dictionary with id {id} not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )

    if query is None or query == "":
        return StringDataResponseDto(
            message="Query cannot be empty", status=ResponseStatusEnum.BAD_REQUEST
        )

    manager.load_index(found_dic.id)
    prompt = manager.prompt_generator(
        found_dic.id, query, lang, dbms, activate_log=True
    )

    print(prompt)

    return StringDataResponseDto(data=prompt, status=ResponseStatusEnum.OK)


@router.get(
    "/debug",
    tags=[tag],
    response_model=StringDataResponseDto,
    name="generatePromptDebug",
)
def generate_prompt_debug() -> StringDataResponseDto:

    try:
        with open("/opt/chatsql/logs/chatsql_log.txt", "r") as file:
            return StringDataResponseDto(data=file.read(), status=ResponseStatusEnum.OK)
    except FileNotFoundError:
        return StringDataResponseDto(
            message="Log file not found", status=ResponseStatusEnum.NOT_FOUND
        )
