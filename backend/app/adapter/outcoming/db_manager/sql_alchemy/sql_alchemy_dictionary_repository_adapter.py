from typing import List, Optional
from models.dictionary_dto import DictionaryDto
from .models import Dictionaries
from .base import SessionLocal
from core.port.outcoming.dictionary_repository import DictionaryRepository


class SqlAlchemyDictionaryRepositoryAdapter(DictionaryRepository):

    def __init__(self, session=SessionLocal()):
        self._session = session

    def get_all_dictionaries(self) -> List[DictionaryDto]:
        dictionaries = self._session.query(Dictionaries).all()

        return [DictionaryDto.from_orm(dictionary) for dictionary in dictionaries]

    def get_dictionary_by_id(self, id: int) -> Optional[DictionaryDto]:
        dictionary = (
            self._session.query(Dictionaries).filter(Dictionaries.id == id).first()
        )

        if dictionary is None:
            return None

        return DictionaryDto.from_orm(dictionary)

    def get_dictionary_by_name(self, name: str) -> Optional[DictionaryDto]:
        dictionary = (
            self._session.query(Dictionaries).filter(Dictionaries.name == name).first()
        )

        if dictionary is None:
            return None

        return DictionaryDto.from_orm(dictionary)

    def create_dictionary(self, name: str, description: str) -> DictionaryDto:
        db_dictionary = Dictionaries(name=name, description=description)
        self._session.add(db_dictionary)
        self._session.commit()
        self._session.refresh(db_dictionary)
        return DictionaryDto.from_orm(db_dictionary)

    def update_dictionary(
        self, id: int, name: str, description: str
    ) -> Optional[DictionaryDto]:
        current_dictionary = (
            self._session.query(Dictionaries).filter(Dictionaries.id == id).first()
        )

        if current_dictionary is None:
            return None

        current_dictionary.name = name
        current_dictionary.description = description
        self._session.commit()
        self._session.refresh(current_dictionary)
        return DictionaryDto.from_orm(current_dictionary)

    def delete_dictionary(self, id: int):
        dictionary = (
            self._session.query(Dictionaries).filter(Dictionaries.id == id).first()
        )
        if dictionary:
            self._session.delete(dictionary)
            self._session.commit()
