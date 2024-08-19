class DictionaryError:
    @staticmethod
    def dictionary_already_exists(name: str) -> str:
        return f"Dictionary with name '{name}' already exists."

    @staticmethod
    def format_error() -> str:
        return "Dictionary schema is bad formatted."

    @staticmethod
    def missing_dictionary_file() -> str:
        return "Dictionary file is mandatory."

    @staticmethod
    def missing_dictionary_metadata() -> str:
        return "Dictionary name and description are mandatory."

    @staticmethod
    def dictionary_not_found(id: str) -> str:
        return f"Dictionary with id {id} not found."


class LoginError:
    @staticmethod
    def wrong_password() -> str:
        return "Wrong password."

    @staticmethod
    def invalid_authentication_scheme() -> str:
        return "Invalid authentication scheme."

    @staticmethod
    def invalid_authorization_code() -> str:
        return "Invalid authorization code."

    @staticmethod
    def invalid_expired_token() -> str:
        return "Invalid or expired token."


class PromptError:
    @staticmethod
    def missing_query() -> str:
        return "Query cannot be empty."
