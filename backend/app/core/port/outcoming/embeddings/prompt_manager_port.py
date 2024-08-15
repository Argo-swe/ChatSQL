from abc import ABC, abstractmethod

from core.port.outcoming.embeddings.debug_manager_port import DebugManagerPort
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort


class PromptManagerPort(ABC):

    def __init__(self, index_manager: IndexManagerPort):
        self._index_manager = index_manager
        self._debug_manager = self._create_debug_manager()

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

    @abstractmethod
    def get_index_manager(self) -> IndexManagerPort:
        pass

    @abstractmethod
    def _create_debug_manager(self) -> DebugManagerPort:
        pass
