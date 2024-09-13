from models.dictionary_internal_structure.table_dto import TableDto
from models.dictionary_preview_dto import DictionaryPreviewDto
from core.port.outcoming.dictionary_repository import DictionaryRepository
from core.service.dictionary_service import DictionaryService
from tools.exceptions import DictionaryError
from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseStatusEnum
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_dependencies():
    return {
        "dictionary_repository": MagicMock(spec=DictionaryRepository),
        "index_manager": MagicMock(),
        "file_repository": MagicMock(),
        "schema_validator": MagicMock(),
    }


@pytest.fixture
def service(mock_dependencies):
    return DictionaryService(
        dictionary_repository=mock_dependencies["dictionary_repository"],
        index_manager=mock_dependencies["index_manager"],
        file_repository=mock_dependencies["file_repository"],
        schema_validator=mock_dependencies["schema_validator"],
    )


def test_get_dictionary_list(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_all_dictionaries.return_value = [
        DictionaryDto(id=1, name="Dict1", description="Description1"),
        DictionaryDto(id=2, name="Dict2", description="Description2"),
    ]

    response = service.get_dictionary_list()

    assert response.status == ResponseStatusEnum.OK
    assert len(response.data) == 2
    assert response.data[0].name == "Dict1"
    mock_dependencies["dictionary_repository"].get_all_dictionaries.assert_called_once()


def test_get_dictionary_by_id_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        DictionaryDto(id=1, name="Dict1", description="Description1")
    )

    response = service.get_dictionary_by_id(1)

    assert response.status == ResponseStatusEnum.OK
    assert response.data.name == "Dict1"
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_id.assert_called_once_with(1)


def test_get_dictionary_by_id_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = None

    response = service.get_dictionary_by_id(1)

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.message == "Dictionary with id 1 not found"
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_id.assert_called_once_with(1)


def test_get_dictionary_file_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        DictionaryDto(id=1, name="Dict1", description="Description1")
    )
    mock_dependencies["file_repository"].get_file_path.return_value = "file_path"

    response = service.get_dictionary_file_path(1)

    assert response == "file_path"
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_id.assert_called_once_with(1)
    mock_dependencies["file_repository"].get_file_path.assert_called_once_with(1)


def test_get_dictionary_file_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = None

    response = service.get_dictionary_file_path(1)

    assert response is None
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_id.assert_called_once_with(1)
    mock_dependencies["file_repository"].load.assert_not_called()


def test_get_dictionary_preview_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        DictionaryDto(id=1, name="Dict1", description="Description1")
    )

    preview_dto = DictionaryPreviewDto(
        database_name="Test Database",
        database_description="Test Description",
        tables=[
            TableDto(name="Table1", description="Table1 description"),
            TableDto(name="Table2", description="Table2 description"),
        ],
    )
    mock_dependencies["file_repository"].get_preview.return_value = preview_dto

    response = service.get_dictionary_preview(1)

    assert response.status == ResponseStatusEnum.OK
    assert response.data == preview_dto

    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_id.assert_called_once_with(1)
    mock_dependencies["file_repository"].get_preview.assert_called_once_with(1)


def test_get_dictionary_preview_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = None

    response = service.get_dictionary_preview(1)

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.message == DictionaryError.dictionary_not_found(1)

    mock_dependencies["file_repository"].get_preview.assert_not_called()


