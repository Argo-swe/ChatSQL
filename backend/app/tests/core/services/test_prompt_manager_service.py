from models.prompt_dto import PromptDto
from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort
from core.service.dictionary_service import DictionaryService
from core.service.prompt_manager_service import PromptManagerService
from models.responses.response_dto import ResponseStatusEnum
from models.responses.string_data_response_dto import StringDataResponseDto
from tools.exceptions import PromptError
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_dependencies():
    return {
        "dictionary_service": MagicMock(spec=DictionaryService),
        "prompt_manager": MagicMock(spec=PromptManagerPort),
    }


@pytest.fixture
def service(mock_dependencies):
    return PromptManagerService(
        dictionary_service=mock_dependencies["dictionary_service"],
        prompt_manager=mock_dependencies["prompt_manager"],
    )


def test_generate_prompt_dictionary_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_service"].get_dictionary_by_id.return_value = (
        StringDataResponseDto(
            message="Dictionary with id 1 not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )
    )

    response = service.generate_prompt(1, "Example prompt", "mysql", "english")

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.data is None
    assert response.message == "Dictionary with id 1 not found"


def test_generate_prompt_missing_query(service, mock_dependencies):
    mock_dependencies["dictionary_service"].get_dictionary_by_id.return_value = (
        StringDataResponseDto(data="", status=ResponseStatusEnum.OK)
    )

    response = service.generate_prompt(1, "", "mysql", "english")

    assert response.status == ResponseStatusEnum.BAD_REQUEST
    assert response.message == PromptError.missing_query()


def test_generate_prompt_success(service, mock_dependencies):
    mock_dependencies["dictionary_service"].get_dictionary_by_id.return_value = (
        StringDataResponseDto(data="", status=ResponseStatusEnum.OK)
    )
    mock_dependencies["prompt_manager"].prompt_generator.return_value = (
        "generated_prompt",
        None,
    )

    response = service.generate_prompt(1, "Example prompt", "mysql", "english")

    assert response.status == ResponseStatusEnum.OK
    assert response.data == "generated_prompt"
    mock_dependencies[
        "dictionary_service"
    ].get_dictionary_by_id.assert_called_once_with(1)
    mock_dependencies["prompt_manager"].prompt_generator.assert_called_once_with(
        1, "Example prompt", "mysql", "english", activate_log=False
    )


def test_generate_prompt_with_debug_dictionary_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_service"].get_dictionary_by_id.return_value = (
        StringDataResponseDto(
            message="Dictionary with id 1 not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )
    )

    response = service.generate_prompt_with_debug(
        1, "Example prompt", "mysql", "english"
    )

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.data is None
    assert response.message == "Dictionary with id 1 not found"


def test_generate_prompt_with_debug_missing_query(service, mock_dependencies):
    mock_dependencies["dictionary_service"].get_dictionary_by_id.return_value = (
        StringDataResponseDto(data="", status=ResponseStatusEnum.OK)
    )

    response = service.generate_prompt_with_debug(1, "", "mysql", "english")

    assert response.status == ResponseStatusEnum.BAD_REQUEST
    assert response.message == PromptError.missing_query()


def test_generate_prompt_with_debug_success(service, mock_dependencies):
    mock_dependencies["dictionary_service"].get_dictionary_by_id.return_value = (
        StringDataResponseDto(data="", status=ResponseStatusEnum.OK)
    )
    mock_dependencies["prompt_manager"].prompt_generator.return_value = (
        "generated_prompt",
        "debug_info",
    )

    response = service.generate_prompt_with_debug(
        1, "Example prompt", "mysql", "english"
    )

    assert response.status == ResponseStatusEnum.OK
    assert response.data == PromptDto(prompt="generated_prompt", debug="debug_info")
    mock_dependencies[
        "dictionary_service"
    ].get_dictionary_by_id.assert_called_once_with(1)
    mock_dependencies["prompt_manager"].prompt_generator.assert_called_once_with(
        1, "Example prompt", "mysql", "english", activate_log=True
    )
