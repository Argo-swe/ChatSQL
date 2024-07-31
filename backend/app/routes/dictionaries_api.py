from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.dictionary_dto import DictionaryDto
from models.dictionary_preview_dto import DictionaryPreviewDto
from models.dictionary_internal_structure.table_dto import TableDto
from tools.dictionary_validator import DictionaryValidator
from tools.utils import Utils
from tools.schema_multi_extractor import SchemaMultiExtractor

from engine.index_manager import IndexManager

from auth.jwt_bearer import JwtBearer
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
from typing import Annotated
import aiofiles
import os

from sqlalchemy.orm import Session
from database import crud
from database.base import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tag = "dictionary"
router = APIRouter()

out_file_base_path = "/opt/chatsql/dictionary_schemas"
os.makedirs(out_file_base_path, exist_ok=True)

manager = IndexManager()


@router.get(
    "/", tags=[tag], response_model=DictionariesResponseDto, name="getAllDictionaries"
)
def get_all_dictionaries(db: Session = Depends(get_db)) -> DictionariesResponseDto:
    dictionaries = crud.get_all_dictionaries(db)

    return DictionariesResponseDto(data=dictionaries, status=ResponseStatusEnum.OK)


@router.get(
    "/{id}", tags=[tag], response_model=DictionaryResponseDto, name="getDictionary"
)
def get_dictionary(id: int, db: Session = Depends(get_db)) -> DictionaryResponseDto:
    found_dic = crud.get_dictionary_by_id(db, id)

    if found_dic is not None:
        return DictionaryResponseDto(data=found_dic, status=ResponseStatusEnum.OK)

    return DictionaryResponseDto(
        data=None,
        message=f"Dictionary with id {id} not found",
        status=ResponseStatusEnum.NOT_FOUND,
    )


@router.get("/{id}/file", tags=[tag], name="getDictionaryFile")
def get_dictionary_file(id: int, db: Session = Depends(get_db)):
    found_dic = crud.get_dictionary_by_id(db, id)

    if found_dic is not None:
        return FileResponse(__generate_schema_file_name(id))

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
def get_dictionary_preview(
    id: int, db: Session = Depends(get_db)
) -> DictionaryResponseDto:
    found_dic = crud.get_dictionary_by_id(db, id)

    if found_dic is not None:
        dictionary_sub_schema = SchemaMultiExtractor.extract_preview(id)

        dictionary_preview_dto = DictionaryPreviewDto(
            database_name=dictionary_sub_schema["database_name"],
            database_description=dictionary_sub_schema["database_description"],
            tables=[TableDto(**table) for table in dictionary_sub_schema["tables"]],
        )

        return DictionaryResponseDto(
            data=dictionary_preview_dto, status=ResponseStatusEnum.OK
        )

    return ResponseDto(
        message=f"Dictionary with id {id} not found",
        status=ResponseStatusEnum.NOT_FOUND,
    )


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
    db: Session = Depends(get_db),
) -> DictionaryResponseDto:
    if dictionary.name is not None and dictionary.description is not None and file:
        found_dic = crud.get_dictionary_by_name(db, name=dictionary.name)

        if found_dic:
            return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with name '{dictionary.name}' already exists",
                status=ResponseStatusEnum.CONFLICT,
            )

        new_dic = crud.create_dictionary(db=db, dictionary=dictionary)

        # validate dictionary schema
        content = await file.read()
        is_valid = DictionaryValidator.validate(Utils.string_to_json(content))

        if not is_valid:
            return DictionaryResponseDto(
                data=None,
                message="Dictionary schema is bad formatted",
                status=ResponseStatusEnum.BAD_REQUEST,
            )

        async with aiofiles.open(
            __generate_schema_file_name(new_dic.id), "wb"
        ) as out_file:
            await out_file.write(content)

        # create txtai index
        manager.create_index(new_dic.id)

        return DictionaryResponseDto(data=new_dic, status=ResponseStatusEnum.OK)

    if not file:
        return DictionaryResponseDto(
            data=None,
            message="Dictionary file is mandatory",
            status=ResponseStatusEnum.BAD_REQUEST,
        )

    return DictionaryResponseDto(
        data=None,
        message="Dictionary name and description are mandatory",
        status=ResponseStatusEnum.BAD_REQUEST,
    )


@router.put(
    "/{id}/file",
    tags=[tag],
    response_model=DictionaryResponseDto,
    dependencies=[Depends(JwtBearer())],
    name="updateDictionaryFile",
)
async def update_dictionary_file(
    id: int, file: Annotated[UploadFile, File()], db: Session = Depends(get_db)
) -> DictionaryResponseDto:
    found_dic = crud.get_dictionary_by_id(db, id)

    if found_dic is None:
        return DictionaryResponseDto(
            data=None,
            message=f"Dictionary with id {id} not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )

    # validate dictionary schema
    content = await file.read()
    is_valid = DictionaryValidator.validate(Utils.string_to_json(content))

    if not is_valid:
        return DictionaryResponseDto(
            data=None,
            message="Dictionary schema is bad formatted",
            status=ResponseStatusEnum.BAD_REQUEST,
        )

    async with aiofiles.open(__generate_schema_file_name(id), "wb") as out_file:
        await out_file.write(content)

    # update txtai index
    manager.create_index(found_dic.id)

    return DictionaryResponseDto(data=found_dic, status=ResponseStatusEnum.OK)


@router.put(
    "/{id}",
    tags=[tag],
    response_model=DictionaryResponseDto,
    dependencies=[Depends(JwtBearer())],
    name="updateDictionaryMetadata",
)
def update_dictionary_metadata(
    id: int, dictionary: DictionaryDto, db: Session = Depends(get_db)
) -> DictionaryResponseDto:
    found_dic = crud.get_dictionary_by_id(db, id)

    if found_dic is None:
        return DictionaryResponseDto(
            data=None,
            message=f"Dictionary with id {id} not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )

    if dictionary.name is None or dictionary.description is None:
        return DictionaryResponseDto(
            data=None,
            message="Dictionary name and description are mandatory",
            status=ResponseStatusEnum.BAD_REQUEST,
        )

    dic_with_name = crud.get_dictionary_by_name(db, dictionary.name)
    if dic_with_name is not None and dic_with_name.id != id:
        return DictionaryResponseDto(
            data=None,
            message=f"Dictionary with name '{dictionary.name}' already exists",
            status=ResponseStatusEnum.CONFLICT,
        )

    new_dic = crud.update_dictionary(db, dictionary)

    return DictionaryResponseDto(data=new_dic, status=ResponseStatusEnum.OK)


@router.delete("/{id}", tags=[tag], response_model=ResponseDto, name="deleteDictionary")
def delete_dictionary(id: int, db: Session = Depends(get_db)) -> ResponseDto:
    found_dic = crud.get_dictionary_by_id(db, id)

    if found_dic is None:
        return ResponseDto(
            message=f"Dictionary with id {id} not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )

    crud.delete_dictionary(db, id)

    if os.path.exists(__generate_schema_file_name(id)):
        os.remove(__generate_schema_file_name(id))

    # delete txtai index
    manager.delete_index(found_dic.id)

    return ResponseDto(status=ResponseStatusEnum.OK)


def __generate_schema_file_name(id: int) -> str:
    global out_file_base_path
    return f"{out_file_base_path}/dic_schema_{id}.json"