@pytest.mark.asyncio
async def test_create_dictionary(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_name.return_value = (
        None
    )
    mock_dependencies["dictionary_repository"].create_dictionary.return_value = (
        DictionaryDto(id=1, name="Test Dictionary", description="Description")
    )
    mock_dependencies["schema_validator"].validate.return_value = True

    dictionary_dto = DictionaryDto(name="Test Dictionary", description="Description")
    content = '{"valid": "json"}'

    response = await service.create_dictionary(dictionary_dto, content)

    assert response.status == ResponseStatusEnum.OK
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_name.assert_called_once_with("Test Dictionary")
    mock_dependencies[
        "dictionary_repository"
    ].create_dictionary.assert_called_once_with("Test Dictionary", "Description")
    mock_dependencies["schema_validator"].validate.assert_called_once()
    mock_dependencies["file_repository"].save.assert_called_once_with(1, content)
    mock_dependencies["index_manager"].create_index.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_create_dictionary_conflict(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_name.return_value = (
        DictionaryDto(id=1, name="Existing Dictionary", description="Description")
    )

    dictionary_dto = DictionaryDto(
        name="Existing Dictionary", description="Description"
    )
    content = '{"valid": "json"}'

    response = await service.create_dictionary(dictionary_dto, content)

    assert response.status == ResponseStatusEnum.CONFLICT
    assert (
        response.message == "Dictionary with name 'Existing Dictionary' already exists"
    )
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_name.assert_called_once_with("Existing Dictionary")


@pytest.mark.asyncio
async def test_create_dictionary_missing_content(service, mock_dependencies):
    dictionary_dto = DictionaryDto(name="Test Dictionary", description="Description")

    response = await service.create_dictionary(dictionary_dto, "")

    assert response.status == ResponseStatusEnum.BAD_REQUEST
    assert response.message == DictionaryError.missing_dictionary_file()
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_name.assert_not_called()


@pytest.mark.asyncio
async def test_create_dictionary_invalid_content(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_name.return_value = (
        None
    )
    mock_dependencies["schema_validator"].validate.return_value = False

    dictionary_dto = DictionaryDto(name="Test Dictionary", description="Description")
    content = '{"invalid": "json"}'  # Contenuto non valido

    response = await service.create_dictionary(dictionary_dto, content)

    assert response.status == ResponseStatusEnum.BAD_REQUEST
    assert response.message == DictionaryError.format_error()

    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_name.assert_called_once_with("Test Dictionary")
    mock_dependencies["schema_validator"].validate.assert_called_once()

    mock_dependencies["file_repository"].save.assert_not_called()
    mock_dependencies["index_manager"].create_index.assert_not_called()


def test_update_dictionary_metadata(service, mock_dependencies):
    existing_dic = DictionaryDto(id=1, name="Old Name", description="Old Description")
    updated_dic = DictionaryDto(id=1, name="New Name", description="New Description")

    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        existing_dic
    )
    mock_dependencies["dictionary_repository"].get_dictionary_by_name.return_value = (
        None
    )
    mock_dependencies["dictionary_repository"].update_dictionary.return_value = (
        updated_dic
    )

    response = service.update_dictionary_metadata(
        1, DictionaryDto(name="New Name", description="New Description")
    )

    assert response.status == ResponseStatusEnum.OK
    assert response.data == updated_dic
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_id.assert_called_once_with(1)
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_name.assert_called_once_with("New Name")
    mock_dependencies[
        "dictionary_repository"
    ].update_dictionary.assert_called_once_with(1, "New Name", "New Description")


def test_update_dictionary_metadata_name_conflict(service, mock_dependencies):
    existing_dic = DictionaryDto(id=1, name="Old Name", description="Old Description")
    conflicting_dic = DictionaryDto(id=2, name="New Name", description="Description")

    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        existing_dic
    )
    mock_dependencies["dictionary_repository"].get_dictionary_by_name.return_value = (
        conflicting_dic
    )

    response = service.update_dictionary_metadata(
        1, DictionaryDto(name="New Name", description="New Description")
    )

    assert response.status == ResponseStatusEnum.CONFLICT
    assert response.message == "Dictionary with name 'New Name' already exists"
    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_name.assert_called_once_with("New Name")
    mock_dependencies["dictionary_repository"].update_dictionary.assert_not_called()


def test_update_dictionary_metadata_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = None

    response = service.update_dictionary_metadata(
        1, DictionaryDto(name="New Name", description="New Description")
    )

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.message == "Dictionary with id 1 not found"

    mock_dependencies[
        "dictionary_repository"
    ].get_dictionary_by_name.assert_not_called()
    mock_dependencies["dictionary_repository"].update_dictionary.assert_not_called()


@pytest.mark.asyncio
async def test_update_dictionary_file(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        DictionaryDto(id=1, name="Test Dictionary", description="Description")
    )
    mock_dependencies["schema_validator"].validate.return_value = True

    content = '{"valid": "json"}'

    response = await service.update_dictionary_file(1, content)

    assert response.status == ResponseStatusEnum.OK
    mock_dependencies["schema_validator"].validate.assert_called_once()
    mock_dependencies["file_repository"].save.assert_called_once_with(1, content)
    mock_dependencies["index_manager"].create_index.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_update_dictionary_file_invalid_content(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        DictionaryDto(id=1, name="Test Dictionary", description="Description")
    )
    mock_dependencies["schema_validator"].validate.return_value = False

    content = '{"invalid": "json"}'

    response = await service.update_dictionary_file(1, content)

    assert response.status == ResponseStatusEnum.BAD_REQUEST
    assert response.message == DictionaryError.format_error()
    mock_dependencies["schema_validator"].validate.assert_called_once()
    mock_dependencies["file_repository"].save.assert_not_called()


@pytest.mark.asyncio
async def test_update_dictionary_file_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = None

    content = '{"valid": "json"}'

    response = await service.update_dictionary_file(1, content)

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.message == "Dictionary with id 1 not found"

    mock_dependencies["schema_validator"].validate.assert_not_called()
    mock_dependencies["file_repository"].save.assert_not_called()
    mock_dependencies["index_manager"].create_index.assert_not_called()


def test_delete_dictionary(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = (
        DictionaryDto(id=1, name="Test Dictionary", description="Description")
    )

    response = service.delete_dictionary(1)

    assert response.status == ResponseStatusEnum.OK
    mock_dependencies[
        "dictionary_repository"
    ].delete_dictionary.assert_called_once_with(1)
    mock_dependencies["file_repository"].delete.assert_called_once_with(1)
    mock_dependencies["index_manager"].delete_index.assert_called_once_with(1)


def test_delete_dictionary_not_found(service, mock_dependencies):
    mock_dependencies["dictionary_repository"].get_dictionary_by_id.return_value = None

    response = service.delete_dictionary(1)

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.message == "Dictionary with id 1 not found"
    mock_dependencies["dictionary_repository"].delete_dictionary.assert_not_called()
    mock_dependencies["file_repository"].delete.assert_not_called()
    mock_dependencies["index_manager"].delete_index.assert_not_called()
