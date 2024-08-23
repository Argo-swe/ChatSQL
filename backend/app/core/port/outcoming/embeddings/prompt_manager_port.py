from abc import ABC, abstractmethod

from core.port.outcoming.embeddings.debug_manager_port import DebugManagerPort
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort


class PromptManagerPort(ABC):

    def __init__(self, index_manager: IndexManagerPort):
        """Initialize the PromptManagerPort with an IndexManagerPort instance.

        Args:
            index_manager (IndexManagerPort): The index manager used to manage indexing operations.
        """
        self._index_manager = index_manager
        self._debug_manager = self._create_debug_manager()

    @abstractmethod
    def prompt_generator(
        self,
        dictionary_id: int,
        user_request: str,
        lang: str = "english",
        dbms: str = "MariaDB",
        activate_log: bool = False,
    ):
        """Generate a prompt based on the provided parameters.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.
            user_request (str): The user request or query to generate the prompt.
            lang (str, optional): The language for the prompt (default is "english").
            dbms (str, optional): The database management system to be used (default is "MariaDB").
            activate_log (bool, optional): Whether to activate logging (default is False).

        Returns:
            Any: The generated prompt.
        """

    @abstractmethod
    def get_index_manager(self) -> IndexManagerPort:
        """Retrieve the current IndexManagerPort instance.

        Returns:
            IndexManagerPort: The index manager instance.
        """

    @abstractmethod
    def _create_debug_manager(self) -> DebugManagerPort:
        """Create and return a DebugManagerPort instance for managing debug operations.

        Returns:
            DebugManagerPort: The debug manager instance.
        """
