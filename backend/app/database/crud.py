from sqlalchemy.orm import Session

from . import models
from models.dictionary_dto import DictionaryDto


# Admin
def get_user_by_username(db: Session, username: str):
    return db.query(models.Admins).filter(models.Admins.username == username).first()


# Dictionaries
def get_all_dictionaries(db: Session):
    return db.query(models.Dictionaries).all()


def get_dictionary_by_id(db: Session, id: int):
    return db.query(models.Dictionaries).filter(models.Dictionaries.id == id).first()


def get_dictionary_by_name(db: Session, name: str):
    return (
        db.query(models.Dictionaries).filter(models.Dictionaries.name == name).first()
    )


def create_dictionary(db: Session, dictionary: DictionaryDto):
    db_dictionary = models.Dictionaries(
        name=dictionary.name, description=dictionary.description
    )
    db.add(db_dictionary)
    db.commit()
    db.refresh(db_dictionary)
    return db_dictionary


def update_dictionary(db: Session, dictionary: DictionaryDto):
    current_dictionary = get_dictionary_by_id(db, dictionary.id)
    current_dictionary.name = dictionary.name
    current_dictionary.description = dictionary.description
    db.commit()
    db.refresh(current_dictionary)
    return current_dictionary


def delete_dictionary(db: Session, id: int):
    dictionary = get_dictionary_by_id(db, id)
    db.delete(dictionary)
    db.commit()
