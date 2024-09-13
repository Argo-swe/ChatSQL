from adapter.outcoming.embeddings.txtai.txtai_debug_manager_adapter import (
    TxtaiDebugManagerAdapter,
)
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort


class TxtaiPromptManagerAdapter(PromptManagerPort):
    def __init__(
        self, index_manager: IndexManagerPort, file_repository: FileRepository
    ):
        self._index_manager = index_manager
        self._debug_manager = TxtaiDebugManagerAdapter(self._index_manager)
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
        tuples, log_content_phase_1 = self.__get_tuples(user_request, activate_log)
        relevant_tuples, log_content_phase_2 = self.__get_relevant_tuples(
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

    def __get_tuples(self, user_request: str, activate_log: bool):
        """Execute an SQL-like query using txtai to perform semantic search on table and column description fields.

        Args:
            user_request (str): The user's query string, which is used to search for relevant matches.
            activate_log (bool): Flag indicating whether to log the details of the semantic search process.

        Returns:
            tuple: 
                - The results of the semantic search.
                - A list of log entries (if logging is enabled), otherwise an empty list.
        """
        query_limit = 20
        # The max_score field can vary from 0.3 to 0.4. This affects system recall
        sql_query = f"""
            SELECT table_name, text, table_pos, column_description, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE
            similar(':x', 'table_description') AND
            similar(':x', 'column_description') AND
            score >= 0.2
            GROUP BY table_name
            HAVING max_score >= 0.35
            ORDER BY max_score DESC
            LIMIT {query_limit}
        """
        tuples = self._index_manager.get_embeddings().search(
            sql_query, limit=query_limit * 10, parameters={"x": user_request}
        )
        log_content = []
        if activate_log:
            log_content = self._debug_manager.semantic_search_log(user_request, tuples)
        return tuples, log_content

    def get_index_manager(self) -> IndexManagerPort:
        return self._index_manager

    def __get_relevant_tuples(self, tuples, activate_log):
        """Filters the tuples to find the most relevant ones based on their scores.

        Args:
            tuples: The tuples to filter.
            activate_log: A flag to indicate whether the filtering process should be logged.

        Returns:
            tuple:
                - A list of tuples that have been deemed relevant based on score thresholds.
                - A list of log entries (if logging is enabled), otherwise an empty list.
        """
        relevant_tuples = []
        score = 0
        log_content = []
        for tuple in tuples:
            scoring_distance = score - tuple["max_score"]
            if tuple["max_score"] >= 0.45:
                relevant_tuples.append(tuple)
                score = tuple["max_score"]
            # The scoring_distance variable can vary from 0.15 to 0.25. This affects system recall
            elif scoring_distance <= 0.2:
                relevant_tuples.append(tuple)
            else:
                break
        if activate_log:
            log_content = self._debug_manager.semantic_search_log_custom_algorithm(
                relevant_tuples, tuples
            )
            
        return relevant_tuples, log_content
