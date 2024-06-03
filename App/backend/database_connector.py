import streamlit
import sqlalchemy

class DatabaseConnector:
    def __init__(self):
        self.connection = streamlit.connection("sqlite", "sql")

    def fetchUser(self, username: str):
        result = self.connection.query("SELECT username, password FROM admins WHERE username = :x", params={"x":username})
        return result.iloc[0]

    def __fetchDictionaryById(self, id: int):
        result = self.connection.query("SELECT id, name, description FROM dictionaries WHERE id = :x", params={"x":id})
        return result.iloc[0]
    
    def __fetchDictionaryByName(self, name: str):
        result = self.connection.query("SELECT id, name, description FROM dictionaries WHERE name = :x", params={"x":name})
        return result.iloc[0]
    
    def fetchDictionary(self, table_field: str, value):
        if(table_field == "id"):
            return self.__fetchDictionaryById(value)
        if(table_field == "name"):
            return self.__fetchDictionaryByName(value)
    
    def insertDictionary(self, name: str, description: str) -> bool:
        if(name == None or name == ""):
            return False
        try:
            with self.connection.session as session:
                session.execute(sqlalchemy.text("INSERT INTO dictionaries(name, description) VALUES (:x, :y)"), {"x" : name, "y": description})
                session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
                raise ValueError("A dictionary with that name already exists")
    
    def __deleteDictionaryById(self, id: int) -> bool:
        if(self.__fetchDictionaryById(id).empty):
            return False
        with self.connection.session as session:
            session.execute(sqlalchemy.text("DELETE FROM dictionaries WHERE id = :x"),{"x":id})
            session.commit()
        return True
        
    def __deleteDictionaryByName(self, name: str) -> bool:
        if(self.__fetchDictionaryByName(name).empty):
            return False
        with self.connection.session as session:
            session.execute(sqlalchemy.text("DELETE FROM dictionaries WHERE name = :x"),{"x":name})
            session.commit()
        return True

    def deleteDictionary(self, table_field: str, field_value) -> bool:
        if(table_field == "id"):
            return self.__deleteDictionaryById(field_value)
        if(table_field == "name"):
            return self.__deleteDictionaryByName(field_value)
        return False

    def updateDictionary(self, key_field: str, key_value, update_field: str, update_value: str) -> bool:
        validinput =    (key_field == "id" or key_field == "name") and \
                        (update_field == "name" or update_field == "description") and \
                        ((update_value != "" and update_value != None) if update_field == "name" else True) # Additional check for an updated name to be not None or empty
        if((not validinput) or self.fetchDictionary(key_field, key_value).empty): # Previous checks fail or entry does not exist 
            return False
        query = f"UPDATE dictionaries SET {update_field} = :y WHERE {key_field} = :x"
        try:
            with self.connection.session as session:
                session.execute(sqlalchemy.text(query), {"x" : key_value, "y" : update_value})
                session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            raise ValueError("A dictionary with that name already exists")
