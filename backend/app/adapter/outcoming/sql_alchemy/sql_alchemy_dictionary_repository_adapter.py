from .models import Dictionaries
from .base import SessionLocal
from core.port.outcoming.dictionary_repository import DictionaryRepository


class SqlAlchemyDictionaryRepositoryAdapter(DictionaryRepository):

    def __init__(self):
        self._session = SessionLocal()

    def get_all_dictionaries(self):
        return self._session.query(Dictionaries).all()

    def get_dictionary_by_id(self, id: int):
        return self._session.query(Dictionaries).filter(Dictionaries.id == id).first()

    def get_dictionary_by_name(self, name: str):
        return (
            self._session.query(Dictionaries).filter(Dictionaries.name == name).first()
        )

    def create_dictionary(self, name: str, description: str):
        db_dictionary = Dictionaries(name=name, description=description)
        self._session.add(db_dictionary)
        self._session.commit()
        self._session.refresh(db_dictionary)
        return db_dictionary

    def update_dictionary(self, id: int, name: str, description: str):
        current_dictionary = self.get_dictionary_by_id(id)
        current_dictionary.name = name
        current_dictionary.description = description
        self._session.commit()
        self._session.refresh(current_dictionary)
        return current_dictionary

    def delete_dictionary(self, id: int):
        dictionary = self.get_dictionary_by_id(id)
        self._session.delete(dictionary)
        self._session.commit()
