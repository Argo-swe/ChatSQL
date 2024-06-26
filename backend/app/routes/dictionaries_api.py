from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.dictionary_dto import DictionaryDto

from engine.backend.jwt_bearer import JwtBearer
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
from typing import Annotated, List
import aiofiles
import os

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

tag = "dictionary"
router = APIRouter()

outFileBasePath = "/opt/chatsql/dictionary_schemas"

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

        # TODO: validare dizionario e create indice txtai

        async with aiofiles.open(__generateSchemaFileName(newDic.id), 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)


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

    async with aiofiles.open(__generateSchemaFileName(id), 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # TODO: validare dizionario e aggiornare indice txtai

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

    # TODO: rimuovere indice txtai

    return ResponseDto(
                status=ResponseStatusEnum.OK
            )

def __generateSchemaFileName(id: int) -> str:
    global outFileBasePath
    return f'{outFileBasePath}/dic_schema_{id}.json'
