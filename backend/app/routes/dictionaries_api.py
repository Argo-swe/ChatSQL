from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.dictionary_dto import DictionaryDto
from models.dictionary_preview_dto import DictionaryPreviewDto
from models.dictionary_internal_structure.table_dto import TableDto
from tools.dictionary_validator import DictionaryValidator
from tools.utils import Utils
from tools.schema_multi_extractor import Schema_Multi_Extractor

from engine.index_manager import IndexManager

from auth.jwt_bearer import JwtBearer
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
from typing import Annotated, List
import aiofiles
import os

from sqlalchemy.orm import Session
from database import crud
from database.base import SessionLocal

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tag = "dictionary"
router = APIRouter()

outFileBasePath = "/opt/chatsql/dictionary_schemas"
os.makedirs(outFileBasePath, exist_ok=True)

manager = IndexManager()

@router.get("/", tags=[tag], response_model=DictionariesResponseDto)
def getAllDictionaries(db: Session = Depends(getDb)) -> DictionariesResponseDto:
    dictionaries = crud.getAllDictionaries(db)

    return DictionariesResponseDto(
            data=dictionaries,
            status=ResponseStatusEnum.OK
        )

@router.get("/{id}", tags=[tag], response_model=DictionaryResponseDto)
def getDictionary(id: int, db: Session = Depends(getDb)) -> DictionaryResponseDto:
    foundDic = crud.getDictionaryById(db, id)

    if foundDic != None:
        return DictionaryResponseDto(
                data=foundDic,
                status=ResponseStatusEnum.OK
            )

    return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND
            )

@router.get("/{id}/file", tags=[tag])
def getDictionaryFile(id: int, db: Session = Depends(getDb)):
    foundDic = crud.getDictionaryById(db, id)

    if foundDic != None:
        return FileResponse(__generateSchemaFileName(id))

    return ResponseDto(
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND
            )

@router.get("/{id}/dictionary-preview", tags=[tag])
def getDictionaryPreview(id: int, db: Session = Depends(getDb)) -> DictionaryResponseDto:
    foundDic = crud.getDictionaryById(db, id)

    if foundDic != None:
        dictionary_sub_schema = Schema_Multi_Extractor.extract_preview(id)

        dictionary_preview_dto = DictionaryPreviewDto(
            database_name=dictionary_sub_schema["database_name"],
            database_description=dictionary_sub_schema["database_description"],
            tables=[TableDto(**table) for table in dictionary_sub_schema["tables"]]
        )

        return DictionaryResponseDto(
            data = dictionary_preview_dto,
            status=ResponseStatusEnum.OK
        )

    return ResponseDto(
        message=f"Dictionary with id {id} not found",
        status=ResponseStatusEnum.NOT_FOUND
    )

@router.post("/", tags=[tag], response_model=DictionaryResponseDto, dependencies=[Depends(JwtBearer())])
async def createDictionary(file: Annotated[UploadFile, File()], dictionary: DictionaryDto = Depends(), db: Session = Depends(getDb)) -> DictionaryResponseDto:
    if dictionary.name != None and dictionary.description != None and file:
        foundDic = crud.getDictionaryByName(db, name=dictionary.name)

        if foundDic:
            return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with name '{dictionary.name}' already exists",
                status=ResponseStatusEnum.CONFLICT
            )

        newDic = crud.createDictionary(db=db, dictionary=dictionary)

        # validate dictionary schema
        content = await file.read()
        isValid = DictionaryValidator.validate(Utils.string_to_json(content))

        if not isValid:
            return DictionaryResponseDto(
                    data=None,
                    message=f"Dictionary schema is bad formatted",
                    status=ResponseStatusEnum.BAD_REQUEST
                )

        async with aiofiles.open(__generateSchemaFileName(newDic.id), 'wb') as out_file:
            await out_file.write(content)

        # create txtai index
        manager.createIndex(newDic.id)

        return DictionaryResponseDto(
                data=newDic,
                status=ResponseStatusEnum.OK
        )

    if not file:
        return DictionaryResponseDto(
                data=None,
                message=f"Dictionary file is mandatory",
                status=ResponseStatusEnum.BAD_REQUEST
            )

    return DictionaryResponseDto(
                data=None,
                message=f"Dictionary name and description are mandatory",
                status=ResponseStatusEnum.BAD_REQUEST
            )

@router.put("/{id}/file", tags=[tag], response_model=DictionaryResponseDto, dependencies=[Depends(JwtBearer())])
async def updateDictionaryFile(id: int, file: Annotated[UploadFile, File()], db: Session = Depends(getDb)) -> DictionaryResponseDto:
    foundDic = crud.getDictionaryById(db, id)

    if foundDic == None:
        return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND
            )

    # validate dictionary schema
    content = await file.read()
    isValid = DictionaryValidator.validate(Utils.string_to_json(content))

    if not isValid:
        return DictionaryResponseDto(
                data=None,
                message=f"Dictionary schema is bad formatted",
                status=ResponseStatusEnum.BAD_REQUEST
            )

    async with aiofiles.open(__generateSchemaFileName(id), 'wb') as out_file:
        await out_file.write(content)

    # update txtai index
    manager.createIndex(foundDic.id)

    return DictionaryResponseDto(
                data=foundDic,
                status=ResponseStatusEnum.OK
            )

@router.put("/{id}", tags=[tag], response_model=DictionaryResponseDto, dependencies=[Depends(JwtBearer())])
def updateDictionaryMetadata(id: int, dictionary: DictionaryDto, db: Session = Depends(getDb)) -> DictionaryResponseDto:
    foundDic = crud.getDictionaryById(db, id)

    if foundDic == None:
        return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND
            )

    if dictionary.name == None or dictionary.description == None:
        return DictionaryResponseDto(
                data=None,
                message="Dictionary name and description are mandatory",
                status=ResponseStatusEnum.BAD_REQUEST
            )

    dicWithName = crud.getDictionaryByName(db, dictionary.name)
    if dicWithName != None and dicWithName.id != id:
        return DictionaryResponseDto(
            data=None,
            message=f"Dictionary with name '{dictionary.name}' already exists",
            status=ResponseStatusEnum.CONFLICT
        )

    newDic = crud.updateDictionary(db, dictionary)

    return DictionaryResponseDto(
                data=newDic,
                status=ResponseStatusEnum.OK
            )

@router.delete("/{id}", tags=[tag], response_model=ResponseDto)
def deleteDictionary(id: int, db: Session = Depends(getDb)) -> ResponseDto:
    foundDic = crud.getDictionaryById(db, id)

    if foundDic == None:
        return ResponseDto(
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND
            )

    crud.deleteDictionary(db, id)

    if os.path.exists(__generateSchemaFileName(id)):
        os.remove(__generateSchemaFileName(id))

    # delete txtai index
    manager.deleteIndex(foundDic.id)

    return ResponseDto(
                status=ResponseStatusEnum.OK
            )

def __generateSchemaFileName(id: int) -> str:
    global outFileBasePath
    return f'{outFileBasePath}/dic_schema_{id}.json'
