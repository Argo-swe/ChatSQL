class DictionaryError:
    """A collection of methods for generating error messages related to dictionary operations."""

    @staticmethod
    def dictionary_already_exists(name: str) -> str:
        """Generates an error message indicating that a dictionary with the specified name already exists.

        Args:
            name (str): The name of the dictionary.

        Returns:
            str: An appropriate error message.
        """
        return f"Dictionary with name '{name}' already exists"

    @staticmethod
    def file_too_large() -> str:
        """Generates an error message indicating that the dictionary schema file is too large.

        Returns:
            str: An appropriate error message.
        """
        return "Dictionary file is too large, max size 1MB"

    @staticmethod
    def format_error() -> str:
        """Generates an error message indicating that the dictionary schema is badly formatted.

        Returns:
            str: An appropriate error message.
        """
        return "Dictionary schema is bad formatted"

    @staticmethod
    def missing_dictionary_file() -> str:
        """Generates an error message indicating that the dictionary file is missing.

        Returns:
            str: An appropriate error message.
        """
        return "Dictionary file is mandatory"

    @staticmethod
    def missing_dictionary_metadata() -> str:
        """Generates an error message indicating that the dictionary metadata (name and description) is missing.

        Returns:
            str: An appropriate error message.
        """
        return "Dictionary name and description are mandatory"

    @staticmethod
    def dictionary_not_found(id: int) -> str:
        """Generates an error message indicating that a dictionary with the specified ID was not found.

        Args:
            id (int): The ID of the dictionary.

        Returns:
            str: An appropriate error message.
        """
        return f"Dictionary with id {id} not found"


class LoginError:
    """A collection of methods for generating error messages related to login operations."""

    @staticmethod
    def wrong_password() -> str:
        """Generates an error message indicating that the provided password is incorrect.

        Returns:
            str: An appropriate error message.
        """
        return "Wrong password"

    @staticmethod
    def invalid_authentication_scheme() -> str:
        """Generates an error message indicating that the authentication scheme is invalid.

        Returns:
            str: An appropriate error message.
        """
        return "Invalid authentication scheme"

    @staticmethod
    def invalid_authorization_code() -> str:
        """Generates an error message indicating that the authorization code is invalid.

        Returns:
            str: An appropriate error message.
        """
        return "Invalid authorization code"

    @staticmethod
    def invalid_expired_token() -> str:
        """Generates an error message indicating that the token is either invalid or expired.

        Returns:
            str: An appropriate error message.
        """
        return "Invalid or expired token"


class PromptError:
    """A collection of methods for providing error messages related to prompt generation."""

    @staticmethod
    def missing_query() -> str:
        """Generates an error message indicating that the user request cannot be empty.

        Returns:
            str: An appropriate error message.
        """
        return "Query cannot be empty"
