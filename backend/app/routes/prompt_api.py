from typing import Annotated
from configuration import Configuration
from models.responses.string_data_response_dto import StringDataResponseDto
from models.responses.prompt_response_dto import PromptResponseDto
from routes.auth.jwt_bearer import JwtBearer
from core.service.prompt_manager_service import PromptManagerService

from fastapi import APIRouter, Depends, Query


def create_prompt_router(config: Configuration):
    tag = "prompt"
    router = APIRouter()

    def get_prompt_manager_service() -> PromptManagerService:
        """Retrieve the prompt manager service instance from the configuration."""
        return config.get_prompt_manager_service()

    @router.get(
        "/",
        tags=[tag],
        response_model=StringDataResponseDto,
        name="generatePrompt",
        summary="Generate a prompt based on query parameters",
    )
    def generate_prompt(
        dictionary_id: Annotated[int, Query(alias="dictionaryId")],
        query: str,
        dbms: str,
        lang: str,
        prompt_manager_service: PromptManagerService = Depends(
            get_prompt_manager_service
        ),
    ) -> StringDataResponseDto:
        """Generate a prompt using the provided parameters.

        - **dictionaryId**: ID of the dictionary to be used.
        - **query**: The input query string to generate the prompt.
        - **dbms**: The database management system being used.
        - **lang**: The language for the generated prompt.

        Returns the generated prompt as a string.
        """
        return prompt_manager_service.generate_prompt(dictionary_id, query, lang, dbms)

    @router.get(
        "/debug",
        tags=[tag],
        response_model=PromptResponseDto,
        dependencies=[Depends(JwtBearer())],
        name="generatePromptWithDebug",
        summary="Generate a prompt with debug information",
    )
    def generate_prompt_with_debug(
        dictionary_id: Annotated[int, Query(alias="dictionaryId")],
        query: str,
        dbms: str,
        lang: str,
        prompt_manager_service: PromptManagerService = Depends(
            get_prompt_manager_service
        ),
    ) -> PromptResponseDto:
        """Generate a prompt with detailed debug information.

        - **dictionaryId**: ID of the dictionary to be used.
        - **query**: The input query string to generate the prompt.
        - **dbms**: The database management system being used.
        - **lang**: The language for the generated prompt.

        Returns the generated prompt along with additional debug data.
        """
        return prompt_manager_service.generate_prompt_with_debug(
            dictionary_id, query, lang, dbms
        )

    return router


prompt_router = create_prompt_router
