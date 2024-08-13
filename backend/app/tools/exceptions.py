class DictionaryError:
    @staticmethod
    def dictionary_already_exists(name: str) -> str:
        return f"Dictionary with name '{name}' already exists."

    @staticmethod
    def format_error() -> str:
        return f"Dictionary schema is bad formatted."

    @staticmethod
    def missing_dictionary_file() -> str:
        return f"Dictionary file is mandatory."

    @staticmethod
    def missing_dictionary_metadata() -> str:
        return f"Dictionary name and description are mandatory."
    
    @staticmethod
    def dictionary_not_found(id: str) -> str:
        return f"Dictionary with id {id} not found."

class LoginError:
    @staticmethod
    def wrong_password() -> str:
        return f"Wrong password."

class PromptError:
    @staticmethod
    def missing_query() -> str:
        return f"Query cannot be empty."
