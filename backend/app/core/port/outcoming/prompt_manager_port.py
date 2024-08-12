from abc import ABC, abstractmethod


class PromptManagerPort(ABC):

    @abstractmethod
    def prompt_generator(
        self,
        dictionary_id: int,
        user_request: str,
        lang="english",
        dbms="MariaDB",
        activate_log=False,
    ):
        pass
