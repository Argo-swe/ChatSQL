from abc import ABC, abstractmethod


class DebugManagerPort(ABC):

    @abstractmethod
    def semantic_search_log(self, user_request, tuples):
        pass

    @abstractmethod
    def log_phase_2(self, relevant_tuples, tuples):
        pass
