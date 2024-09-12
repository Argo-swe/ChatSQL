from typing import Annotated
from configuration import Configuration
from core.service.dictionary_service import DictionaryService
from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.dictionary_dto import DictionaryDto

from routes.auth.jwt_bearer import JwtBearer
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
from tools.exceptions import DictionaryError


def create_dictionary_router(config: Configuration):
    tag = "dictionary"
    router = APIRouter()

    def get_dictionary_service() -> DictionaryService:
        """Retrieve the dictionary service instance from the configuration."""
        return config.get_dictionary_service()

    @router.get(
        "/",
        tags=[tag],
        response_model=DictionariesResponseDto,
        name="getAllDictionaries",
        summary="Retrieve all dictionaries",
    )
    def get_all_dictionaries(
        dictionary_service: DictionaryService = Depends(get_dictionary_service),
    ) -> DictionariesResponseDto:
        """Retrieve the list of all dictionaries available in the system."""
        return dictionary_service.get_dictionary_list()

    @router.get(
        "/{id}",
        tags=[tag],
        response_model=DictionaryResponseDto,
        name="getDictionary",
        summary="Retrieve a dictionary by ID",
    )
    def get_dictionary(
        id: int, dictionary_service: DictionaryService = Depends(get_dictionary_service)
    ) -> DictionaryResponseDto:
        """Retrieve the details of a specific dictionary by its ID."""
        return dictionary_service.get_dictionary_by_id(id)

    @router.get(
        "/{id}/file",
        tags=[tag],
        name="getDictionaryFile",
        summary="Download a dictionary file by ID",
    )
    def get_dictionary_file(
        id: int, dictionary_service: DictionaryService = Depends(get_dictionary_service)
    ):
        """Download the file associated with a specific dictionary by its ID."""
        response = dictionary_service.get_dictionary_file_path(id)

        if response is not None:
            return FileResponse(response)

        return ResponseDto(
            message=DictionaryError.dictionary_not_found(id),
            status=ResponseStatusEnum.NOT_FOUND,
        )

    @router.get(
        "/{id}/dictionary-preview",
        tags=[tag],
        response_model=DictionaryResponseDto,
        name="getDictionaryPreview",
        summary="Retrieve a dictionary preview by ID",
    )
    def get_dictionary_preview(
        id: int, dictionary_service: DictionaryService = Depends(get_dictionary_service)
    ) -> DictionaryResponseDto:
        """Retrieve the preview of a specific dictionary by its ID."""
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
        dictionary_service: DictionaryService = Depends(get_dictionary_service),
        summary="Create a new dictionary",
    ) -> DictionaryResponseDto:
        """Create a new dictionary with metadata and an optional file."""
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
        summary="Update dictionary file by ID",
    )
    async def update_dictionary_file(
        id: int,
        file: Annotated[UploadFile, File()],
        dictionary_service: DictionaryService = Depends(get_dictionary_service),
    ) -> DictionaryResponseDto:
        """Update the file associated with a specific dictionary by its ID."""
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
        summary="Update dictionary metadata by ID",
    )
    def update_dictionary_metadata(
        id: int,
        dictionary: DictionaryDto,
        dictionary_service: DictionaryService = Depends(get_dictionary_service),
    ) -> DictionaryResponseDto:
        """Update the metadata of a specific dictionary by its ID."""
        return dictionary_service.update_dictionary_metadata(id, dictionary)

    @router.delete(
        "/{id}",
        tags=[tag],
        response_model=ResponseDto,
        dependencies=[Depends(JwtBearer())],
        name="deleteDictionary",
        summary="Delete a dictionary by ID",
    )
    def delete_dictionary(
        id: int, dictionary_service: DictionaryService = Depends(get_dictionary_service)
    ) -> ResponseDto:
        """Delete a specific dictionary by its ID."""
        return dictionary_service.delete_dictionary(id)

    return router


dictionaries_router = create_dictionary_router
