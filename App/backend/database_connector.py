import sqlalchemy

class DatabaseConnector:
    engines = {}

    def __init__(self, url: str = "sqlite:///../../db/chatsql.db"):
        if url not in DatabaseConnector.engines:
            DatabaseConnector.engines[url] = sqlalchemy.create_engine(url)
        self.engine = DatabaseConnector.engines[url]


    def fetchUser(self, username: str):
        with self.engine.connect() as connection:
            result = connection.execute(sqlalchemy.text("SELECT username, password FROM admins WHERE username = :x"), {"x" : username})
            return result.one_or_none()

    def __fetchDictionaryById(self, id: int):
        with self.engine.connect() as connection:
            result = connection.execute(sqlalchemy.text("SELECT id, name, description FROM dictionaries WHERE id = :x"), {"x":id})
            return result.one_or_none()
    
    def __fetchDictionaryByName(self, name: str):
        with self.engine.connect() as connection:
            result = connection.query("SELECT id, name, description FROM dictionaries WHERE name = :x", {"x":name})
            return result.iloc[0]
    
    def fetchDictionary(self, table_field: str, value):
        if(table_field == "id"):
            return self.__fetchDictionaryById(value)
        if(table_field == "name"):
            return self.__fetchDictionaryByName(value)
    
    def insertDictionary(self, name: str, description: str | None = None) -> bool:
        if(name == None or name == ""):
            return False
        try:
            with self.engine.connect() as connection:
                connection.execute(sqlalchemy.text("INSERT INTO dictionaries(name, description) VALUES (:x, :y)"), {"x" : name, "y": description})
                connection.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
                raise ValueError("A dictionary with that name already exists")
    
    def __deleteDictionaryById(self, id) -> bool:
        if(self.__fetchDictionaryById(id).empty):
            return False
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text("DELETE FROM dictionaries WHERE id = :x"), {"x":id})
            connection.commit()
        return True
        
    def __deleteDictionaryByName(self, name) -> bool:
        if(self.__fetchDictionaryByName(name).empty):
            return False
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text("DELETE FROM dictionaries WHERE name = :x"), {"x":name})
            connection.commit()
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
        if((not validinput) or (self.fetchDictionary(key_field, key_value) is None)): # Previous checks fail or entry does not exist 
            return False
        query = f"UPDATE dictionaries SET {update_field} = :y WHERE {key_field} = :x"
        try:
            with self.engine.connect() as connection:
                connection.execute(sqlalchemy.text(query), {"x" : key_value, "y" : update_value})
                connection.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            raise ValueError("A dictionary with that name already exists")
