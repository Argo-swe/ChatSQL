from typing import Annotated

from adapter.outcoming.sql_alchemy.sql_alchemy_dictionary_repository_adapter import (
    SqlAlchemyDictionaryRepositoryAdapter,
)
from adapter.outcoming.txtai.txtai_index_manager_adapter import TxtaiIndexManagerAdapter
from adapter.outcoming.txtai.txtai_prompt_manager_agapter import (
    TxtaiPromptManagerAdapter,
)
from models.responses.string_data_response_dto import StringDataResponseDto
from models.responses.prompt_response_dto import PromptResponseDto
from auth.jwt_bearer import JwtBearer
from core.service.prompt_manager_service import PromptManagerService
from core.service.dictionary_service import DictionaryService


from fastapi import APIRouter, Depends, Query

tag = "prompt"
router = APIRouter()

# TODO: ottimizzare gli import (Dep inj o singleton?)
dictionary_repository = SqlAlchemyDictionaryRepositoryAdapter()
index_manager = TxtaiIndexManagerAdapter()
dictionary_service = DictionaryService(dictionary_repository, index_manager)
prompt_manager = TxtaiPromptManagerAdapter(index_manager)
prompt_manager_service = PromptManagerService(dictionary_service, prompt_manager)


@router.get(
    "/", tags=[tag], response_model=StringDataResponseDto, name="generatePrompt"
)
def generate_prompt(
    dictionary_id: Annotated[int, Query(alias="dictionaryId")],
    query: str,
    dbms: str,
    lang: str,
) -> StringDataResponseDto:

    return prompt_manager_service.generate_prompt(dictionary_id, query, lang, dbms)


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
) -> PromptResponseDto:

    return prompt_manager_service.generate_prompt_with_debug(
        dictionary_id, query, lang, dbms
    )
