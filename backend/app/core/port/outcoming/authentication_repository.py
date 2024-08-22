from abc import ABC, abstractmethod

from models.admin_dto import AdminDto


class AuthenticationRepository(ABC):

    @abstractmethod
    def get_user_by_username(self, username: str) -> AdminDto:
        """Retrieve user details by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            The user details associated with the given username.
        """
        pass
