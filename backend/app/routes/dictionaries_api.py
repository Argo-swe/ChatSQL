from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto

from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import FileResponse
from typing import Annotated, List
import aiofiles

from models.dictionary_dto import DictionaryDto

tag = "dictionary"
router = APIRouter()

out_file_base_path = "/usr/src/app/dic_schemas"
next_id = 2

# TODO: da rimuovere quando legato a DB
dictionaries: List[DictionaryDto] = [
    DictionaryDto(id=1, name="Dizionario di prova", description="Descrizione esempio 1")
]

# TODO: update & upload file

@router.get("/", tags=[tag], response_model=DictionariesResponseDto)
def getAllDictionaries() -> DictionariesResponseDto:
    return DictionariesResponseDto(
            data=dictionaries,
            status=ResponseStatusEnum.OK.value
        )

@router.get("/{id}", tags=[tag], response_model=DictionaryResponseDto)
def getDictionary(id: int) -> DictionaryResponseDto:
    found_dic = next((x for x in dictionaries if x.id == id), None)
    print(found_dic)
    if found_dic != None:
        return DictionaryResponseDto(
                data=found_dic,
                status=ResponseStatusEnum.OK.value
            )

    return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND.value
            )

@router.get("/{id}/file", tags=[tag])
def getDictionaryFile(id: int):
    found_dic = next((x for x in dictionaries if x.id == id), None)
    print(found_dic)
    if found_dic != None:
        return FileResponse(generateFileName(id))

    return ResponseDto(
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND.value
            )

@router.post("/", tags=[tag], response_model=DictionaryResponseDto)
async def createDictionary(file: Annotated[UploadFile, File()], dictionary: DictionaryDto = Depends()) -> DictionaryResponseDto:
    global next_id
    if dictionary.name != None and dictionary.description != None and file:
        aus_dic = DictionaryDto(id=next_id, name=dictionary.name, description=dictionary.description)
        dictionaries.append(aus_dic)

        print (file.filename)

        # TODO come gestire il file?
        async with aiofiles.open(generateFileName(next_id), 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write

        next_id += 1

        return DictionaryResponseDto(
                data=aus_dic,
                status=ResponseStatusEnum.OK.value
        )

    if not file:
        return DictionaryResponseDto(
                data=None,
                message=f"Dictionary file is mandatory",
                status=ResponseStatusEnum.BAD_REQUEST.value
            )

    return DictionaryResponseDto(
                data=None,
                message=f"Dictionary name and description are mandatory",
                status=ResponseStatusEnum.BAD_REQUEST.value
            )

@router.put("/{id}/file", tags=[tag], response_model=DictionaryResponseDto)
async def updateDictionaryFile(id: int, file: Annotated[UploadFile, File()]) -> DictionaryResponseDto:
    found_dic = next((x for x in dictionaries if x.id == id), None)
    if found_dic == None:
        return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND.value
            )

    # TODO come gestire il file?
    async with aiofiles.open(generateFileName(id), 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write

    return DictionaryResponseDto(
                data=found_dic,
                status=ResponseStatusEnum.OK.value
            )

@router.put("/{id}", tags=[tag], response_model=DictionaryResponseDto)
def updateDictionaryMetadata(id: int, dictionary: DictionaryDto) -> DictionaryResponseDto:
    found_dic = next((x for x in dictionaries if x.id == id), None)
    if found_dic == None:
        return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND.value
            )

    if dictionary.name == None or dictionary.description == None:
        return DictionaryResponseDto(
                data=None,
                message="Dictionary name and description are mandatory",
                status=ResponseStatusEnum.BAD_REQUEST.value
            )

    found_dic.name = dictionary.name
    found_dic.description = dictionary.description

    return DictionaryResponseDto(
                data=found_dic,
                status=ResponseStatusEnum.OK.value
            )

@router.delete("/{id}", tags=[tag], response_model=ResponseDto)
def deleteDictionary(id: int) -> ResponseDto:
    found_dic = next((x for x in dictionaries if x.id == id), None)

    if found_dic == None:
        return ResponseDto(
                message=f"Dictionary with id {id} not found",
                status=ResponseStatusEnum.NOT_FOUND.value
            )

    dictionaries.remove(found_dic)

    return ResponseDto(
                status=ResponseStatusEnum.OK.value
            )

def generateFileName(id: int) -> str:
    global out_file_base_path
    return f'{out_file_base_path}/dic_schema_{id}.json'
