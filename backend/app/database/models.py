from sqlalchemy import Column, Integer, String, event

from .base import Base


class Admins(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


class Dictionaries(Base):
    __tablename__ = "dictionaries"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)


# creazione dati di default
def insert_data_admins(target, connection, **kw):
    connection.execute(
        target.insert(), {"id": 1, "username": "admin", "password": "admin"}
    )


event.listen(Admins.__table__, "after_create", insert_data_admins)
