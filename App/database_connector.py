import streamlit
import sqlalchemy

class DatabaseConnector:
    def __init__(self):
        self.connection = streamlit.connection("sqlite", "sql")

    # Ritorna una riga di dataframe ("username", "password")
    def fetch_user(self, username):
        result = self.connection.query("SELECT username, password FROM admins WHERE username = :x", params={"x":username})
        return result.iloc[0]

    # Ritorna una riga di dataframe ("id", "name, "description")
    def __fetch_dictionary_by_id__(self, id):
        result = self.connection.query("SELECT id, name, description FROM dictionaries WHERE id = :x", params={"x":id})
        return result.iloc[0]
    
    def __fetch_dictionary_by_name__(self, name):
        result = self.connection.query("SELECT id, name, description FROM dictionaries WHERE name = :x", params={"x":name})
        return result.iloc[0]
    
    def fetch_dictionary(self, table_field, value):
        if(table_field == "id"):
            return self.__fetch_dictionary_by_id__(value)
        if(table_field == "name"):
            return self.__fetch_dictionary_by_name__(value)


    # Raises ValueError for null or non unique values
    def insert_dictionary(self, name, description=None):
        if(name == None or name == ""):
            return False
        try:
            with self.connection.session as session:
                session.execute(sqlalchemy.text("INSERT INTO dictionaries(name, description) VALUES (:x, :y)"), {"x" : name, "y": description})
                session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
                raise ValueError("A dictionary with that name already exists")
    
    def __delete_dictionary_by_id__(self, id):
        if(self.__fetch_dictionary_by_name__(id).empty):
            return False
        with self.connection.session as session:
            session.execute(sqlalchemy.text("DELETE FROM dictionaries WHERE id = :x"),{"x":id})
            session.commit()
        return True
        
    def __delete_dictionary_by_name__(self, name):
        if(self.__fetch_dictionary_by_name__(name).empty):
            return False
        with self.connection.session as session:
            session.execute(sqlalchemy.text("DELETE FROM dictionaries WHERE name = :x"),{"x":name})
            session.commit()
        return True

    def delete_dictionary(self, table_field, field_value):
        if(table_field == "id"):
            return self.__delete_dictionary_by_id__(field_value)
        if(table_field == "name"):
            return self.__delete_dictionary_by_name__(field_value)
        return False


    def __update_dictionary_name__(self, old_name, new_name):
        if(old_name == None):
            return False
        if(new_name == None or new_name == ""):
            return False
        try:
            with self.connection.session as session:
                session.execute(sqlalchemy.text("UPDATE dictionaries SET name = :y WHERE name = :x"),{"x" : old_name, "y" : new_name})
                session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            raise ValueError("A dictionary with that name already exists")

    def __update_dictionary_description__(self, name, new_description):
        if(self.__fetch_dictionary_by_name__(name).empty):  # A dictionary with that name could not be found
            return False
        with self.connection.session as session:
            session.execute(sqlalchemy.text("UPDATE dictionries SET description = :y WHERE name = :x"), {"x" : name, "y" : new_description})
            session.commit()
        return True

    def update_dictionary(self, dictionary_name, table_field, new_value):
        if(table_field == "name"):
            return self.__update_dictionary_name__(dictionary_name, new_value)            
        if(table_field == "description"):
            return self.__update_dictionary_description__(dictionary_name, new_value)
        return False