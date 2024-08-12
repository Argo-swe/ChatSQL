from typing import Annotated
from models.responses.response_dto import ResponseStatusEnum
from models.responses.string_data_response_dto import StringDataResponseDto
from models.responses.prompt_response_dto import PromptResponseDto
from models.prompt_dto import PromptDto
from auth.jwt_bearer import JwtBearer

from fastapi import APIRouter, Depends, Query
from engine.prompt_manager import PromptManager

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

manager = PromptManager()


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

    prompt, log_content = manager.prompt_generator(
        found_dic.id, query, lang, dbms, activate_log=False
    )

    print(prompt)

    return StringDataResponseDto(data=prompt, status=ResponseStatusEnum.OK)


@router.get(
    "/debug",
    tags=[tag],
    response_model=PromptResponseDto,
    dependencies=[Depends(JwtBearer())],
    name="generatePromptWithDebug",
)
def generate_prompt_with_debug(
    dictionary_id: Annotated[int, Query(alias="dictionaryId")],
    query: str,
    dbms: str,
    lang: str,
    db: Session = Depends(get_db),
) -> PromptResponseDto:

    found_dic = crud.get_dictionary_by_id(db, dictionary_id)

    if found_dic is None:
        return PromptResponseDto(
            message=f"Dictionary with id {id} not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )

    if query is None or query == "":
        return PromptResponseDto(
            message="Query cannot be empty", status=ResponseStatusEnum.BAD_REQUEST
        )

    prompt, log_content = manager.prompt_generator(
        found_dic.id, query, lang, dbms, activate_log=True
    )

    print(prompt)

    prompt_dto = PromptDto(prompt=prompt, debug=log_content)

    return PromptResponseDto(data=prompt_dto, status=ResponseStatusEnum.OK)


# @router.get(
#     "/debug/only",
#     tags=[tag],
#     response_model=StringDataResponseDto,
#     name="generatePromptDebug",
# )
# def generate_prompt_debug() -> StringDataResponseDto:

#     try:
#         with open("/opt/chatsql/logs/chatsql_log.txt", "r") as file:
#             return StringDataResponseDto(data=file.read(), status=ResponseStatusEnum.OK)
#     except FileNotFoundError:
#         return StringDataResponseDto(
#             message="Log file not found", status=ResponseStatusEnum.NOT_FOUND
#         )
