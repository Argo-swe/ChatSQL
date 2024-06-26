from sqlalchemy.orm import Session

from . import models
from models.dictionary_dto import DictionaryDto

## Admin
def getUserByUsername(db: Session, username: str):
    return db.query(models.Admins).filter(models.Admins.username == username).first()

## Dictionaries
def getAllDictionaries(db: Session):
    return db.query(models.Dictionaries).all()

def getDictionaryById(db: Session, id: int):
    return db.query(models.Dictionaries).filter(models.Dictionaries.id == id).first()

def getDictionaryByName(db: Session, name: str):
    return db.query(models.Dictionaries).filter(models.Dictionaries.name == name).first()

def createDictionary(db: Session, dictionary: DictionaryDto):
    dbDictionary = models.Dictionaries(name=dictionary.name, description=dictionary.description)
    db.add(dbDictionary)
    db.commit()
    db.refresh(dbDictionary)
    return dbDictionary

def updateDictionary(db: Session, dictionary: DictionaryDto):
    currentDictionary = getDictionaryById(db, dictionary.id)
    currentDictionary.name = dictionary.name
    currentDictionary.description = dictionary.description
    db.commit()
    db.refresh(currentDictionary)
    return currentDictionary

def deleteDictionary(db: Session, id: int):
    dictionary = getDictionaryById(db, id)
    db.delete(dictionary)
    db.commit()
