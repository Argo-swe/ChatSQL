from abc import ABC, abstractmethod
from typing import List


class DebugManagerPort(ABC):

    @abstractmethod
    def semantic_search_log(self, user_request: str, tuples: list) -> List[str]:
        """Log the details of a semantic search operation.

        Args:
            user_request (str): The user's search query or request.
            tuples (list): A list of tuples representing the search results or related data.

        Returns:
            List[str]: A list of log entries detailing the prompt generation process.
        """
        pass

    @abstractmethod
    def semantic_search_log_custom_algorithm(
        self, relevant_tuples: list, tuples: list
    ) -> List[str]:
        """Log the details of a semantic search operation using a custom algorithm.

        Args:
            relevant_tuples (list): A list of tuples representing the results deemed relevant by the custom algorithm.
            tuples (list): A list of all tuples considered during the search.

        Returns:
            List[str]: A list of log entries detailing the prompt generation process.
        """
        pass
