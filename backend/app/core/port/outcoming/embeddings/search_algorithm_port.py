from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class SearchAlgorithmPort(ABC):

    @abstractmethod
    def semantic_search(
        self, user_request: str, activate_log: bool
    ) -> Tuple[List[Any], List[str]]:
        """Perform a semantic search process.

        Args:
            user_request (str): The user's query string.
            activate_log (bool): Flag indicating whether to log the details of the semantic search process.

        Returns:
            Tuple:
                - The results of the semantic search.
                - A list of log entries.
        """
