from abc import ABC, abstractmethod


class DebugManagerPort(ABC):

    @abstractmethod
    def semantic_search_log(self, user_request, tuples):
        pass

    @abstractmethod
    def semantic_search_log_custom_algorithm(self, relevant_tuples, tuples):
        pass
