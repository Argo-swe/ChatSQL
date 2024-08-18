from abc import ABC, abstractmethod


class AuthenticationRepository(ABC):

    @abstractmethod
    def get_user_by_username(self, username):
        pass
