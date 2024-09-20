from typing import Optional
from models.admin_dto import AdminDto
from .models import Admins
from .base import SessionLocal
from core.port.outcoming.authentication_repository import AuthenticationRepository


class SqlAlchemyAuthenticationRepositoryAdapter(AuthenticationRepository):

    def __init__(self, session=SessionLocal()):
        self._session = session

    def get_admin_by_username(self, username: str) -> Optional[AdminDto]:
        admin = self._session.query(Admins).filter(Admins.username == username).first()

        if admin is None:
            return None

        return AdminDto.from_orm(admin)
