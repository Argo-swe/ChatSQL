from fastapi import APIRouter, File, UploadFile
from typing import Optional

from models.dictionary_dto import DictionaryDto

tag = "dictionary"
router = APIRouter()

@router.get("/", tags=[tag], response_model=list[DictionaryDto])
def get_dictionaries() -> list[DictionaryDto]:
    dictionaries: list[DictionaryDto] = []
    return dictionaries

@router.post("/", tags=[tag], response_model=DictionaryDto)
def create_dicrionary_metadata(dictionary: DictionaryDto, file: Optional[UploadFile] = None) -> DictionaryDto:
    dictionary = DictionaryDto(name="Dizionario di prova", description=file.filename)
    return dictionary

@router.put("/{id}", tags=[tag], response_model=DictionaryDto)
def update_dicrionary_metadata(id: int, dictionary: DictionaryDto) -> DictionaryDto:
    dictionary = DictionaryDto(name="Dizionario di prova", description="Descrizione dizionario di prova")
    return dictionary

@router.delete("/{id}", tags=[tag], response_model=DictionaryDto)
def update_dicrionary_metadata() -> None:
    dictionary = DictionaryDto(name="Dizionario di prova", description="Descrizione dizionario di prova")
