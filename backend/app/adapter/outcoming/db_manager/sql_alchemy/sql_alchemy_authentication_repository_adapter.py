from .models import Admins
from .base import SessionLocal
from core.port.outcoming.authentication_repository import AuthenticationRepository


class SqlAlchemyAuthenticationRepositoryAdapter(AuthenticationRepository):

    def __init__(self, session=SessionLocal()):
        self._session = session

    def get_user_by_username(self, username: str):
        return self._session.query(Admins).filter(Admins.username == username).first()
