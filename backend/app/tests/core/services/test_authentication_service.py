from core.port.outcoming.authentication_repository import AuthenticationRepository
from core.service.authentication_service import AuthenticationService
from models.admin_dto import AdminDto
from models.responses.response_dto import ResponseStatusEnum
from routes.auth.jwt_handler import JwtHandler
from tools.exceptions import LoginError
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_dependencies():
    return {
        "authentication_repository": MagicMock(spec=AuthenticationRepository),
    }


@pytest.fixture
def service(mock_dependencies, monkeypatch):
    mock_sign = MagicMock()
    monkeypatch.setattr(JwtHandler, "sign", mock_sign)

    service_instance = AuthenticationService(
        authentication_repository=mock_dependencies["authentication_repository"],
    )
    return service_instance, mock_sign


def test_login_user_not_found(service, mock_dependencies):
    service_instance, _ = service
    service_instance._authentication_repository.get_user_by_username.return_value = None

    response = service_instance.login(
        username="nonexistent_user", password="password123"
    )

    assert response.status == ResponseStatusEnum.NOT_FOUND
    assert response.data is None
    mock_dependencies[
        "authentication_repository"
    ].get_user_by_username.assert_called_once_with("nonexistent_user")


def test_login_wrong_password(service, mock_dependencies):
    service_instance, _ = service
    mock_user = AdminDto(id=1, username="existing_user", password="correct_password")
    mock_dependencies["authentication_repository"].get_user_by_username.return_value = (
        mock_user
    )

    response = service_instance.login(
        username="existing_user", password="wrong_password"
    )

    assert response.status == ResponseStatusEnum.BAD_CREDENTIAL
    assert response.data is None
    assert response.message == LoginError.wrong_password()
    mock_dependencies[
        "authentication_repository"
    ].get_user_by_username.assert_called_once_with("existing_user")


def test_login_success(service, mock_dependencies):
    service_instance, mock_sign = service
    mock_user = AdminDto(id=1, username="existing_user", password="correct_password")
    mock_dependencies["authentication_repository"].get_user_by_username.return_value = (
        mock_user
    )

    mock_sign.return_value = {"token": "fake_jwt_token"}

    response = service_instance.login("existing_user", "correct_password")

    assert response.status == ResponseStatusEnum.OK
    assert response.data == {"token": "fake_jwt_token"}
    mock_dependencies[
        "authentication_repository"
    ].get_user_by_username.assert_called_once_with("existing_user")
    mock_sign.assert_called_once_with(1)
