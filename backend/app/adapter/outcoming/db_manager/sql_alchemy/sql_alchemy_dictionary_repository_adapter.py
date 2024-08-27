from typing import List
from models.dictionary_dto import DictionaryDto
from .models import Dictionaries
from .base import SessionLocal
from core.port.outcoming.dictionary_repository import DictionaryRepository


class SqlAlchemyDictionaryRepositoryAdapter(DictionaryRepository):

    def __init__(self, session=SessionLocal()):
        self._session = session

    def get_all_dictionaries(self) -> List[DictionaryDto]:
        return self._session.query(Dictionaries).all()

    def get_dictionary_by_id(self, id: int) -> DictionaryDto:
        return self._session.query(Dictionaries).filter(Dictionaries.id == id).first()

    def get_dictionary_by_name(self, name: str) -> DictionaryDto:
        return (
            self._session.query(Dictionaries).filter(Dictionaries.name == name).first()
        )

    def create_dictionary(self, name: str, description: str) -> DictionaryDto:
        db_dictionary = Dictionaries(name=name, description=description)
        self._session.add(db_dictionary)
        self._session.commit()
        self._session.refresh(db_dictionary)
        return db_dictionary

    def update_dictionary(self, id: int, name: str, description: str) -> DictionaryDto:
        current_dictionary = self.get_dictionary_by_id(id)
        current_dictionary.name = name
        current_dictionary.description = description
        self._session.commit()
        self._session.refresh(current_dictionary)
        return current_dictionary

    def delete_dictionary(self, id: int):
        dictionary = self.get_dictionary_by_id(id)
        if dictionary:
            self._session.delete(dictionary)
            self._session.commit()
