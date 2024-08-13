from adapter.outcoming.sql_alchemy.sql_alchemy_dictionary_repository_adapter import (
    SqlAlchemyDictionaryRepositoryAdapter
)
from adapter.outcoming.json.filesystem_json_adapter import FilesystemJsonAdapter
from adapter.outcoming.txtai.txtai_index_manager_adapter import TxtaiIndexManagerAdapter
from core.service.dictionary_service import DictionaryService
from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.dictionary_dto import DictionaryDto

from engine.index_manager import IndexManager

from auth.jwt_bearer import JwtBearer
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
from typing import Annotated


tag = "dictionary"
router = APIRouter()
manager = IndexManager()

# TODO: ottimizzare gli import (Dep inj o singleton?)
dictionary_repository = SqlAlchemyDictionaryRepositoryAdapter()
index_manager = TxtaiIndexManagerAdapter()
json_repository = FilesystemJsonAdapter("/opt/chatsql/dictionary_schemas")
dictionary_service = DictionaryService(dictionary_repository, index_manager, json_repository)


@router.get(
    "/", tags=[tag], response_model=DictionariesResponseDto, name="getAllDictionaries"
)
def get_all_dictionaries() -> DictionariesResponseDto:
    return dictionary_service.get_dictionary_list()


@router.get(
    "/{id}", tags=[tag], response_model=DictionaryResponseDto, name="getDictionary"
)
def get_dictionary(id: int) -> DictionaryResponseDto:
    return dictionary_service.get_dictionary_by_id(id)


@router.get("/{id}/file", tags=[tag], name="getDictionaryFile")
def get_dictionary_file(id: int):
    response = dictionary_service.get_dictionary_file(id)

    if response is not None:
        return FileResponse(response)

    return ResponseDto(
        message=f"Dictionary with id {id} not found",
        status=ResponseStatusEnum.NOT_FOUND,
    )


@router.get(
    "/{id}/dictionary-preview",
    tags=[tag],
    response_model=DictionaryResponseDto,
    name="getDictionaryPreview",
)
def get_dictionary_preview(id: int) -> DictionaryResponseDto:
    return dictionary_service.get_dictionary_preview(id)


@router.post(
    "/",
    tags=[tag],
    response_model=DictionaryResponseDto,
    dependencies=[Depends(JwtBearer())],
    name="createDictionary",
)
async def create_dictionary(
    file: Annotated[UploadFile, File()],
    dictionary: DictionaryDto = Depends(),
) -> DictionaryResponseDto:
    if file:
        content = await file.read()
    else:
        content = ""
    return await dictionary_service.create_dictionary(dictionary, content)


@router.put(
    "/{id}/file",
    tags=[tag],
    response_model=DictionaryResponseDto,
    dependencies=[Depends(JwtBearer())],
    name="updateDictionaryFile",
)
async def update_dictionary_file(
    id: int, file: Annotated[UploadFile, File()]
) -> DictionaryResponseDto:
    if file:
        content = await file.read()
    else:
        content = ""
    return await dictionary_service.update_dictionary_file(id, content)


@router.put(
    "/{id}",
    tags=[tag],
    response_model=DictionaryResponseDto,
    dependencies=[Depends(JwtBearer())],
    name="updateDictionaryMetadata",
)
def update_dictionary_metadata(
    id: int, dictionary: DictionaryDto
) -> DictionaryResponseDto:
    return dictionary_service.update_dictionary_metadata(id, dictionary)


@router.delete("/{id}", tags=[tag], response_model=ResponseDto, name="deleteDictionary")
def delete_dictionary(id: int) -> ResponseDto:
    return dictionary_service.delete_dictionary(id)


def __generate_schema_file_name(id: int) -> str:
    global out_file_base_path
    return f"{out_file_base_path}/dic_schema_{id}.json"
