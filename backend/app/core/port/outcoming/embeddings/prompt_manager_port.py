from abc import ABC, abstractmethod

from core.port.outcoming.embeddings.debug_manager_port import DebugManagerPort
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort


class PromptManagerPort(ABC):

    @abstractmethod
    def prompt_generator(
        self,
        dictionary_id: int,
        user_request: str,
        lang: str = "english",
        dbms: str = "MariaDB",
        activate_log: bool = False,
    ) -> tuple[str | None, str | None]:
        """Generate a prompt based on the provided parameters.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.
            user_request (str): The user request or query to generate the prompt.
            lang (str, optional): The language for the prompt (default is "english").
            dbms (str, optional): The database management system to be used (default is "MariaDB").
            activate_log (bool, optional): Whether to activate logging (default is False).

        Returns:
            tuple[str | None, str | None]: A tuple containing the generated prompt and optional debug information.
        """

    @abstractmethod
    def get_index_manager(self) -> IndexManagerPort:
        """Retrieve the current IndexManagerPort instance.

        Returns:
            IndexManagerPort: The index manager instance.
        """
