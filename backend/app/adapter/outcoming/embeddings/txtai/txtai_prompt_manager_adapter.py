from adapter.outcoming.embeddings.txtai.txtai_search_algorithm_adapter import TxtaiSearchAlgorithmAdapter
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort


class TxtaiPromptManagerAdapter(PromptManagerPort):
    def __init__(
        self, index_manager: IndexManagerPort, file_repository: FileRepository
    ):
        self._index_manager = index_manager
        self._search_algorithm = TxtaiSearchAlgorithmAdapter(self._index_manager)
        self._file_repository = file_repository

    def prompt_generator(
        self,
        dictionary_id,
        user_request,
        lang="english",
        dbms="MariaDB",
        activate_log=False,
    ) -> tuple[str | None, str | None]:
        self._index_manager.load_index(dictionary_id)
        tuples, log_content_phase_1 = self._search_algorithm.semantic_search(user_request, activate_log)
        relevant_tuples, log_content_phase_2 = self._search_algorithm.search_filtering(
            tuples, activate_log
        )
        if not relevant_tuples:
            return None, None

        dyn_string = self._file_repository.extract_schema_metadata(
            dictionary_id, relevant_tuples
        )

        dyn_string += f"User request: {user_request}.\n"
        dyn_string += f"Convert user request to a suitable SQL query for {dbms}.\n"
        dyn_string += f"Answer in {lang}."
        log_content = (
            "\n".join(log_content_phase_1 + log_content_phase_2)
            if activate_log
            else None
        )
        return dyn_string, log_content

    def get_index_manager(self) -> IndexManagerPort:
        return self._index_manager
